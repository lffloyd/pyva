# Code generation information

## Registers

* Return register: ```$v0``` - used to return values from function/method calls
* Activation registry: ```$ra```
* Frame pointer: ```$fp```
* Stack pointer: ```$sp```
* Accumulator: ```$a0```
* Temporary registers: ```$t0, $t1, ..., $tn```

## Allocation sizes

* Integer (number): 4 bytes
* String (used only for the static 'main' method declaration): 40 bytes

## Additional links

* [Oracle Java information about numeric types sizes](https://docs.oracle.com/cd/E19253-01/817-6223/chp-typeopexpr-2/index.html) - official Oracle docs
* [Online C Compiler to MIPS Assembly](https://godbolt.org) - used as a translator example
* [MIPS instruction set reference](http://www.mrc.uidaho.edu/mrc/people/jff/digital/MIPSir.html) - reference for the various instructions used