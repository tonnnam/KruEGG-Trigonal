import streamlit as st
import math
import random
import re

st.set_page_config(page_title="Triangle Trig Game", page_icon="🎯")
# ใส่โค้ดนี้ไว้ใกล้ๆ กับส่วน import ด้านบน
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
def local_js(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        js_code = f.read()
    st.components.v1.html(f"""
    <script>
    {js_code}
    </script>
    """, height=0)

# ---------------------- ฟังก์ชันช่วยตรวจคำตอบ ----------------------
def parse_answer(user_input: str):
    user_input = user_input.strip()
    user_input = user_input.replace("√", "math.sqrt")

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

# ---------------------- ฟังก์ชันสร้างโจทย์ ----------------------
def ask_basic_trig():
    funcs = ["sin", "cos", "tan"]
    func = random.choice(funcs)
    if func == "tan":
        angles = [15, 30, 37, 45, 60, 75]
    else:
        angles = [15, 30, 37, 45, 60, 75, 90, 120]
    angle = random.choice(angles)

    if func == "sin":
        correct = math.sin(math.radians(angle))
    elif func == "cos":
        correct = math.cos(math.radians(angle))
    else:
        correct = math.tan(math.radians(angle))

    qtype = random.choice(["text", "mcq"])

    if qtype == "mcq":
        wrongs = [round(correct + random.uniform(-0.5, 0.5), 2) for _ in range(3)]
        options = list(set([round(correct, 2)] + wrongs))
        random.shuffle(options)
        return f"หาค่าของ {func}({angle}°)", correct, "mcq", options
    else:
        return f"หาค่าของ {func}({angle}°)", correct, "text", None

def ask_law_of_sines():
    A = random.choice([30, 45, 60])
    B = random.choice([60, 75, 45])
    a = random.randint(5, 15)
    b = a * math.sin(math.radians(B)) / math.sin(math.radians(A))
    return f"จากกฎของไซน์: ถ้า A = {A}°, B = {B}°, a = {a}\nจงหาความยาวด้าน b", b, "text", None

def ask_law_of_cosines():
    a = random.randint(5, 12)
    b = random.randint(5, 12)
    C = random.choice([30, 60, 90, 120])
    c = math.sqrt(a**2 + b**2 - 2*a*b*math.cos(math.radians(C)))
    return f"จากกฎของโคไซน์: ถ้า a = {a}, b = {b}, C = {C}°\nจงหาความยาวด้าน c", c, "text", None

# ----- ฟังก์ชันกลางสำหรับสร้างโจทย์ใหม่ตามด่าน -----
def generate_new_question():
    level = st.session_state.level
    if level <= 10:
        q_data = ask_basic_trig()
    elif level <= 20:
        q_data = ask_law_of_sines()
    else:
        q_data = ask_law_of_cosines()
    
    st.session_state.question, st.session_state.answer, st.session_state.qtype, st.session_state.options = q_data
    st.session_state.correct_flag = False
    st.session_state.feedback = ""
    st.session_state.user_input = ""


# ---------------------- Init Session ----------------------
def init_game():
    st.session_state.level = 1
    st.session_state.score = 0
    st.session_state.lives = 3 # เพิ่มชีวิตเริ่มต้น
    st.session_state.game_over = False
    generate_new_question()

if "level" not in st.session_state:
    init_game()

# ---------------------- UI ----------------------
st.title("🎯 Triangle Trig Game byKASIDIS LAKTAN")
local_css("style.css") # <<< เรียกใช้ฟังก์ชันนี้ตรงนี้

# --- หน้า Game Over ---
if st.session_state.game_over:
    st.error("### GAME OVER! 💔")
    st.write(f"คุณทำคะแนนได้ทั้งหมด: **{st.session_state.score}** คะแนน")
    if st.button("เริ่มเล่นใหม่"):
        init_game()
        st.rerun()

# --- หน้าเล่นเกม ---
else:
    # แสดงผล Level, Score, Lives
    col1, col2, col3 = st.columns(3)
    col1.metric("🚩 ด่าน", f"{st.session_state.level}")
    col2.metric("⭐ คะแนน", f"{st.session_state.score}")
    col3.metric("❤️ ชีวิต", "❤️ " * st.session_state.lives if st.session_state.lives > 0 else "หมดแล้ว!")
    st.divider()

    st.subheader("โจทย์:")
    st.code(st.session_state.question, language=None)

    # --- ส่วนของการตอบ ---
    def handle_correct_answer():
        st.session_state.feedback = "✅ ถูกต้อง! เก่งมากครับ"
        st.session_state.score += 1
        st.session_state.correct_flag = True
        st.balloons()

    def handle_wrong_answer():
        st.session_state.lives -= 1
        correct_answer_formatted = f"{st.session_state.answer:.2f}"
        if st.session_state.lives > 0:
            st.session_state.feedback = f"❌ ผิด! คำตอบที่ถูกคือ {correct_answer_formatted}\nคุณเสีย 1 ชีวิต"
            generate_new_question() # สุ่มโจทย์ใหม่ในด่านเดิม
        else:
            st.session_state.feedback = f"❌ ผิด! คำตอบที่ถูกคือ {correct_answer_formatted}"
            st.session_state.game_over = True
        st.session_state.correct_flag = False

    # ถ้าเป็นช้อยส์
    if st.session_state.qtype == "mcq":
        choice = st.radio("เลือกคำตอบที่ถูกต้อง:", st.session_state.options, key=f"mcq_answer_{st.session_state.level}")
        if st.button("ตรวจคำตอบ"):
            if abs(choice - st.session_state.answer) < 0.01:
                handle_correct_answer()
            else:
                handle_wrong_answer()
            st.rerun()

    # ถ้าเป็นเขียนเอง
    else:
        with st.form(key=f"answer_form_{st.session_state.level}"):
            user_input = st.text_input("คำตอบของคุณ (เช่น 3/5, 0.87, √3/2):", value=st.session_state.user_input)
            submitted = st.form_submit_button("ตรวจคำตอบ")

        if submitted:
            st.session_state.user_input = user_input
            if check_answer(user_input, st.session_state.answer):
                handle_correct_answer()
            else:
                handle_wrong_answer()
            st.rerun()

    # แสดง feedback
    if st.session_state.feedback:
        if st.session_state.correct_flag:
        st.success(st.session_state.feedback)
        # หัวใจลอยตอนตอบถูก
        st.components.v1.html("""
        <div style="position:fixed; top:50%; left:50%; font-size:60px; z-index:9999; 
                    animation: heartFloat 2s ease-out forwards; pointer-events:none; 
                    transform:translate(-50%,-50%);">💖</div>
        <style>
        @keyframes heartFloat {
            0% { opacity:1; transform:translate(-50%,-50%) scale(0.5); }
            50% { transform:translate(-50%,-60%) scale(1.2); }
            100% { opacity:0; transform:translate(-50%,-80%) scale(0.8); }
        }
        </style>
        """, height=0)
    else:
        st.error(st.session_state.feedback)
        # หัวใจแตกตอนตอบผิด  
        st.components.v1.html("""
        <div style="position:fixed; top:50%; left:50%; font-size:60px; z-index:9999; 
                    animation: heartBreak 2s ease-out forwards; pointer-events:none; 
                    transform:translate(-50%,-50%);">💔</div>
        <style>
        @keyframes heartBreak {
            0% { opacity:1; transform:translate(-50%,-50%) scale(1); }
            50% { transform:translate(-50%,-40%) scale(1.3) rotate(10deg); }
            100% { opacity:0; transform:translate(-50%,-80%) scale(0.5) rotate(-10deg); }
        }
        </style>
        """, height=0)
    
    # ถ้าตอบถูก -> โชว์ปุ่ม "ไปด่านถัดไป"
    if st.session_state.correct_flag:
        if st.button("➡️ ไปด่านถัดไป"):
            st.session_state.level += 1
            generate_new_question()
            st.rerun()

