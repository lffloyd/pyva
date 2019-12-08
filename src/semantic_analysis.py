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
                    print(info.children[0].val)
                    if resp == ReturnType.partialMult:
                        info.set(
                            type = info.children[0].type,
                            children = info.children[0].children,
                            val = info.children[0].val,
                            cgen = info.children[0].cgen)
                    else:
                        setValToAll(info.children[2], mult)
                    return ReturnType.partialMult
                elif(info.children[1] == "*"  and info.children[0].val != None):                              
                    mult = mult * info.children[0].val
                    #print(info.children[2])
                    resp = analiseSemantica(info.children[2], mult = mult)
                    print(info.children[2].type)
                    print(info.children[2].val)
                    if resp == ReturnType.partialMult:
                        info.set(
                            type = info.children[2].type,
                            children = info.children[2].children,
                            val = info.children[2].val,
                            cgen = info.children[2].cgen)
                    else:
                        setValToAll(info.children[0], mult)
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
                return ReturnType.total
            elif len(info.children) > 1:                            
                if(info.children[1] and info.children[2].val != None):
                    #print(info.children[0])
                    if(info.children[1] == "+" ):
                        sum = sum + info.children[2].val
                    if(info.children[1] == "-" ):
                        sum = sum - info.children[2].val
                    resp = analiseSemantica(info.children[0], sum)
                    print(info.children[0].val)
                    if resp == ReturnType.partialSum:
                        info.set(
                            type = info.children[0].type,
                            children = info.children[0].children,
                            val = info.children[0].val,
                            cgen = info.children[0].cgen)
                    else:
                        setValToAll(info.children[2], sum)
                    return ReturnType.partialSum
                elif(info.children[1] and info.children[0].val != None):
                    #print(info.children[2])
                    if(info.children[1] == "+" ):
                        sum = sum + info.children[0].val
                    if(info.children[1] == "-" ):
                        sum = info.children[0].val - sum
                    resp = analiseSemantica(info.children[2], sum)
                    print(info.children[2].type)
                    print(info.children[2].val)
                    if resp == ReturnType.partialSum:
                        info.set(
                            type = info.children[2].type,
                            children = info.children[2].children,
                            val = info.children[2].val,
                            cgen = info.children[2].cgen)
                    else:
                        setValToAll(info.children[0], sum)
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
                        symbolT.insert_scope(Scope(table = symbolT.scopes[symbolT.current_scope_level].table))
                        analiseSemantica(item)
                        symbolT.remove()
                    else:
                        if (item.type == "var" or item.type == "conj_params"):
                        
                            if (len(item.children[0].children) > 1):
                                novo = dict()
                                novo.setdefault('type', 'int[]')
                                symbolT.insert_entry(
                                    item.children[1], novo)
                            else:
                                novo = dict()
                                novo.setdefault('type', item.children[0].children[0])
                                symbolT.insert_entry(item.children[1], novo)

                        elif (item.type == "mais_param" and len(item.children) > 1):
                            if (len(item.children[2].children) > 1):
                                novo = dict()
                                novo.setdefault('type', 'int[]')
                                symbolT.insert_entry(
                                    item.children[3], novo)
                            else:
                                novo = dict()
                                novo.setdefault('type', item.children[2].children[0])
                                symbolT.insert_entry(item.children[3], novo)

                        elif item.type == "pexp" and item.toTable != None:
                            #print(item.children[0])
                            if not (symbolT.is_in_global(item.children[item.toTable['pos']])):
                                print('Erro: Variável {0} não declarada'.format(
                                    item.children[item.toTable['pos']]))
                            atribbutes = symbolT.lookup(item.children[item.toTable['pos']])
                            item.val = atribbutes.get('val')
                        elif (item.type == "cmd2" or item.type == "cmd1") and item.toTable != None:
                            #print(item.children[0])
                            if not (symbolT.is_in_global(item.children[item.toTable['pos']])):
                                print('Erro: Variável {} não declarada'.format(
                                    item.children[item.toTable['pos']]))
                            elif item.children[2].val != None and item.children[1] != "[":
                                novo = dict()
                                novo.setdefault('val', item.children[2].val)
                                symbolT.insert_entry(
                                    item.children[item.toTable['pos']], novo)
                        analiseSemantica(item)
                    if len(info.children) == 1 and item.val:
                        info.val = item.val
                elif (item == "{"):
                    symbolT.insert_scope(Scope(table = symbolT.scopes[symbolT.current_scope_level].table))
                elif (item == "}"):
                    #print(symbolT.scopes[symbolT.current_scope_level].table)
                    symbolT.remove()
                    #print(symbolT.scopes[symbolT.current_scope_level].table)
def setValToAll(info, val):
    info.set(val = val)
    index = 0
    for item in info.children:
        if type(item) is ASTNode:  
            setValToAll(item, val)
        else:
            info.children[index] = val
    index +=1