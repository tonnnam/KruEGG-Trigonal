document.addEventListener("DOMContentLoaded", () => {
  const checkBtn = document.querySelector("#check-answer"); // ปุ่มตรวจคำตอบ
  const radios = document.querySelectorAll("input[name='answer']");
  const choices = document.querySelectorAll(".stRadio label");

  checkBtn.addEventListener("click", () => {
    let selected = document.querySelector("input[name='answer']:checked");

    if (!selected) {
      alert("เลือกคำตอบก่อนนะ!");
      return;
    }

    // รีเซ็ตเอฟเฟกต์เก่า
    choices.forEach(label => {
      label.classList.remove("correct", "wrong");
    });

    // สมมุติคำตอบที่ถูกคือ value="2" (ปรับตามจริงของคุณ)
    const correctAnswer = "2";

    if (selected.value === correctAnswer) {
      selected.parentElement.classList.add("correct");
      showFloatingEmoji("❤️"); // หัวใจลอยตอนตอบถูก
    } else {
      selected.parentElement.classList.add("wrong");
      showFloatingEmoji("💔"); // หัวใจแตกตอนตอบผิด
    }
  });

  // ฟังก์ชันทำอีโมจิลอยๆ
  function showFloatingEmoji(symbol) {
    const emoji = document.createElement("div");
    emoji.textContent = symbol;
    emoji.className = "floating-emoji";
    document.body.appendChild(emoji);

    // เอาออกหลัง 1.5 วิ
    setTimeout(() => {
      emoji.remove();
    }, 1500);
  }
});