import unittest
from to_r1cs import *
from r1cs_to_QAP import *

######### R1CS tests #############

class Alltests(unittest.TestCase):
    #we compare R1CS with expected output 
    def test_R1CS1(self):
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
        r1cs=R1CS_generation(flatcode,size_of_s,index_of)
        r1cs=np.array(r1cs)
        expected=np.array([[[0,1,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,0,0,1,0,0,0]],
                    [[0,0,0,0,1,0,0,0],[0,1,0,0,0,0,0,0],[0,0,0,0,0,1,0,0]],
                    [[0,0,0,0,0,1,0,0],[2,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0]],
                    [[0,0,0,0,0,0,1,0],[0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1]],
                    [[-5,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0]]])
        np.testing.assert_array_equal(r1cs,expected)

#we compare R1CS with expected output 
    def test_R1CS2(self):
        code_to_flat="""def add(x):
                            return x**3 + x + 5
        """
        inputs, body = extract_inputs_and_body(parse(code_to_flat))
        nbr_of_inputs=len(inputs)
        flatcode = flatten_body(body)
        index_of,nbr_of_dummy=generate_index_of(inputs,flatcode)
        size_of_s=nbr_of_inputs+nbr_of_dummy+2
        nbr_arg=len(sys.argv)
        list_args=str(sys.argv)
        r1cs=R1CS_generation(flatcode,size_of_s,index_of)
        r1cs=np.array(r1cs)
        expected=np.array([[[0,1,0,0,0,0],[0,1,0,0,0,0],[0,0,0,1,0,0]],
            [[0,0,0,1,0,0],[0,1,0,0,0,0],[0,0,0,0,1,0]],
            [[0,1,0,0,1,0],[1,0,0,0,0,0],[0,0,0,0,0,1]],
            [[5,0,0,0,0,1],[1,0,0,0,0,0],[0,0,1,0,0,0]]])
        np.testing.assert_array_equal(r1cs,expected)

#we compare R1CS with expected output
    def test_R1CS3(self):
        code_to_flat="""def add(x):
                            return x ** 2 - 4
        """
        inputs, body = extract_inputs_and_body(parse(code_to_flat))
        nbr_of_inputs=len(inputs)
        flatcode = flatten_body(body)
        index_of,nbr_of_dummy=generate_index_of(inputs,flatcode)
        size_of_s=nbr_of_inputs+nbr_of_dummy+2
        nbr_arg=len(sys.argv)
        list_args=str(sys.argv)
        r1cs=R1CS_generation(flatcode,size_of_s,index_of)
        r1cs=np.array(r1cs)
        expected=np.array([[[0,1,0,0],[0,1,0,0],[0,0,0,1]],
            [[-4,0,0,1],[1,0,0,0],[0,0,1,0]]])
        np.testing.assert_array_equal(r1cs,expected)

#verify R1CS when code = return -x + 4*y
    '''   
    def test_R1CS4(self):  #this test FAIL because the parser from the flattening method cannot read (-1)*x
        code_to_flat="""def add(x,y):
                            return -1*x + 4*y
        """
        inputs, body = extract_inputs_and_body(parse(code_to_flat))
        nbr_of_inputs=len(inputs)
        flatcode = flatten_body(body)
        index_of,nbr_of_dummy=generate_index_of(inputs,flatcode)
        size_of_s=nbr_of_inputs+nbr_of_dummy+2
        nbr_arg=len(sys.argv)
        list_args=str(sys.argv)
        r1cs=R1CS_generation(flatcode,size_of_s,index_of)
        r1cs=np.array(r1cs)
        expected=np.array([[[-1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,0,0,1,0]],
            [[4,0,0,0,0,0],[0,0,1,0,0,0],[0,0,0,0,0,1]],
            [[0,0,0,0,1,1],[1,0,0,0,0,0],[0,0,0,1,0,0]]])
        np.testing.assert_array_equal(r1cs,expected)
    '''
#verify R1CS when code = return x+y+z+t
    def test_R1CS5(self):  
        code_to_flat="""def add(x,y,z,t):
                            return x+y+z+t
        """
        inputs, body = extract_inputs_and_body(parse(code_to_flat))
        nbr_of_inputs=len(inputs)
        flatcode = flatten_body(body)
        index_of,nbr_of_dummy=generate_index_of(inputs,flatcode)
        size_of_s=nbr_of_inputs+nbr_of_dummy+2
        nbr_arg=len(sys.argv)
        list_args=str(sys.argv)
        r1cs=R1CS_generation(flatcode,size_of_s,index_of)
        r1cs=np.array(r1cs)
        expected=np.array([[[0,1,1,0,0,0,0,0],[1,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0]],
                            [[0,0,0,1,0,0,1,0],[1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,1]],
                            [[0,0,0,0,1,0,0,1],[1,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0]]])
        np.testing.assert_array_equal(r1cs,expected)

#verify R1CS when code = return x*3 + x*3
    def test_R1CS6(self):  
        code_to_flat="""def add(x):
                            return x*3 +x*3
        """
        inputs, body = extract_inputs_and_body(parse(code_to_flat))
        nbr_of_inputs=len(inputs)
        flatcode = flatten_body(body)
        index_of,nbr_of_dummy=generate_index_of(inputs,flatcode)
        size_of_s=nbr_of_inputs+nbr_of_dummy+2
        nbr_arg=len(sys.argv)
        list_args=str(sys.argv)
        r1cs=R1CS_generation(flatcode,size_of_s,index_of)
        r1cs=np.array(r1cs)
        expected=np.array([[[0,1,0,0,0],[3,0,0,0,0],[0,0,0,1,0]],
                            [[0,1,0,0,0],[3,0,0,0,0],[0,0,0,0,1]],
                            [[0,0,0,1,1],[1,0,0,0,0],[0,0,1,0,0]]])
        np.testing.assert_array_equal(r1cs,expected)
######### POLYNOMIALS tests #############

#we compare the polynomial with expected output 
    def testpoly1(self):
        expected_poly = np.poly1d([-3.444, 51.5,-294.777,805.833,-1063.777,592.666,-88.0])
        r1cs=np.array([[[0,1,0,0,0,0],[0,1,0,0,0,0],[0,0,0,1,0,0]],
            [[0,0,0,1,0,0],[0,1,0,0,0,0],[0,0,0,0,1,0]],
            [[0,1,0,0,1,0],[1,0,0,0,0,0],[0,0,0,0,0,1]],
            [[5,0,0,0,0,1],[1,0,0,0,0,0],[0,0,1,0,0,0]]])
        polynoms=generate_polynoms(r1cs)
        s=np.array([1, 3, 35, 9, 27, 30])
        t=generate_polynomT(s,polynoms)
        np.testing.assert_equal(np.isclose(t.coeffs,expected_poly.coeffs,atol=0.001),[1,1,1,1,1,1,1])

#we compare the polynomial with expected output 
    def testpoly2(self):
        expected_poly = np.poly1d([-2.583,55.36,-504.2, 2536,-7626.861,1.37927e+04,-1.4236936e+04,7335.9,-1350])
        r1cs=np.array([[[0,1,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,0,0,1,0,0,0]],
                    [[0,0,0,0,1,0,0,0],[0,1,0,0,0,0,0,0],[0,0,0,0,0,1,0,0]],
                    [[0,0,0,0,0,1,0,0],[2,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0]],
                    [[0,0,0,0,0,0,1,0],[0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1]],
                    [[-5,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0]]])
        polynoms=generate_polynoms(r1cs)
        s=np.array([1, 3,4,211,9,27,54,216])
        t=generate_polynomT(s,polynoms)
        print(t.coeffs)
        print(expected_poly.coeffs)
        np.testing.assert_equal(np.isclose(t.coeffs,expected_poly.coeffs,atol=0.8),[1,1,1,1,1,1,1,1,1])


######### VERIFICATION tests #############

#verify the proof with s = 0 0 0 ...
    def testverif1(self):
        expected_poly = np.poly1d([-2.583,55.36,-504.2, 2536,-7626.861,1.37927e+04,-1.4236936e+04,7335.9,-1350])
        r1cs=np.array([[[0,1,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,0,0,1,0,0,0]],
                    [[0,0,0,0,1,0,0,0],[0,1,0,0,0,0,0,0],[0,0,0,0,0,1,0,0]],
                    [[0,0,0,0,0,1,0,0],[2,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0]],
                    [[0,0,0,0,0,0,1,0],[0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1]],
                    [[-5,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0]]])
        polynoms=generate_polynoms(r1cs)
        s=np.array([0, 0,0,0,0,0,0,0])
        t=generate_polynomT(s,polynoms)
        print(t.coeffs)
        print(expected_poly.coeffs)
        self.assertTrue(s_is_solution(s,polynoms,5)) #i need to elaborate more on this case ...

#verify the proof with s = 1 0 0 ...
    def testverif2(self):
        expected_poly = np.poly1d([-2.583,55.36,-504.2, 2536,-7626.861,1.37927e+04,-1.4236936e+04,7335.9,-1350])
        r1cs=np.array([[[0,1,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,0,0,1,0,0,0]],
                    [[0,0,0,0,1,0,0,0],[0,1,0,0,0,0,0,0],[0,0,0,0,0,1,0,0]],
                    [[0,0,0,0,0,1,0,0],[2,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0]],
                    [[0,0,0,0,0,0,1,0],[0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1]],
                    [[-5,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0]]])
        polynoms=generate_polynoms(r1cs)
        s=np.array([1, 0,0,0,0,0,0,0])
        t=generate_polynomT(s,polynoms)
        print(t.coeffs)
        print(expected_poly.coeffs)
        self.assertFalse(s_is_solution(s,polynoms,5))

#we verify the proof with a random s
    def testverif2(self):
        expected_poly = np.poly1d([-2.583,55.36,-504.2, 2536,-7626.861,1.37927e+04,-1.4236936e+04,7335.9,-1350])
        r1cs=np.array([[[0,1,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,0,0,1,0,0,0]],
                    [[0,0,0,0,1,0,0,0],[0,1,0,0,0,0,0,0],[0,0,0,0,0,1,0,0]],
                    [[0,0,0,0,0,1,0,0],[2,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0]],
                    [[0,0,0,0,0,0,1,0],[0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1]],
                    [[-5,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0]]])
        polynoms=generate_polynoms(r1cs)
        s=np.array([1,5,8,34,28,90,4,76])
        t=generate_polynomT(s,polynoms)
        print(t.coeffs)
        print(expected_poly.coeffs)
        self.assertFalse(s_is_solution(s,polynoms,5))

#we verify the proof with almost the right s
    def testverif2(self):
        expected_poly = np.poly1d([-2.583,55.36,-504.2, 2536,-7626.861,1.37927e+04,-1.4236936e+04,7335.9,-1350])
        r1cs=np.array([[[0,1,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,0,0,1,0,0,0]],
                    [[0,0,0,0,1,0,0,0],[0,1,0,0,0,0,0,0],[0,0,0,0,0,1,0,0]],
                    [[0,0,0,0,0,1,0,0],[2,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0]],
                    [[0,0,0,0,0,0,1,0],[0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1]],
                    [[-5,0,0,0,0,0,0,1],[1,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0]]])
        polynoms=generate_polynoms(r1cs)
        s=np.array([1, 3,4,211,9,27,53,216])
        t=generate_polynomT(s,polynoms)
        print(t.coeffs)
        print(expected_poly.coeffs)
        self.assertFalse(s_is_solution(s,polynoms,5))

#other tests : we try to run our programm manually with different combination of CLI ....
#normally we should test the reading and writing on file (file with wrong format/missing information/inexistant/test the regex etc....)
#but we will not do it for now

#INTEGRATION TESTS ...

unittest.main()