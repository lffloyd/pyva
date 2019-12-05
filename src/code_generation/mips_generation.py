def prog_cgen(p):
    print(p[1].cgen(p[1]) + p[2].cgen(p[2]))

def main_cgen(p):
    return (p[2] + ":        \n" +
        "move $fp $sp       \n" +
        "sw $ra 0($sp)      \n" +
        "addiu $sp $sp -4   \n" +
        p[12].cgen(p[12]) + "\n" +
        "lw $ra 4($sp)      \n" +
        "addiu $sp $sp 12    \n" +
        "lw $fp 0($sp)      \n" +
        "jr $ra             \n")

def conj_classes_cgen(p):
    if(p[1].type == "empty"):
        return p[1].cgen(p[1])
    else:
        return p[1].cgen(p[1]) + p[2].cgen(p[2])

def classe_cgen(p):
    return (p[2] + ":        \n" +
        "move $fp $sp       \n" +
        "sw $ra 0($sp)      \n" +
        "addiu $sp $sp -4   \n" +
        p[6].cgen(p[6])+    "\n" +
        "lw $ra 4($sp)      \n" +
        "addiu $sp $sp z    \n" +
        "lw $fp 0($sp)      \n" +
        "jr $ra             \n")

def extension_cgen(p):
    if(p[1].type == "empty"):
        return p[1].cgen(p[1])
    else:
        return ""

def conj_var_cgen(p):
    if(p[1].type == "empty"):
        return p[1].cgen(p[1])
    else:
        return ""

def conj_metodos_cgen(p):
    if(p[1].type == "empty"):
        return p[1].cgen(p[1])
    else:
        return p[1].cgen(p[1]) + p[2].cgen(p[2])

def var_cgen(p):
    return ""

def metodo_cgen(p):
    return (p[3] + ":        \n" +
        "move $fp $sp       \n" +
        "sw $ra 0($sp)      \n" +
        "addiu $sp $sp -4   \n" +
        p[6].cgen(p[6])+    "\n" +
        "lw $ra 4($sp)      \n" +
        "addiu $sp $sp z    \n" +
        "lw $fp 0($sp)      \n" +
        "jr $ra             \n")