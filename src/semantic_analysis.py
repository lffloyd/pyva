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
            if(info.val):
                return ReturnType.total
            elif len(info.children) > 1:
                #Se um dos termos é constante a função propaga a constante para dentro do outro termo
                #  que apos ser analisado retorna se essa constante foi usada e pode ser descartada                          
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
                        setValToAll(info.children[2], mult)
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
                        setValToAll(info.children[0], mult)
                    return ReturnType.partialMult
                else:
                    #Necessario pois caso não exista constante nos termos eles ainda precisam ser analisados semanticamente
                    resp = analiseSemantica(info.children[0], mult = mult)
                    if resp == ReturnType.partialMult:
                        analiseSemantica(info.children[2])
                        #Esse retorno é importante para quando existem constantes intercaladas (ex.: 3*x*2*y*4)
                        #pois nesse caso sempre existe uma operacao sem constantes no meio
                        return ReturnType.partialMult
                    else:
                        return analiseSemantica(info.children[2], mult = mult)

        elif (info.type == "aexp"):
            if(info.val):
                return ReturnType.total
            elif len(info.children) > 1:
                #Se um dos termos é constante a função propaga a constante para dentro do outro termo
                #  que apos ser analisado retorna se essa constante foi usada e pode ser descartada                                
                if(info.children[1] and info.children[2].val != None):
                    if(info.children[1] == "+" ):
                        sum = sum + info.children[2].val
                    if(info.children[1] == "-" ):
                        sum = sum - info.children[2].val
                    resp = analiseSemantica(info.children[0], sum)
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
                    return ReturnType.partialSum
                else:
                    #Necessario pois caso não exista constante nos termos eles ainda precisam ser analisados semanticamente
                    resp = analiseSemantica(info.children[0], sum = sum)
                    if resp == ReturnType.partialSum:
                        analiseSemantica(info.children[2])
                        #Esse retorno é importante para quando existem constantes intercaladas (ex.: 3+x+2+y+4)
                        #pois nesse caso sempre existe uma operacao sem constantes no meio
                        return ReturnType.partialSum
                    else:
                        return analiseSemantica(info.children[2], sum = sum)
        if info.children != None:
            for item in info.children:
                if type(item) is ASTNode:  
                    if (item.type == "class"):
                        #Limpando a tabela de simbolos
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
                    #Propagando valor para nos superiores na arvore caso so tenha um filho e a analise dele tenha atribuido valor
                    if len(info.children) == 1 and item.val:
                        info.val = item.val
                elif (item == "{"):
                    symbolT.insert_scope(Scope(table = symbolT.scopes[symbolT.current_scope_level].table))
                elif (item == "}"):
                    symbolT.remove()

def setValToAll(info, val):
    info.set(val = val)
    index = 0
    for item in info.children:
        if type(item) is ASTNode:  
            setValToAll(item, val)
        else:
            info.children[index] = val
    index +=1