from .symtable.symbol_table import SymbolTable, Scope
from .abstract_syntax_tree.ast_node import ASTNode
from enum import Enum

class ReturnType(Enum):
    no = 0
    total = 1
    partialSum = 2
    partialMult = 3

symbolT = SymbolTable()


def analiseSemantica(info, sum = 0, mult = 1):
    global symbolT
    if(info != None and type(info) is ASTNode):
        if (info.type == "mexp" ):
            sum = 0
            if(info.val):
                return ReturnType.total
            elif len(info.children) > 1:                            
                if(info.children[1] == "*"  and info.children[2].val != None):                     
                    mult = mult * info.children[2].val
                    resp = analiseSemantica(info.children[0], mult = mult)
                    if resp == ReturnType.partialMult:
                        info.set(
                            type = info.children[0].type,
                            children = info.children[0].children,
                            val = info.children[0].val,
                            cgen = info.children[0].cgen)
                    else:
                        #TODO mudar os filhos na arvore
                        setValToAll(info.children[2], mult)
                        #info.children[2].val = mult
                    return ReturnType.partialMult
                elif(info.children[1] == "*"  and info.children[0].val != None):                              
                    mult = mult * info.children[0].val
                    resp = analiseSemantica(info.children[2], mult = mult)
                    if resp == ReturnType.partialMult:
                        info.set(
                            type = info.children[2].type,
                            children = info.children[2].children,
                            val = info.children[2].val,
                            cgen = info.children[2].cgen)
                    else:
                        #TODO mudar os filhos na arvore
                        setValToAll(info.children[0], mult)
                        #info.children[0].val = mult
                    return ReturnType.partialMult
                else:
                    resp = analiseSemantica(info.children[0], mult = mult)
                    if resp == ReturnType.partialMult:
                        analiseSemantica(info.children[2])
                        return ReturnType.partialMult
                    else:
                        return analiseSemantica(info.children[2], mult = mult)

        elif (info.type == "aexp"):
            mult = 1
            if(info.val):
                return ReturnType.partialSum
            elif len(info.children) > 1:                            
                if(info.children[1] and info.children[2].val != None):
                    if(info.children[1] == "+" ):
                        sum = sum + info.children[2].val
                    if(info.children[1] == "-" ):
                        sum = sum + info.children[2].val
                    resp = analiseSemantica(info.children[0], sum)
                    if resp == ReturnType.partialSum:
                        info.set(
                            type = info.children[0].type,
                            children = info.children[0].children,
                            val = info.children[0].val,
                            cgen = info.children[0].cgen)
                    else:
                        setValToAll(info.children[2], sum)
                        #info.children[2].val = sum
                    return ReturnType.partialSum
                elif(info.children[1] and info.children[0].val != None):
                    if(info.children[1] == "+" ):
                        sum = sum + info.children[0].val
                    if(info.children[1] == "-" ):
                        sum = info.children[0].val - sum
                    resp = analiseSemantica(info.children[2], sum)
                    if resp == ReturnType.partialSum:
                        info.set(
                            type = info.children[2].type,
                            children = info.children[2].children,
                            val = info.children[2].val,
                            cgen = info.children[2].cgen)
                    else:
                        setValToAll(info.children[0], sum)
                        #info.children[0].val = sum
                    return ReturnType.partialSum
                else:
                    resp = analiseSemantica(info.children[0], sum = sum)
                    if resp == ReturnType.partialSum:
                        analiseSemantica(info.children[2])
                        return ReturnType.partialSum
                    else:
                        return analiseSemantica(info.children[2], sum = sum)
        if info.children != None:
            for item in info.children:
                if type(item) is ASTNode:  
                    if (item.type == "class"):
                        symbolT = SymbolTable()
                        analiseSemantica(item)

                    elif (item.type == "metodo"):
                        symbolT.insert_scope(Scope())
                        analiseSemantica(item)
                        symbolT.remove()
                    else:
                        if (item.type == "var" or item.type == "conj_params"):
                            
                            if (len(item.children[0].children) > 1):
                                
                                symbolT.insert_entry(
                                    item.children[1], {'type': 'int[]'})
                            else:
                                symbolT.insert_entry(item.children[1], {
                                                    'type': item.children[0].children[0]})

                        elif (item.type == "mais_param" and len(item.children) > 1):
                            if (len(item.children[2].children) > 1):
                                symbolT.insert_entry(
                                    item.children[3], {'type': 'int[]'})
                            else:
                                symbolT.insert_entry(item.children[3], {
                                                    'type': item.children[2].children[0]})

                        elif ((item.type == "pexp" or item.type == "cmd2" or item.type == "cmd1") and item.toTable):
                            sco = symbolT.scopes[symbolT.current_scope_level]
                            glob = symbolT.scopes[0]
                            
                            if not (sco.is_in(item.children[0]) or glob.is_in(item.children[0])):
                                print('Erro: Variável {0} não declarada'.format(
                                    item.children[0]))
                        analiseSemantica(item)
def setValToAll(info, val):
    info.set(val = val)
    index = 0
    for item in info.children:
        if type(item) is ASTNode:  
            setValToAll(item, val)
        else:
            info.children[index] = val
    index +=1