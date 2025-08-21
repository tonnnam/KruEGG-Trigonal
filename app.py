import streamlit as st
import math
import random
import re

st.set_page_config(page_title="Triangle Trig Game", page_icon="🎯")

# ---------------------- ฟังก์ชันช่วยตรวจคำตอบ ----------------------
def parse_answer(user_input: str):
    """ แปลงคำตอบจาก string เป็นค่า float เพื่อตรวจ """
    user_input = user_input.strip()
    user_input = user_input.replace("√", "math.sqrt")  # แปลง √ เป็น math.sqrt

    # ถ้าเป็นเศษส่วนเช่น 3/5
    if re.match(r"^\d+/\d+$", user_input):
        num, den = user_input.split("/")
        return float(num) / float(den)

    try:
        # eval แต่จำกัด scope
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
    angles = [15, 30, 45, 60, 75, 90, 120]
    angle = random.choice(angles)

    if func == "sin":
        correct = round(math.sin(math.radians(angle)), 3)
    elif func == "cos":
        correct = round(math.cos(math.radians(angle)), 3)
    else:
        correct = round(math.tan(math.radians(angle)), 3)

    return f"หา {func}({angle}°)", correct

def ask_law_of_sines():
    A = random.choice([30, 45, 60])
    B = random.choice([60, 75, 45])
    a = random.randint(5, 15)
    b = round(a * math.sin(math.radians(B)) / math.sin(math.radians(A)), 2)
    return f"ให้ A = {A}°, B = {B}°, a = {a}\nจงหา b", b

def ask_law_of_cosines():
    a = random.randint(5, 12)
    b = random.randint(5, 12)
    C = random.choice([30, 60, 90, 120])
    c = round(math.sqrt(a**2 + b**2 - 2*a*b*math.cos(math.radians(C))), 2)
    return f"ให้ a = {a}, b = {b}, C = {C}°\nจงหา c", c

# ---------------------- Init Session ----------------------
if "level" not in st.session_state:
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.question, st.session_state.answer = ask_basic_trig()
    st.session_state.feedback = ""
    st.session_state.correct_flag = False

# ---------------------- UI ----------------------
st.title("🎯 Triangle Trig Game")
st.write(f"**ด่าน {st.session_state.level}** | คะแนน: {st.session_state.score}")

st.write("โจทย์:")
st.code(st.session_state.question)

# แบบฟอร์มคำตอบ
with st.form(key="answer_form"):
    user_input = st.text_input("คำตอบของคุณ (เช่น 3/5, 0.6, √3/2):")
    submitted = st.form_submit_button("ตรวจคำตอบ")

if submitted:
    correct = st.session_state.answer
    if check_answer(user_input, correct):
        st.session_state.feedback = "✅ ถูกต้อง!"
        st.session_state.score += 1
        st.session_state.correct_flag = True   # ตั้ง flag ให้แสดงปุ่ม
    else:
        st.session_state.feedback = f"❌ ผิด! คำตอบที่ถูกคือ {correct}\nเริ่มใหม่ที่ด่าน 1"
        st.session_state.level = 1
        st.session_state.score = 0
        st.session_state.question, st.session_state.answer = ask_basic_trig()
        st.session_state.correct_flag = False

# แสดงผล
if st.session_state.feedback:
    st.info(st.session_state.feedback)

# ถ้าตอบถูก -> โชว์ปุ่ม "ไปด่านถัดไป"
if st.session_state.correct_flag:
    if st.button("➡️ ไปด่านถัดไป"):
        st.session_state.level += 1
        # เลือกโจทย์ตาม level
        if st.session_state.level <= 10:
            st.session_state.question, st.session_state.answer = ask_basic_trig()
        elif st.session_state.level <= 20:
            st.session_state.question, st.session_state.answer = ask_law_of_sines()
        else:
            st.session_state.question, st.session_state.answer = ask_law_of_cosines()
        
        # รีเซ็ต flag และ feedback
        st.session_state.correct_flag = False
        st.session_state.feedback = ""
