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
        if info.children != None:
            index = 0
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
                        if (item.type == "mexp" ):
                            sum = 0
                            if(item.val):
                                info.children[index] =item.val * mult
                                return ReturnType.total
                            elif len(item.children) > 1:                            
                                if(item.children[1] and item.children[2].val != None):                                    
                                    item.children[2] = item.children[2].val
                                    if(item.children[1] == "*" ):
                                        mult = mult * item.children[2]
                                        item.children[2] = mult
                                        resp = analiseSemantica(item, mult=mult)
                                        if resp == ReturnType.partialMult:
                                            item.set(children = [item.children[0]])
                                        return ReturnType.partialMult
                                elif(item.children[1] and item.children[0].val != None):
                                    print("val3: " + str(item.children[0].val))
                                    
                                    item.children[0] = item.children[0].val
                                    if(item.children[1] == "*" ):
                                        mult = mult * item.children[0]
                                        print("mult3: "+ str(mult))
                                        item.children[0] = mult
                                        resp = analiseSemantica(item, mult=mult)
                                        if resp == ReturnType.partialMult:
                                            item.set(children = [item.children[2]])
                                        return ReturnType.partialMult
                                else:
                                    analiseSemantica(item, mult=mult)
                                    return ReturnType.no
                        elif (item.type == "aexp"):
                            mult = 1
                            if(item.val):
                                
                                #sexp = ASTNode(type="sexp", children=[item.val + sum], val=item.val + sum)
                                #mexp = ASTNode(type="mexp", children=[sexp], val=sexp.val)
                                #info.children[index] = mexp
                                #print(info.children[0].children[0].val)
                                info.children[index] =item.val + sum
                                return ReturnType.total
                            elif len(item.children) > 1:                            
                                if(item.children[1] and item.children[2].val != None):
                                    item.children[2] = item.children[2].val
                                    if(item.children[1] == "+" ):
                                        sum = sum + item.children[2]
                                        item.children[2] = sum
                                        resp = analiseSemantica(item, sum)
                                        if resp == ReturnType.partialSum:
                                            item.set(children = [item.children[0]])
                                        return ReturnType.partialSum
                                    if(item.children[1] == "-" ):
                                        sum = sum - item.children[2]
                                        item.children[2] = sum
                                        resp = analiseSemantica(item, sum)
                                        if resp == ReturnType.partialSum:
                                            item.set(children = [item.children[0]])
                                        return ReturnType.partialSum
                                elif(item.children[1] and item.children[0].val != None):
                                    item.children[0] = item.children[0].val
                                    if(item.children[1] == "+" ):
                                        sum = sum + item.children[0]
                                        item.children[0] = sum
                                        resp = analiseSemantica(item, sum)
                                        if resp == ReturnType.partialSum:
                                            item.set(children = [item.children[2]])
                                        return ReturnType.partialSum
                                    if(item.children[1] == "-" ):
                                        sum = sum - item.children[0]
                                        item.children[0] = sum
                                        resp = analiseSemantica(item, sum)
                                        if resp == ReturnType.partialSum:
                                            item.set(children = [item.children[2]])
                                        return ReturnType.partialSum
                                else:
                                    analiseSemantica(item, sum)
                                    return ReturnType.no
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
                index += 1
