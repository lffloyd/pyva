from .symtable.symbol_table import SymbolTable, Scope
from .abstract_syntax_tree.ast_node import ASTNode

symbolT = SymbolTable()


def analiseSemantica(info, constante=0):
    global symbolT
    if(info != None and type(info) is ASTNode):
        if info.children != None:
            index = 0
            for item in info.children:
                if type(item) is ASTNode:  # TODO trocar para not
                    #if item.val != None and len(item.children):  # TODO apagar apos implementacao
                        #print(item.val)
                        #item[index].info = item.val
                        #item[index].children = []
                # else:
                    if (item.type == "class"):
                        symbolT = SymbolTable()
                        analiseSemantica(item)

                    elif (item.type == "metodo"):
                        symbolT.insert_scope(Scope())
                        analiseSemantica(item)
                        symbolT.remove()
                    else:
                        if (item.type == "mexp" ):
                            constante = 0
                        if (item.type == "aexp"):
                            if(item.val):
                                info.children[index] = item.val + constante
                                return True
                            elif len(item.children) > 1:                            
                                if(item.children[1] and item.children[2].val != None):
                                    item.children[2] = item.children[2].val
                                    if(item.children[1] == "+" ):
                                        constante = constante + item.children[2]
                                        item.children[2] = constante
                                        resp = analiseSemantica(item, constante)
                                        if resp :
                                            item.set(children = [item.children[0]])
                                        return True
                                    if(item.children[1] == "-" ):
                                        constante = constante - item.children[2]
                                        item.children[2] = constante
                                        resp = analiseSemantica(item, constante)
                                        if resp :
                                            item.set(children = [item.children[0]])
                                        return True
                                elif(item.children[1] and item.children[0].val != None):
                                    item.children[0] = item.children[0].val
                                    if(item.children[1] == "+" ):
                                        constante = constante + item.children[0]
                                        item.children[0] = constante
                                        resp = analiseSemantica(item, constante)
                                        if resp :
                                            item.set(children = [item.children[2]])
                                        return True
                                    if(item.children[1] == "-" ):
                                        constante = constante - item.children[0]
                                        item.children[0] = constante
                                        resp = analiseSemantica(item, constante)
                                        if resp :
                                            item.set(children = [item.children[2]])
                                        return True
                                    return None
                                else:
                                    return analiseSemantica(item, constante)
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
