class Factorial { 
    public static void main(String[] a) { 
        System.out.println(new Fac().ComputeFac(10));
    }
}

class Fac {
    int aaa;
    public int ComputeFac(int num,int ottt) {
        int num_aux;
        int statica;
        if (num < 1){
            num_aux = 1;
            //aaa = 3;
        }
        else{
            statica = 2;
            num_aux = 5 + 3*this.ComputeFac(statica - 1)*5*(3+statica+1+num_aux)*statica*statica + 2 + statica;
        }            
        return num_aux;
    }
    /* public int ComputeFac2(int num) {
        int num_aux;
        int statica;
        if (num < 1)
            num_aux = 1;
        else
            num_aux = 3 + (this.ComputeFac(num - 1)) + 3 + 5;
        return num_auxx;
    } */
}