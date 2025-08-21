import math
import random

def ask_basic_trig():
    funcs = ["sin", "cos", "tan"]
    func = random.choice(funcs)
    # เพิ่มมุมเยอะขึ้น
    angles = [15, 30, 45, 60, 75, 90, 120]
    angle = random.choice(angles)
    
    try:
        if func == "sin":
            correct = round(math.sin(math.radians(angle)), 3)
        elif func == "cos":
            correct = round(math.cos(math.radians(angle)), 3)
        else:  # tan
            correct = round(math.tan(math.radians(angle)), 3)

        print(f"\nหา {func}({angle}°) (ตอบทศนิยม 3 ตำแหน่ง)")
        ans = float(input("คำตอบ: "))
        return abs(ans - correct) < 0.01
    except:
        return False


def ask_law_of_sines():
    A = random.choice([30, 45, 60])
    B = random.choice([60, 75, 45])
    a = random.randint(5, 15)
    b = round(a * math.sin(math.radians(B)) / math.sin(math.radians(A)), 2)

    print(f"\nให้ A = {A}°, B = {B}°, a = {a}")
    print("จงหา b (ตอบทศนิยม 2 ตำแหน่ง)")
    try:
        ans = float(input("คำตอบ: "))
        return abs(ans - b) < 0.05
    except:
        return False


def ask_law_of_cosines():
    a = random.randint(5, 12)
    b = random.randint(5, 12)
    C = random.choice([30, 60, 90, 120])
    c = round(math.sqrt(a**2 + b**2 - 2*a*b*math.cos(math.radians(C))), 2)

    print(f"\nให้ a = {a}, b = {b}, C = {C}°")
    print("จงหา c (ตอบทศนิยม 2 ตำแหน่ง)")
    try:
        ans = float(input("คำตอบ: "))
        return abs(ans - c) < 0.05
    except:
        return False


def game():
    print("🎯 เกมทบทวนตรีโกณมิติ – หาค่าด้านหรือมุมของสามเหลี่ยม")
    print("ตอบผิด = เกมจบ! 🔥\n")

    score = 0
    level = 1

    while True:
        if level <= 10:
            correct = ask_basic_trig()
        elif level <= 20:
            correct = ask_law_of_sines()
        else:
            correct = ask_law_of_cosines()

        if correct:
            score += 1
            level += 1
            print(f"✅ ถูกต้อง! คะแนน: {score} | ด่าน {level-1}")
        else:
            print("❌ ผิดแล้ว! เกมจบ")
            print(f"คะแนนรวม: {score} (ถึงด่าน {level-1})")
            break


if __name__ == "__main__":
    game()
