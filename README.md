# zkSNARK_QAP

## Presentation

this code is a simple implementation of Quadratics Arithmetics Program (https://medium.com/@VitalikButerin/quadratic-arithmetic-programs-from-zero-to-hero-f6d558cea649)

this program creates a basic commitment to the following function:

func Verify (a int, b int) {
	 return a^3 * 2b - 5
}

the program has 3 CLI commands:
    - `export` Export R1CS
    - `prove` Generate proof with exported R1CS from `export` that accepts a, b`
    - `verify` Verify proof


## How to start

Start the program with: \
-python main.py export\
(this will create a r1cs.txt file containing the R1CS)\
-then you can try the other command with: python main.py <file_name> prove < a > < b >\
(file name should refer to a file containing the r1cs)\
-finally try the verify command with:  python main.py < file_name > prove < a > < b > verify


## Security problems

Note that this approach isn't secure because the function "Verify" is relatively simple so it could be cracked easily\
Also If the verifier want has access to the vector s such that s.A(x) * s.B(x) - s.c(x) % Z(x) = 0 he can guess the secret value of the input (a,b)\
If (a,b) needs to be kept secret, we should not send it directly in command line like that ! we need to encode it first__


note :
the code for flattening is taken from : 
https://github.com/ethereum/research/blob/master/zksnark/code_to_r1cs.py


Aziz Kanoun

