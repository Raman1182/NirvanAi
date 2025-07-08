const submitBtn = document.getElementById('submitBtn');
const promptInput = document.getElementById('promptInput');
const responseText = document.getElementById('responseText');

submitBtn.addEventListener('click', async () => {
  const prompt = promptInput.value.trim();
  if (!prompt) {
    alert("Please enter a prompt.");
    return;
  }

  responseText.textContent = "Thinking...";

  try {
  const res = await fetch("http://127.0.0.1:8000/api/chat/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ prompt })
  });

  if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`Server error: ${res.status}\n${errorText}`);
  }

  const data = await res.json();
  responseText.textContent = data.response || "No response.";
} catch (err) {
  responseText.textContent = "Error: " + err.message;
}

});
