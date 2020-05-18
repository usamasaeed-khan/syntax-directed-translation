# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 02:25:00 2020

@author: Usama Saeed
"""

import re, abc, sys



""" Abstract class that provides functions
     for assembly language code. """
     
class Assembly(abc.ABC):
    
    @abc.abstractmethod
    def get_assembly_code(self, character):
        pass
    
    def generate_start_assembly(self):
        
        return ("INCLUDE C:\\Irvine\\Irvine32.inc\n"
                "INCLUDELIB C:\\Irvine\\Irvine32.lib\n"
                "INCLUDELIB C:\\Irvine\\Kernel32.lib\n"
                "INCLUDELIB C:\\Irvine\\User32.lib\n\n"
                ".CODE\n"
                "MAIN PROC\n\n"
                "    MOV EAX,0\n")
    
    def generate_end_code(self):
        
        return ("    CALL WRITEDEC\n\n"
                "MAIN ENDP\n"
                "END MAIN")
        

class SDT(Assembly):
    
    def __init__(self, expression):
        
        self.tokens_list = self.generate_tokens(expression)
        self.index = 0
        
    def generate_tokens(self, expression):
        return re.findall('[0-9]+|\+|\-|\/|\*|\(|\)', expression)
    
    def __move_next__(self):
        if self.index < len(self.tokens_list) - 1:
            self.index += 1
    
    
    def display_tokens_list(self):
        
        print()
        for i in range(len(self.tokens_list)): 
            
            print("Token[" + str(i) + "]  =  " + self.tokens_list[i], end = "")    
            print("  (Number)") if self.tokens_list[i].isdigit() else print(" (Operator)")
    
        print("\n")
    def get_assembly_code(self, character):
        
        switch_case = {
                
                "+" : "    POP AX\n"
                      "    POP BX\n"
                      "    ADD AX,BX\n"
                      "    PUSH AX\n",
                    
                "-" : "    POP BX\n"
                      "    POP AX\n"
                      "    SUB AX,BX\n"
                      "    PUSH AX\n",
                    
                "*" : "    POP AX\n"
                      "    POP BX\n"
                      "    MUL BX\n"
                      "    PUSH AX\n",
                
                "/" : "    POP BX\n"
                      "    POP AX\n"
                      "    MOV DX, 0\n"
                      "    DIV BX\n"
                      "    PUSH AX\n",
                     
                "%" : "    POP BX\n"
                      "    POP AX\n"
                      "    MOV DX, 0\n"
                      "    DIV BX\n"
                      "    PUSH DX\n"
        }
    
        return "    MOV AX, " + character + "\n    PUSH AX\n" if character.isdigit() else switch_case.get(character, "")
    
    
    def __str__(self):
        print("Parse Tree Leaf Nodes: ")
        file_text = super().generate_start_assembly() + self.__expr() + super().generate_end_code()
        print("\n\nAssembly file has been successfully generated with the following code, named: output.asm\n\n\n")
        with open('output.asm', 'w') as fout:
            fout.write(file_text)
            
        return file_text
        
    
    def __expr(self):
        return self.__term() + self.__expr__()

    def __expr__(self):
        
        if self.tokens_list[self.index] == "+" or self.tokens_list[self.index] == "-":
            
            current_index_assembly = self.get_assembly_code(self.tokens_list[self.index])
            self.__move_next__()
            return self.__term() + self.__expr__() + current_index_assembly
        
        else:
            print("\u03B5 ")
            return ""
            
            
    def __term(self):
        return self.__factor() + self.__term__()
    
    def __factor(self):
        
        if self.tokens_list[self.index].isdigit():
            
            current_index_assembly = self.get_assembly_code(str(self.tokens_list[self.index]))
            print(self.tokens_list[self.index])
            self.__move_next__()
            
            return current_index_assembly
        
        elif self.tokens_list[self.index] == "(":
    
            print(self.tokens_list[self.index])
            self.__move_next__()
            expr_val = self.__expr()
            
            if self.tokens_list[self.index] == ")":
                print(self.tokens_list[self.index])
                self.__move_next__() 

            return expr_val    
    
    def __term__(self):
        
        if self.tokens_list[self.index] == "*" or self.tokens_list[self.index] == "/" or self.tokens_list[self.index] == "%":
            
            
            print(self.tokens_list[self.index])
            current_index_assembly = self.get_assembly_code(self.tokens_list[self.index])
            self.__move_next__()
            
            return self.__factor() + self.__term__() + current_index_assembly
        
        else:
            print("\u03B5 ")
            return ""

        
if __name__ == '__main__':
    
    if (len(sys.argv) == 2) :
    
        expression = sys.argv[1]
        sdt = SDT(expression)
        sdt.display_tokens_list()
        print(sdt)
        
    else:
        print("\n\nExpected number of arguments: 2(1-python file\t2-expression in string), found: " + str(len(sys.argv)) + " arguments, terminating...\n\n")
    

