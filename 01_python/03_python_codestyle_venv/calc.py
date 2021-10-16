"""
python lesson 3 task 2. Simple calc with PEP format and pylint check
(c) Stadnik Vladislav. Nix Solutions Python course (Fall 2021)
"""

class Calc:
    """ Simple calc with add/minus/double/devide functions"""

    @classmethod
    def add(cls, *args):
        """ This function calculate a sum of any count of numbers """
        return sum(args)

    @classmethod
    def minus(cls, *args):
        """ This function calculate a diff between any count of numbers """
        res = args[0]
        for i in range(1, len(args)):
            res = res - args[i]
        return res

    @classmethod
    def double(cls, *args):
        """ This function calculate a multiplication of any count of numbers """
        res = args[0]
        for i in range(1, len(args)):
            res = res * args[i]
        return res

    @classmethod
    def devide(cls, *args):
        """ This function calculate a division of any count of numbers """
        res = args[0]
        for i in range(1, len(args)):
            res = res / args[i]
        return res

if __name__ == "__main__":
    print("Simple calc test:")
    calc = Calc()
    print("3+4: ", calc.add(3, 4))
    print("3+4+2+46: ", calc.add(3, 4, 2, 46))
    print("3-4: ", calc.minus(3, 4))
    print("3-4-1-15-17: ", calc.minus(3, 4, 1, 15, 17))
    print("3*4: ", calc.double(3, 4))
    print("2*2*3*5: ", calc.double(2, 2, 3, 5))
    print("20/5: ", calc.devide(20, 5))
    print("100/4/5/2: ", calc.devide(100, 4, 5, 2))
