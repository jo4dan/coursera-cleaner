from flask import Flask, render_template_string, request
import re

app = Flask(__name__)

# make detection pattern loose but effective
PATTERN = re.compile(
    r"You are a helpful AI assistant.*?other pages to study course materials or research related topics\.?",
    re.IGNORECASE | re.DOTALL,
)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Coursera Cleaner 🧹</title>
    <style>
        body { background-color: #111; color: #eee; font-family: monospace; padding: 20px; }
        textarea { width: 100%; height: 300px; background-color: #222; color: #eee; border: 1px solid #555; padding: 10px; }
        pre { background-color: #222; color: #0f0; padding: 10px; white-space: pre-wrap; word-break: break-word; }
        #copyBtn { background-color: #08f; color: #fff; border: none; padding: 8px 15px; margin-left: 10px; cursor: pointer; border-radius: 5px; }
        #copyBtn:hover { background-color: #06c; }
        #copyMsg { color: #0f0; margin-left: 10px; opacity: 0; transition: opacity 0.3s ease; }
        #copyMsg.show { opacity: 1; }
        .credit { color: rgb(57,255,20); }
    </style>
</head>
<body>
    <h2>Coursera Text Cleaner 💻 <span class="credit">github.com/jo4dan</span></h2>

    <textarea id="inputText" placeholder="paste your raw text here..."></textarea><br>

    <h3>✅ Cleaned Output (bash copy-paste friendly):</h3>
    <button id="copyBtn" onclick="copyText()">📋 Copy</button>
    <span id="copyMsg">✅ Copied!</span>
    <pre id="cleanedText"></pre>

    <script>
        async function cleanText(text) {
            const res = await fetch("/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text })
            });
            const data = await res.json();
            document.getElementById("cleanedText").innerText = data.cleaned || "";
        }

        const input = document.getElementById("inputText");
        input.addEventListener("input", async () => {
            const text = input.value.trim();
            if (text.length > 0) {
                await cleanText(text);
            } else {
                document.getElementById("cleanedText").innerText = "";
            }
        });

        function copyText() {
            const text = document.getElementById("cleanedText").innerText;
            navigator.clipboard.writeText(text).then(() => {
                const msg = document.getElementById("copyMsg");
                msg.classList.add("show");
                setTimeout(() => msg.classList.remove("show"), 1500);
                document.getElementById("inputText").value = "";
                document.getElementById("cleanedText").innerText = "";
            });
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.get_json()
        text = data.get("text", "")
        cleaned = re.sub(PATTERN, "", text)
        return {"cleaned": cleaned}
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
