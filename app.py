import streamlit as st
import math
import random

st.set_page_config(page_title="Triangle Trig Game", page_icon="🎯")

# ฟังก์ชันโจทย์
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


# =================== เกมหลัก ===================
if "level" not in st.session_state:
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.question, st.session_state.answer = ask_basic_trig()

st.title("🎯 Triangle Trig Game")
st.write(f"**ด่าน {st.session_state.level}** | คะแนน: {st.session_state.score}")

st.write("โจทย์:")
st.code(st.session_state.question)

user_input = st.text_input("คำตอบของคุณ:")

if st.button("ตรวจคำตอบ"):
    try:
        ans = float(user_input)
        correct = st.session_state.answer

        if abs(ans - correct) < 0.05:
            st.success("✅ ถูกต้อง!")
            st.session_state.score += 1
            st.session_state.level += 1

            # เปลี่ยนประเภทโจทย์ตามด่าน
            if st.session_state.level <= 10:
                st.session_state.question, st.session_state.answer = ask_basic_trig()
            elif st.session_state.level <= 20:
                st.session_state.question, st.session_state.answer = ask_law_of_sines()
            else:
                st.session_state.question, st.session_state.answer = ask_law_of_cosines()
        else:
            st.error(f"❌ ผิด! คำตอบที่ถูกคือ {correct}")
            st.session_state.level = 1
            st.session_state.score = 0
            st.session_state.question, st.session_state.answer = ask_basic_trig()
    except:
        st.warning("⚠️ ใส่ตัวเลขเท่านั้น")