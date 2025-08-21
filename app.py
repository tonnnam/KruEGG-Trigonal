import streamlit as st
import math
import random

st.set_page_config(page_title="Triangle Trig Game", page_icon="🎯")

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

    return f"หา {func}({angle}°) (ตอบทศนิยม 3 ตำแหน่ง)", correct


def ask_law_of_sines():
    A = random.choice([30, 45, 60])
    B = random.choice([60, 75, 45])
    a = random.randint(5, 15)
    b = round(a * math.sin(math.radians(B)) / math.sin(math.radians(A)), 2)

    return f"ให้ A = {A}°, B = {B}°, a = {a}\nจงหา b (ทศนิยม 2 ตำแหน่ง)", b


def ask_law_of_cosines():
    a = random.randint(5, 12)
    b = random.randint(5, 12)
    C = random.choice([30, 60, 90, 120])
    c = round(math.sqrt(a**2 + b**2 - 2*a*b*math.cos(math.radians(C))), 2)

    return f"ให้ a = {a}, b = {b}, C = {C}°\nจงหา c (ทศนิยม 2 ตำแหน่ง)", c


# ---------------------- Init Session ----------------------
if "level" not in st.session_state:
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.question, st.session_state.answer = ask_basic_trig()
    st.session_state.feedback = ""


# ---------------------- UI ----------------------
st.title("🎯 Triangle Trig Game")
st.write(f"**ด่าน {st.session_state.level}** | คะแนน: {st.session_state.score}")

st.write("โจทย์:")
st.code(st.session_state.question)

# ใช้ st.form เพื่อให้กด Submit แล้วค่อยตรวจ
with st.form(key="answer_form"):
    user_input = st.text_input("คำตอบของคุณ:")
    submitted = st.form_submit_button("ตรวจคำตอบ")

if submitted:
    try:
        ans = float(user_input)
        correct = st.session_state.answer

        if abs(ans - correct) < 0.05:
            st.session_state.feedback = "✅ ถูกต้อง!"
            st.session_state.score += 1
            st.session_state.level += 1

            # เปลี่ยนโจทย์ตาม level
            if st.session_state.level <= 10:
                st.session_state.question, st.session_state.answer = ask_basic_trig()
            elif st.session_state.level <= 20:
                st.session_state.question, st.session_state.answer = ask_law_of_sines()
            else:
                st.session_state.question, st.session_state.answer = ask_law_of_cosines()
        else:
            st.session_state.feedback = f"❌ ผิด! คำตอบที่ถูกคือ {correct}\nเริ่มใหม่ที่ด่าน 1"
            st.session_state.level = 1
            st.session_state.score = 0
            st.session_state.question, st.session_state.answer = ask_basic_trig()
    except:
        st.session_state.feedback = "⚠️ ใส่ตัวเลขเท่านั้น"

# แสดงผลการตรวจ
if st.session_state.feedback:
    st.info(st.session_state.feedback)
