
# A hack to avoid running the interpreter in grove.py
#if __name__ == "__main__":
#    __name__ = "notmain"
#    
#exec(open("grove.py").read())
#
## A hack to avoid running the interpreter in grove.py
#if __name__ == "notmain":
#    __name__ = "__main__"
 
from grove import * 
import sys


def check_no_parse(filename="no_parse.txt"):
    with open(filename) as f:
        numTests = 0
        numTestsPassed = 0
        for ln in f:
            numTests = numTests + 1
            try:
                parse(ln)
                print("Failed to raise a parsing error for following line:")
                print(ln)
            except GroveError:
                numTestsPassed = numTestsPassed + 1
            except Exception as e:
                print("Unexpected error (" + str(e) + ") when trying to parse the following line:")
                print(ln)
                
    return (numTestsPassed, numTests)
                
def check_no_eval(filename="no_eval.txt"):
    with open(filename) as f:
        numTests = 0
        numTestsPassed = 0
        for ln in f:
            numTests = numTests + 1
            root = parse(ln)
            try:
                root.eval()
                print("Failed to raise an evaluation error for the following line:")
                print(ln)
            except GroveError:
                numTestsPassed = numTestsPassed + 1
            except Exception as e:
                print("Unexpected error (" + str(e) + ") when trying to evaluate the following line:")
                print(ln)
                
    return (numTestsPassed, numTests)

    
def check_bad_last_eval(filename):
    with open(filename) as f:
        lines = f.readlines()
        # All of the lines should work correctly, except the last one
        for i in range(len(lines) - 1):
            root = parse(lines[i])
            root.eval()
            
        root = parse(lines[-1])
        try:
            root.eval()
            print("Failed to raise an evaluation error for following line:")
            print(lines[-1])
            raise Exception()
        except GroveError as ge:
            return ge
    return False
             
             
             
if __name__ == "__main__":
    totalPoints = 0
    
    print("Checking that parsing errors are caught...")
    (passed, numTests) = check_no_parse()
    failed = numTests - passed
    possiblePoints = 16
    points = max(possiblePoints - failed, 0)
    print("\n*** EARNED " + str(points) + " out of " + str(possiblePoints) + " for catching parsing errors.\n\n")
    totalPoints = totalPoints + points
    
    print("Checking that evaluation errors are caught...")
    (passed, numTests) = check_no_eval()
    failed = numTests - passed
    possiblePoints = 14
    points = max(possiblePoints - failed, 0)
    print("\n*** EARNED " + str(points) + " out of " + str(possiblePoints) + " for catching evaluation errors.\n\n")
    totalPoints = totalPoints + points
    
    print("Checking that type mismatch errors are caught...")
    res = check_bad_last_eval("bad_var_types.txt")
    possiblePoints = 4
    if type(res) == GroveError:
        points = possiblePoints
    else:
        points = 0
    print("\n*** EARNED " + str(points) + " out of " + str(possiblePoints) + " for catching type mismatch errors.\n\n")
    totalPoints = totalPoints + points
    
    
    print("Checking that undefined method calls are caught...")
    res = check_bad_last_eval("bad_call.txt")
    possiblePoints = 4
    if type(res) == GroveError:
        points = possiblePoints
        print("NOTE: The following GroveError should say something about an unrecognized or undefined method:")
        print(res)
    else:
        points = 0
    print("\n*** EARNED " + str(points) + " out of " + str(possiblePoints) + " for catching undefined method call errors.\n\n")
    totalPoints = totalPoints + points
           
    # We abuse the exit code to "return" the number of points to the calling environment
    sys.exit(totalPoints)
    
