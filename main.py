from to_r1cs import *
from r1cs_to_QAP import *
import sys
import os.path


def main():
    code_to_flat="""def add(a, b):
                        return a**3 * 2*b - 5
        """
    inputs, body = extract_inputs_and_body(parse(code_to_flat))
    nbr_of_inputs=len(inputs)
    flatcode = flatten_body(body)
    index_of,nbr_of_dummy=generate_index_of(inputs,flatcode)
    size_of_s=nbr_of_inputs+nbr_of_dummy+2
    nbr_arg=len(sys.argv)
    list_args=str(sys.argv)
    if(nbr_arg==2 and sys.argv[1]=="export"):       
        export_r1cs(flatcode,size_of_s,index_of)
        print()
        print("r1cs exported in r1cs.txt")
        print("****************************************")
    elif(nbr_arg ==5 and sys.argv[1]=="prove"):
        a=sys.argv[3]
        b=sys.argv[4]
        if(os.path.exists(sys.argv[2])==False or a.isnumeric()== False or b.isnumeric()==False):
            print(" a or b format is incorrect or file does not exist")
        else:
            s,polynoms,t=generate_proof(sys.argv[2],int(a),int(b))
    elif(nbr_arg ==6 and sys.argv[1]=="prove" and sys.argv[5]=="verify"):
        a=sys.argv[3]
        b=sys.argv[4]
        if(os.path.exists(sys.argv[2])==False or a.isnumeric()== False or b.isnumeric()==False):
            print(" a or b format is incorrect or file does not exist")
        else:
            s,polynoms,t=generate_proof(sys.argv[2],int(a),int(b))
            print()
            print(" **************** V E R I F I C A T I O N **************")
            print()
            verify_proof(s,polynoms,nbr_of_dummy+1)
    else:
        print("-please verify arguments format")
        print("-make sure to call export before prove")
        print("-make sure to call prove before verify")

if __name__ == "__main__":
    main()
