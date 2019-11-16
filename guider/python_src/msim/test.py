from python_src.msim.marie_parser import Parser

program = """
InputLoop, Input // get user input
Store InputChar // store input in variable
Subt EndChar 
Skipcond 400 // check for the end character
Jump Continue // if not end character, continue input loop
Jump Print // if end character, jump to print loop
Continue, Load InputChar // get the input char
StoreI CharArray // save it in the array
Load CharArray // load the array start address
Add One // increment
Store CharArray // store the array start address
Jump InputLoop // loop

Print, Load CharArray // load array start address
Subt One // subtract one to get last char in the array
Store CharArray // save the new address
Subt PrintStop 
Skipcond 400 // check to make sure it is not the address to stop printing at
Jump ContinuePrint // if it's not the address, continue print loop
Jump End // it is the address, end the program 
ContinuePrint, LoadI CharArray // load the actual character
Output // output the character
Jump Print // loop
End, Halt

// stored variables
InputChar, HEX 000
EndChar, HEX 023
One, HEX 001
PrintStop, HEX 01B
CharArray, HEX 01C
"""


if __name__ == '__main__':

    p = Parser(program)

    print(p.render_html())

