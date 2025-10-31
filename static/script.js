async function sendMessage() {
  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");
  const userMessage = input.value.trim();
  if (userMessage === "") return;
  const sendBtn = document.querySelector('.input-area button');
  sendBtn.disabled = true;
  chatBox.innerHTML += `<div class="message user">${userMessage}</div>`;
  input.value = "";
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage })
    });

    if (!res.ok) throw new Error(`Server returned ${res.status}`);
    const data = await res.json();
    const botReply = data.reply;
    chatBox.innerHTML += `<div class="message bot">${botReply}</div>`;
  } catch (err) {
    console.error(err);
    chatBox.innerHTML += `<div class="message bot">Sorry — an error occurred. Please try again later.</div>`;
  } finally {
    sendBtn.disabled = false;
    chatBox.scrollTop = chatBox.scrollHeight;
  }
}