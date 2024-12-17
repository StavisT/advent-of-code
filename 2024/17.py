from dataclasses import dataclass
from typing import Callable


@dataclass
class Register:
    out: list
    A: int=0
    B: int=0
    C: int=0
    instruction_pointer: int = 0
    
    def print_out(self):
        print(",".join([str(i) for i in self.out]))
    
Instruction = Callable[[int, Register], None]


def adv_0(combo:int, register: Register):
    # division
    res = int( register.A / (2**combo))
    register.A = res
        
    register.instruction_pointer += 2


def bxl_1(combo: int, register: Register):
    # bitwise xor of operand and register.B
    res = int(bin(combo),2) ^ int(bin(register.B),2)
    register.B = res

    register.instruction_pointer += 2

    
def bst_2(combo: int, register: Register):
    res = combo % 8
    register.B = res

    register.instruction_pointer += 2


def jnz_3(combo: int, register: Register):
    if register.A > 0:
        register.instruction_pointer = combo
    else:
        register.instruction_pointer += 2

        # jump by setting the instruction pointer to the value of its literal operand

def bxc_4(combo:int, register: Register):
    res = int(bin(register.B),2) ^ int(bin(register.C),2)
    register. B = res

    register.instruction_pointer += 2


def out_5(combo:int, register: Register):
    res = combo % 8
    register.out.append(res)

    register.instruction_pointer += 2


def bdv_6(combo:int, register: Register):
    res = int( register.A / (2**combo))
    register.B = res

    register.instruction_pointer += 2


def cdv_7(combo:int, register: Register):
    res = int( register.A / (2**combo))
    register.C = res

    register.instruction_pointer += 2


INSTRUCTIONS: dict[int, Instruction] = {
    0: adv_0,
    1: bxl_1,
    2: bst_2,
    3: jnz_3,
    4: bxc_4,
    5: out_5,
    6: bdv_6,
    7: cdv_7
}


def handle_operand_values(opcode: int, combo_literal: int,  register: Register) -> int:
    if opcode in [1,3]:
        return combo_literal
    if combo_literal < 4:
        return combo_literal
    elif combo_literal == 4:
        return register.A
    elif combo_literal ==5:
        return register.B
    elif combo_literal ==6:
        return register.C
    else:
        raise ValueError("Not a valid operand")
    
# needs a instruction pointer
def run_program(program: list[int], register: Register) -> None:
    last_instruction = len(program)
    while register.instruction_pointer < last_instruction -1:
        opcode = program[register.instruction_pointer]
        operand_literal = program[register.instruction_pointer +1]
        operand = handle_operand_values(opcode, operand_literal, register)

        instruction = INSTRUCTIONS[opcode]
        instruction(operand, register)



if __name__ == "__main__":
    # case 1:
    # register = Register(C=9, out=[])
    # program = [2,6]
    # run_program(program, register)
    # print(register)

    # case 2:
    # register = Register(A=10, out=[])
    # program = [5,0,5,1,5,4]
    # run_program(program, register)
    # print(register)

    # Case 3
    # register = Register(A=2024,out=[])
    # program = [0,1,5,4,3,0]
    # run_program(program, register)
    # print(register)
    
    # case 4:
    # register = Register(B=29, out=[])
    # program = [1,7]
    # run_program(program, register)
    # print(register)
    # register.print_out()

    # Case 5:
    # register = Register(B=2024, C=43690, out=[])
    # program = [4,0]

    # run_program(program, register)
    # print(register)
    # register.print_out()

    # test input
    # register = Register(A=729, out=[])
    # program = [0,1,5,4,3,0]
    # run_program(program, register)
    # print(register)
    # register.print_out()

    # # part 1:
    register = Register(A= 64012472, out= [])
    program = [2,4,1,7,7,5,0,3,1,7,4,1,5,5,3,0]
    run_program(program, register)
    print(register)
    register.print_out()


    # Part 2:
    register = Register(A=117440, out=[])
    program = [0,3,5,4,3,0]
    run_program(program, register)
    print(register)
    register.print_out()