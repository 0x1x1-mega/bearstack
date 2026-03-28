from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))  # Güvenli yol

konusma_gecmisi = [
    {"role": "system", "content": "Sen her dilde konuşabilen ve yanlış değil, hep doğruları konuşan adam gibi bir asistansın. O ne istiyorsa yap."}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mesaj", methods=["POST"])
def mesaj():
    kullanici_mesaji = request.json.get("mesaj")
    konusma_gecmisi.append({"role": "user", "content": kullanici_mesaji})

    yanit = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=konusma_gecmisi
    )

    bot_yaniti = yanit.choices[0].message.content
    konusma_gecmisi.append({"role": "assistant", "content": bot_yaniti})

    return jsonify({"yanit": bot_yaniti})

if __name__ == "__main__":
    app.run(debug=True)
