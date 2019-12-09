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
                ##Se o ultimo termo for uma variavel a analise semantica vai transforma-lo em uma constante
                #não chamar a analise do termo no inicio pode resoltar em um calculo incompleto com esse termo sobrando
                #no final (ex: 3*x*2*y -> 6*x*y com y.val =2)
                analiseSemantica(info.children[2])
                #Se um dos termos é constante a função propaga a constante para dentro do outro termo
                #  que apos ser analisado retorna se essa constante foi usada e pode ser descartada                          
                if(info.children[1] == "*"  and info.children[2].val != None):                     
                    mult = mult * info.children[2].val
                    resp = analiseSemantica(info.children[0], mult = mult)
                    if resp == ReturnType.partialMult:
                        #Como a constante ja foi propagada dentro do outro termo ela não precisa mais estar na arvore
                        info.set(
                            type = info.children[0].type,
                            children = info.children[0].children,
                            val = info.children[0].val,
                            cgen = info.children[0].cgen)
                    #Caso na analise do termo não constante tenha se verificado uma variavel
                    # com valor na tabela e o termo tenha passado a ser constante a operacao é realizada
                    elif info.children[0].val != None:
                        mult = mult * info.children[0].val
                        setValToAll(info.children[2], mult)
                        info.set(
                            type = info.children[2].type,
                            children = info.children[2].children,
                            val = info.children[2].val,
                            cgen = info.children[2].cgen)
                    else:
                        #Caso seja a ultima constante da subarvore info que pode ser utilizada na operacao ela recebe todo o valor
                        setValToAll(info.children[2], mult)
                    return ReturnType.partialMult
                elif(info.children[1] == "*"  and info.children[0].val != None):                              
                    mult = mult * info.children[0].val
                    resp = analiseSemantica(info.children[2], mult = mult)
                    if resp == ReturnType.partialMult:
                        #Como a constante ja foi propagada dentro do outro termo ela não precisa mais estar na arvore
                        info.set(
                            type = info.children[2].type,
                            children = info.children[2].children,
                            val = info.children[2].val,
                            cgen = info.children[2].cgen)
                    #Caso na analise do termo não constante tenha se verificado uma variavel
                    # com valor na tabela e o termo tenha passado a ser constante a operacao é realizada
                    elif info.children[2].val != None:
                        mult = mult * info.children[2].val
                        setValToAll(info.children[0], mult)
                        info.set(
                            type = info.children[0].type,
                            children = info.children[0].children,
                            val = info.children[0].val,
                            cgen = info.children[0].cgen)
                    else:
                        #Caso seja a ultima constante da subarvore info que pode ser utilizada na operacao ela recebe todo o valor
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
                ##Se o ultimo termo for uma variavel a analise semantica vai transforma-lo em uma constante
                #não chamar a analise do termo no inicio pode resoltar em um calculo incompleto com esse termo sobrando
                #no final (ex: 3+ x + 3 + y -> 6 + x + y com y.val =2)
                analiseSemantica(info.children[2])
                #Se um dos termos é constante a função propaga a constante para dentro do outro termo
                #  que apos ser analisado retorna se essa constante foi usada e pode ser descartada                                
                if(info.children[1] and info.children[2].val != None):
                    if(info.children[1] == "+" ):
                        sum = sum + info.children[2].val
                    if(info.children[1] == "-" ):
                        sum = sum - info.children[2].val
                    resp = analiseSemantica(info.children[0], sum)
                    if resp == ReturnType.partialSum:
                        #Como a constante ja foi propagada dentro do outro termo ela não precisa mais estar na arvore
                        info.set(
                            type = info.children[0].type,
                            children = info.children[0].children,
                            val = info.children[0].val,
                            cgen = info.children[0].cgen)
                    #Caso na analise do termo não constante tenha se verificado uma variavel
                    # com valor na tabela e o termo tenha passado a ser constante a operacao é realizada
                    elif info.children[0].val != None:
                        #Se for uma subtração o valor ja ficou negativo, subtrair transforaria a operacao em soma
                        sum = sum + info.children[0].val
                        setValToAll(info.children[2], sum)
                        info.set(
                            type = info.children[2].type,
                            children = info.children[2].children,
                            val = info.children[2].val,
                            cgen = info.children[2].cgen)
                    else:
                        #Caso seja a ultima constante da subarvore info que pode ser utilizada na operacao ela recebe todo o valor
                        setValToAll(info.children[2], sum)
                    return ReturnType.partialSum
                elif(info.children[1] and info.children[0].val != None):
                    if(info.children[1] == "+" ):
                        sum = sum + info.children[0].val
                    if(info.children[1] == "-" ):
                        sum = info.children[0].val - sum
                    resp = analiseSemantica(info.children[2], sum)
                    if resp == ReturnType.partialSum:
                        #Como a constante ja foi propagada dentro do outro termo ela não precisa mais estar na arvore
                        info.set(
                            type = info.children[2].type,
                            children = info.children[2].children,
                            val = info.children[2].val,
                            cgen = info.children[2].cgen)
                    #Caso na analise do termo não constante tenha se verificado uma variavel
                    # com valor na tabela e o termo tenha passado a ser constante a operacao é realizada
                    elif info.children[2].val != None:
                        #Se for uma subtração o valor ja ficou negativo, subtrair transforaria a operacao em soma
                        sum = sum + info.children[2].val
                        setValToAll(info.children[0], sum)
                        info.set(
                            type = info.children[0].type,
                            children = info.children[0].children,
                            val = info.children[0].val,
                            cgen = info.children[0].cgen)
                    else:
                        #Caso seja a ultima constante da subarvore info que pode ser utilizada na operacao ela recebe todo o valor
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
                    elif (item.type == "cmd2" or item.type == "cmd1") and item.toTable != None:
                        analiseSemantica(item)
                        if not (symbolT.is_in_global(item.children[item.toTable['pos']])):
                            print('Erro: Variável {} não declarada'.format(
                                item.children[item.toTable['pos']]))
                        elif item.children[2].val != None and item.children[1] != "[":
                            novo = dict()
                            novo.setdefault('val', item.children[2].val)
                            symbolT.insert_entry(
                                item.children[item.toTable['pos']], novo)
                        #Propagando valor para nos superiores na arvore caso so tenha um filho e a analise dele tenha atribuido valor
                        if len(info.children) == 1 and item.val:
                            info.val = item.val
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
                            if not (symbolT.is_in_global(item.children[item.toTable['pos']])):
                                raise Exception('Erro: Variável {0} não declarada'.format(
                                    item.children[item.toTable['pos']]))
                            atribbutes = symbolT.lookup(item.children[item.toTable['pos']])
                            if atribbutes:
                                item.val = atribbutes.get('val')
                        analiseSemantica(item)
                    #Propagando valor para nos superiores na arvore caso so tenha um filho e a analise dele tenha atribuido valor
                    if len(info.children) == 1 and item.val:
                        info.val = item.val
                #Necessario a criação de um novo escopo pois dentro de um if, else, while etc podem ser atribuidos valores
                #para variaveis que não podem ser utilizados fora. Ao sair do escopo ele é deletado da pilha
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