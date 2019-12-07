from enum import Enum
from re import match

token = {
    'BOOLEAN': r'boolean',
    'CLASS': r'class',
    'EXTENDS': r'extends',
    'PUBLIC': r'public',
    'STATIC': r'static',
    'VOID': r'void',
    'MAIN': r'main',
    'STRING': r'String',
    'RETURN': r'return',
    'INT': r'int',
    'IF': r'if',
    'ELSE': r'else',
    'WHILE': r'while',
    'SYSTEMOUTPRINTLN': r'System.out.println',
    'LENGTH': r'length',
    'TRUE': r'true',
    'FALSE': r'false',
    'THIS': r'this',
    'NEW': r'new',
    'NULL': r'null',
    'LKEY': r'{',
    'RKEY': r'}'
}

if_count = 0
true_branch_count = 0
false_branch_count = 0
loop_count = 0
equals_count = 0
not_equals_count = 0
not_count = 0

def get_next_if_count():
    global if_count
    if_count = if_count + 1
    return if_count

def get_next_true_branch_count():
    global true_branch_count
    true_branch_count = true_branch_count + 1
    return true_branch_count

def get_next_false_branch_count():
    global false_branch_count
    false_branch_count = false_branch_count + 1
    return false_branch_count

def get_next_loop_count():
    global loop_count
    loop_count = loop_count + 1
    return loop_count

def get_next_equals_count():
    global equals_count
    equals_count = equals_count + 1
    return equals_count

def get_next_not_equals_count():
    global not_equals_count
    not_equals_count = not_equals_count + 1
    return not_equals_count

def get_next_not_count():
    global not_count
    not_count = not_count + 1
    return not_count


def prog_cgen(p):
    if p.val != None:
        return load_immediate(p.val)

    return p.children[0].cgen(p.children[0]) + p.children[1].cgen(p.children[1])

 #Aqui está dando erro de NoneType, pq o cgen de cmd1 (p.children[14]) ainda n foi feito (linha 10)
#This function calls cgen(cmd1)
def main_cgen(p):
    if p.val != None:
        return load_immediate(p.val)

    return p.children[1] + ":" + "\n" +\
        "\tmove $fp $sp\n" +\
        "\tsw $ra 0($sp)\n" +\
        "\taddiu $sp $sp -40\n" +\
        p.children[14].cgen(p.children[14]) +\
        "\tlw $ra 40($sp)\n" +\
        "\taddiu $sp $sp 40\n" +\
        "\tlw $fp 0($sp)\n" +\
        "\tjr $ra\n"

def cmd1_gen(p):
    if p.val != None:
        return load_immediate(p.val)
    
    children = p.children

    if match(token['LKEY'], children[0]):
        return children[1].cgen(children[1])

    if match(token['WHILE'], children[0]):
        return while_expression(children)

    if match(token['IF'], children[0]):
        if match(token['ELSE'], children[5]):
            return if_else_expression(children)
        return if_expression(children)
    
    if match(token['SYSTEMOUTPRINTLN'], children[0]):
        return children[2].cgen(children[2]) + \
                "\tjal System.out.println\n"

def cmd2_gen(p):
    if p.val != None:
        return load_immediate(p.val)
    
    children = p.children

    if match(token['LKEY'], children[0]):
        return children[1].cgen(children[1])

    if match(token['WHILE'], children[0]):
        return while_expression(children)

    if match(token['IF'], children[0]) and match(token['ELSE'], children[5]):
        return if_else_expression(children)
    
    if match(token['SYSTEMOUTPRINTLN'], children[0]):
        return children[2].cgen(children[2]) + \
                "\tjal System.out.println\n"

def conj_cmd_cgen(p):
    if p.val != None:
        return load_immediate(p.val)

    children = p.children

    if len(children) == 1:
        return children[0].cgen(children[0])

    return children[0].cgen(children[0]) + children[1].cgen(children[1])

def exp_and_cgen(p):
    if p.val != None:
        return load_immediate(p.val)

    children = p.children

    return children[0].cgen(children[0]) + \
            "\tsw $a0 0($sp)\n" + \
            "\taddiu $sp $sp -4\n" + \
            children[2].cgen(children[2]) + \
            "\tlw $t1 4($sp)\n" + \
            "\taddiu $sp $sp 4\n" + \
            "\tand $a0 $a0 $t1\n"

def rexp_lthan_cgen(p):
    if p.val != None:
        return load_immediate(p.val)

    children = p.children

    return children[0].cgen(children[0]) + \
            "\tsw $a0 0($sp)\n" + \
            "\taddiu $sp $sp -4\n" + \
            children[2].cgen(children[2]) + \
            "\tlw $t1 4($sp)\n" + \
            "\taddiu $sp $sp 4\n" + \
            "\tslt $a0 $t1 $a0\n"

def rexp_equals_cgen(p):
    if p.val != None:
        return load_immediate(p.val)

    children = p.children

    eq_count = str(get_next_equals_count())

    return children[0].cgen(children[0]) + \
            "\tsw $a0 0($sp)\n" + \
            "\taddiu $sp $sp -4\n" + \
            children[2].cgen(children[2]) + \
            "\tlw $t1 4($sp)\n" + \
            "\taddiu $sp $sp 4\n" + \
            "\tsub $a0 $t1 $a0\n" + \
            "\tbeq $a0 $0 equals" + eq_count + \
            "not_equals" + eq_count + ":" + \
            "\tli $a0 0\n" + \
            "\tb end_equality" + eq_count + "\n" + \
            "equals" + eq_count + ":" + \
            "\tli $a0 1" + \
            "end_equality" + eq_count + ":\n"

def rexp_nequals_cgen(p):
    if p.val != None:
        return load_immediate(p.val)

    children = p.children

    neq_count = str(get_next_not_equals_count())

    return children[0].cgen(children[0]) + \
            "\tsw $a0 0($sp)\n" + \
            "\taddiu $sp $sp -4\n" + \
            children[2].cgen(children[2]) + \
            "\tlw $t1 4($sp)\n" + \
            "\taddiu $sp $sp 4\n" + \
            "\tsub $a0 $t1 $a0\n" + \
            "\tbne $a0 $0 not_equals" + neq_count + \
            "equals" + neq_count + ":" + \
            "\tli $a0 0\n" + \
            "\tb end_not_equality" + neq_count + "\n" + \
            "not_equals" + neq_count + ":" + \
            "\tli $a0 1" + \
            "end_not_equality" + neq_count + ":\n"

def aexp_minus_cgen(p):
    if p.val != None:
        return load_immediate(p.val)

    children = p.children

    return children[0].cgen(children[0]) + \
            "\tsw $a0 0($sp)\n" + \
            "\taddiu $sp $sp -4\n" + \
            children[2].cgen(children[2]) + \
            "\tlw $t1 4($sp)\n" + \
            "\taddiu $sp $sp 4\n" + \
            "\tsub $a0 $t1 $a0\n"

def aexp_plus_cgen(p):
    if p.val != None:
        return load_immediate(p.val)

    children = p.children

    return children[0].cgen(children[0]) + \
            "\tsw $a0 0($sp)\n" + \
            "\taddiu $sp $sp -4\n" + \
            children[2].cgen(children[2]) + \
            "\tlw $t1 4($sp)\n" + \
            "\taddiu $sp $sp 4\n" + \
            "\tadd $a0 $t1 $a0\n"

def mexp_times_cgen(p):
    if p.val != None:
        return load_immediate(p.val)

    children = p.children

    return children[0].cgen(children[0]) + \
            "\tsw $a0 0($sp)\n" + \
            "\taddiu $sp $sp -4\n" + \
            children[2].cgen(children[2]) + \
            "\tlw $t1 4($sp)\n" + \
            "\taddiu $sp $sp 4\n" + \
            "\tmult $a0 $t1\n" + \
            "\tmflo $a0\n"

def sexp_cgen(p):
    if p.val != None:
        return load_immediate(p.val)
    
    children = p.children

    if match(token['NEW'], children[0]):
        return children[3].cgen(children[3]) + \
                "\tadd $sp $sp -$a0\n"

    if match(token['DOT'], children[1]):
        return ""

    if match(token['LBRACKET'], children[1]):
        return children[2].cgen(children[2]) + \
                "\tadd $sp $sp -$a0\n" + \
                children[0].cgen(children[0]) + \
                "\tadd $sp $sp $a0\n"

def sexp_not_cgent(p):
    if p.val != None:
        return load_immediate(p.val)
    
    children = p.children

    nt_count = str(get_next_not_count())

    return children[1].cgen(children[1]) + \
            "\tbgtz $a0 not_one_branch" + nt_count + "\n" + \
            "not_zero_branch" + nt_count + ":\n" + \
            "\tli $a0 1\n" + \
            "\t b end_not_branch" + nt_count + "\n" + \
            "not_one_branch" + nt_count + ":\n" + \
            "\tli $a0 0\n" + \
            "end_not_branch" + nt_count + ":\n"

def sexp_minus_cgen(p):
    if p.val != None:
        return load_immediate(p.val)

    children = p.children

    return children[1].cgen(children[1]) + \
            "\tsub $a0 $0 $a0\n"

def sexp_terminal_cgen(p):
    converted_value = 0 if (match(token['NULL'], p.val) 
                        or match(token['FALSE'], p.val)) \
                        else 1
    return load_immediate(converted_value)

def exps_cgen(p):
    if p.val != None:
        return load_immediate(p.val)

    children = p.children

    return children[0].cgen(children[0]) + children[1].cgen(children[1])

def generic_recursive_cgen(p):
    if p.val != None:
        return load_immediate(p.val)

    children = p.children

    return children[0].cgen(children[0])


#############################################################################################################
###Esse trecho não está sendo utilizado no momento, mas acho que poderemos reaproveitar
def conj_classes_cgen(p):
    return ""

    # if(p.children[0].type == "empty"):
    #     return p.children[0].cgen(p.children[0])
    # else:
    #     return p.children[0].cgen(p.children[0]) + p.children[1].cgen(p.children[1])

def classe_cgen(p):
    return (p.children[1] + ":" + "\n" +
        "move $fp $sp       \n" +
        "sw $ra 0($sp)      \n" +
        "addiu $sp $sp -4   \n" +
        p.children[6].cgen(p.children[6])+    "\n" +
        "lw $ra 4($sp)      \n" +
        "addiu $sp $sp z    \n" +
        "lw $fp 0($sp)      \n" +
        "jr $ra             \n")

def extension_cgen(p):
    if(p.children[0].type == "empty"):
        return p.children[0].cgen(p.children[0])
    else:
        return ""

def conj_var_cgen(p):
    if(p.children[0].type == "empty"):
        return p.children[0].cgen(p.children[0])
    else:
        return ""

def conj_metodos_cgen(p):
    if(p.children[0].type == "empty"):
        return p.children[0].cgen(p.children[0])
    else:
        return p.children[0].cgen(p.children[0]) + p.children[1].cgen(p.children[1])

def var_cgen(p):
    return ""

def metodo_cgen(p):
    return (p.children[3] + ":" + "\n" +
        "move $fp $sp       \n" +
        "sw $ra 0($sp)      \n" +
        "addiu $sp $sp -4   \n" +
        p.children[6].cgen(p.children[6])+    "\n" +
        "lw $ra 4($sp)      \n" +
        "addiu $sp $sp z    \n" +
        "lw $fp 0($sp)      \n" +
        "jr $ra             \n")

def option_exps(p):
    if (p.children[0].cgen(p.children[0]) == ""):
        return p.children[0].cgen(p.children[0])
    else:
        return p.children[0].cgen(p.children[0]) + "\n" + "sw $a0 0($sp)\n" + "addiu $sp $sp -4\n"

def conj_exps_cgen(p):
    if (len(p.children) == 1):
        return p.children[0].cgen(p.children[0])  
    else:
        return p.children[0].cgen(p.children[0]) + "\n" + "sw $a0 0($sp)\n" + "addiu $sp $sp -4\n" \
            + p.children[1].cgen(p.children[1]) + "\n" + "sw $a0 0($sp)\n" + "addiu $sp $sp -4\n" 
         

#########################################################################################################

def empty_cgen(p):
    return ""

def load_immediate(val):
    return "\tli $a0 " + str(val) + "\n"

def if_expression(exp):
    tb_count = str(get_next_true_branch_count())
    if_count = str(get_next_if_count()) 

    return exp[2].cgen(exp[2]) + "\n" + \
            "\tbgtz $a0 true_branch" + tb_count + "\n" + \
            "true_branch" + tb_count + ":\n" + \
            "\t" + exp[4].cgen(exp[4]) + \
            "end_if" + if_count + ":\n"

def if_else_expression(exp):
    tb_count = str(get_next_true_branch_count())
    fb_count = str(get_next_false_branch_count())
    if_count = str(get_next_if_count()) 

    return exp[2].cgen(exp[2]) + "\n" + \
            "\tbgtz $a0 true_branch" + tb_count + "\n" + \
            "false_branch" + fb_count + ":\n" + \
            exp[6].cgen(exp[6]) + \
            "\tb end_if" + if_count + "\n" + \
            "true_branch" + tb_count + ":\n" + \
            exp[4].cgen(exp[4]) + \
            "end_if" + if_count + ":\n"

def while_expression(exp):
    lp_count = str(get_next_loop_count())

    return exp[2].cgen(exp[2]) + "\n" + \
            "loop" + lp_count + ":\n" + \
            "\tbeq $a0 $0 end_loop\n" + \
            exp[4].cgen(exp[4])
