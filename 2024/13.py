from dataclasses import dataclass
import re

COST_A = 3
COST_B = 1

@dataclass
class ButtonPushes:
    a: int
    b: int

    def cost(self):
        return int(self.a * COST_A) + int(self.b*COST_B)


@dataclass
class Button:
    x: int
    y: int


@dataclass
class ClawMachine:
    a: Button
    b: Button
    prize: Button

    def max_button_presses(self) -> tuple[int, int]:
        max_a = max(self.prize.x // self.a.x ,self.prize.y // self.a.y) + 1
        max_b = max(self.prize.x // self.b.x ,self.prize.y // self.b.y) + 1
        return (max_a, max_b)
    
    def min_button_presses(self) -> int:
        
        min_x = self.prize.x // (self.a.x + self.b.x)
        min_y = self.prize.y // (self.a.y + self.b.y)
    
        return min(min_x, min_y)
    

def read_input(file="2024/13_calibration.txt", p2 = False):
    input = open(file).read().split("\n\n")
    claw_machines = []
    for claw in input:
        cm = ClawMachine(*(Button(*tuple(map(int, re.findall(r"\d+", line)))) for line in claw.splitlines()))
        if p2:
            cm.prize.x += 10000000000000
            cm.prize.y += 10000000000000

        claw_machines.append(cm)

    return claw_machines
            

def is_int(n: float) -> bool:
    decimal_values = str(n).split(".")[-1]
    return int(decimal_values[:4]) == 0
    
def solve(cm) -> ButtonPushes | None:
    y = (cm.prize.x * cm.a.y - cm.prize.y * cm.a.x ) / (cm.b.x * cm.a.y - cm.b.y * cm.a.x)
    if y > 0 and is_int(y):
        y = int(y)
    else:
        return None
    x = (cm.prize.x - cm.b.x * y) / cm.a.x
    if x > 0 and is_int(x):
        x = int(x)
    else:
        return None
    
    return ButtonPushes(x,y)


def solution(p2 = False):
    claw_machines = read_input("2024/13_input.txt", p2)
    tokens = int(0)
    for cm in claw_machines:
        sol = solve(cm)
        if sol:
            t = sol.cost()
            tokens = tokens + int(t)

    print("Solution: ", tokens)


if __name__ == "__main__":
    solution()
    solution(True)



