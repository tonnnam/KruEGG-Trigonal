import streamlit as st
import math
import random
import re

st.set_page_config(page_title="Triangle Trig Game", page_icon="🎯")

# ---------------------- ฟังก์ชันช่วยตรวจคำตอบ ----------------------
def parse_answer(user_input: str):
    user_input = user_input.strip()
    user_input = user_input.replace("√", "math.sqrt")  # แปลง √ เป็น math.sqrt

    # ถ้าเป็นเศษส่วน เช่น 3/5
    if re.match(r"^\d+/\d+$", user_input):
        num, den = user_input.split("/")
        return float(num) / float(den)

    try:
        value = eval(user_input, {"math": math})
        return float(value)
    except:
        return None

def check_answer(user_input, correct_value, tol=0.01):
    val = parse_answer(user_input)
    if val is None:
        return False
    return abs(val - correct_value) < tol

# ---------------------- ฟังก์ชันโจทย์ ----------------------
def ask_basic_trig():
    funcs = ["sin", "cos", "tan"]
    func = random.choice(funcs)
    if func == "tan":
        angles = [15, 30, 37, 45, 60, 75]  # ไม่มี 90°
    else:
        angles = [15, 30, 37, 45, 60, 75, 90, 120]
    angle = random.choice(angles)

    if func == "sin":
        correct = math.sin(math.radians(angle))
    elif func == "cos":
        correct = math.cos(math.radians(angle))
    else:
        correct = math.tan(math.radians(angle))

    # สุ่มว่าจะเป็นข้อเขียน หรือ มัลติชอยส์
    qtype = random.choice(["text", "mcq"])

    if qtype == "mcq":
        wrongs = [round(correct + random.uniform(-0.5, 0.5), 2) for _ in range(3)]
        options = list(set([round(correct, 2)] + wrongs))
        random.shuffle(options)
        return f"หา {func}({angle}°)", correct, "mcq", options
    else:
        return f"หา {func}({angle}°)", correct, "text", None

def ask_law_of_sines():
    A = random.choice([30, 45, 60])
    B = random.choice([60, 75, 45])
    a = random.randint(5, 15)
    b = a * math.sin(math.radians(B)) / math.sin(math.radians(A))
    return f"ให้ A = {A}°, B = {B}°, a = {a}\nจงหา b", b, "text", None

def ask_law_of_cosines():
    a = random.randint(5, 12)
    b = random.randint(5, 12)
    C = random.choice([30, 60, 90, 120])
    c = math.sqrt(a**2 + b**2 - 2*a*b*math.cos(math.radians(C)))
    return f"ให้ a = {a}, b = {b}, C = {C}°\nจงหา c", c, "text", None

# ---------------------- Init Session ----------------------
if "level" not in st.session_state:
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.question, st.session_state.answer, st.session_state.qtype, st.session_state.options = ask_basic_trig()
    st.session_state.feedback = ""
    st.session_state.correct_flag = False
    st.session_state.user_input = ""
    st.session_state.reset_input = False

# ---------------------- UI ----------------------
st.title("🎯 Triangle Trig Game")
st.write(f"**ด่าน {st.session_state.level}** | คะแนน: {st.session_state.score}")

st.write("โจทย์:")
st.code(st.session_state.question)

# ถ้าเป็นช้อยส์
if st.session_state.qtype == "mcq":
    choice = st.radio("เลือกคำตอบที่ถูกต้อง:", st.session_state.options, key="mcq_answer")
    if st.button("ตรวจคำตอบ"):
        if abs(choice - st.session_state.answer) < 0.01:
            st.session_state.feedback = "✅ ถูกต้อง!"
            st.session_state.score += 1
            st.session_state.correct_flag = True
        else:
            st.session_state.feedback = f"❌ ผิด! คำตอบที่ถูกคือ {round(st.session_state.answer,2)}\nเริ่มใหม่ที่ด่าน 1"
            st.session_state.level = 1
            st.session_state.score = 0
            st.session_state.question, st.session_state.answer, st.session_state.qtype, st.session_state.options = ask_basic_trig()
            st.session_state.correct_flag = False

# ถ้าเป็นเขียนเอง
else:
    with st.form(key="answer_form"):
        if st.session_state.reset_input:
            st.session_state.user_input = ""
            st.session_state.reset_input = False
        user_input = st.text_input("คำตอบของคุณ (เช่น 3/5, 0.6, √3/2):", value=st.session_state.user_input)
        submitted = st.form_submit_button("ตรวจคำตอบ")

    if submitted:
        st.session_state.user_input = user_input
        correct = st.session_state.answer
        if check_answer(user_input, correct):
            st.session_state.feedback = "✅ ถูกต้อง!"
            st.session_state.score += 1
            st.session_state.correct_flag = True
        else:
            st.session_state.feedback = f"❌ ผิด! คำตอบที่ถูกคือ {round(correct,2)}\nเริ่มใหม่ที่ด่าน 1"
            st.session_state.level = 1
            st.session_state.score = 0
            st.session_state.question, st.session_state.answer, st.session_state.qtype, st.session_state.options = ask_basic_trig()
            st.session_state.correct_flag = False
            st.session_state.reset_input = True

# แสดง feedback
if st.session_state.feedback:
    st.info(st.session_state.feedback)

# ถ้าตอบถูก -> โชว์ปุ่ม "ไปด่านถัดไป"
if st.session_state.correct_flag:
    if st.button("➡️ ไปด่านถัดไป"):
        st.session_state.level += 1
        if st.session_state.level <= 10:
            st.session_state.question, st.session_state.answer, st.session_state.qtype, st.session_state.options = ask_basic_trig()
        elif st.session_state.level <= 20:
            st.session_state.question, st.session_state.answer, st.session_state.qtype, st.session_state.options = ask_law_of_sines()
        else:
            st.session_state.question, st.session_state.answer, st.session_state.qtype, st.session_state.options = ask_law_of_cosines()

        st.session_state.correct_flag = False
        st.session_state.feedback = ""
        st.session_state.reset_input = True
