def prog_cgen(p):
    print(p.children[0].cgen(p.children[0]) + p.children[1].cgen(p.children[1]))

 #Aqui está dando erro de NoneType, pq o cgen de cmd1 (p.children[14]) ainda n foi feito (linha 10)
def main_cgen(p):
    return p.children[1] + ":\n" +\
        "move $fp $sp\n" +\
        "sw $ra 0($sp)\n" +\
        "addiu $sp $sp -4\n" +\
        p.children[13] + "\n" +\
        "lw $ra 4($sp)\n" +\
        "addiu $sp $sp 12\n" +\
        "lw $fp 0($sp)\n" +\
        "jr $ra\n"

def conj_classes_cgen(p):
    return ''

    # if(p.children[0].type == "empty"):
    #     return p.children[0].cgen(p.children[0])
    # else:
    #     return p.children[0].cgen(p.children[0]) + p.children[1].cgen(p.children[1])

def classe_cgen(p):
    return (p.children[1] + ":        \n" +
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
    return (p.children[3] + ":        \n" +
        "move $fp $sp       \n" +
        "sw $ra 0($sp)      \n" +
        "addiu $sp $sp -4   \n" +
        p.children[6].cgen(p.children[6])+    "\n" +
        "lw $ra 4($sp)      \n" +
        "addiu $sp $sp z    \n" +
        "lw $fp 0($sp)      \n" +
        "jr $ra             \n")


############################################
def option_exps(p):
    if (p.children[0].cgen(p.children[0]) == ""):
        return p.children[0].cgen(p.children[0])
    else:
        return p.children[0].cgen(p.children[0]) + "\n" + "sw $a0 0($sp)\n" + "addiu $sp $sp -4\n"

def exps_cgen(p):
    return p.children[0].cgen(p.children[0]) + "\n" + "sw $a0 0($sp)\n" + "addiu $sp $sp -4\n"\
         + p.children[1].cgen(p.children[1])+ "sw $a0 0($sp)\n" + "addiu $sp $sp -4\n"

def conj_exps_cgen(p):
    if (len(p.children[0:]) == 1):
        return p.children[0].cgen(p.children[0])  
    else:
        return p.children[0].cgen(p.children[0]) + "\n" + "sw $a0 0($sp)\n" + "addiu $sp $sp -4\n" \
            + p.children[1].cgen(p.children[1]) + "\n" + "sw $a0 0($sp)\n" + "addiu $sp $sp -4\n" 
         

def empty_cgen(p):
    return "''"
    
