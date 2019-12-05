def option_exps(p):
    if (p[1].cgen(p[1]) == ""):
        return p[1].cgen(p[1])
    else:
        return p[1].cgen(p[1]) + "\n" + "sw $a0 0($sp)\n" + "addiu $sp $sp -4\n"

def exps_cgen(p):
    return p[1].cgen(p[1]) + "\n" + "sw $a0 0($sp)\n" + "addiu $sp $sp -4\n"\
         + p[2].cgen(p[2])+ "sw $a0 0($sp)\n" + "addiu $sp $sp -4\n"

def conj_exps_cgen(p):
    if (len(p[1:]) == 1):
        return p[1].cgen(p[1])  
    else:
        return p[1].cgen(p[1]) + "\n" + "sw $a0 0($sp)\n" + "addiu $sp $sp -4\n" \
            + p[2].cgen(p[2]) + "\n" + "sw $a0 0($sp)\n" + "addiu $sp $sp -4\n" 
         

def empty_cgen(p):
    return "''"
    