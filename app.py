import os
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Only allow requests from your own site (set ALLOWED_ORIGIN on Render,
# e.g. https://yourname.github.io). Falls back to "*" for local testing.
CORS(app, origins=[os.environ.get("ALLOWED_ORIGIN", "*")])

# Reads OPENAI_API_KEY from the environment automatically
client = OpenAI()

# Change the model on Render (OPENAI_MODEL) without touching the code
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
MAX_CHARS = 1000

SYSTEM_PROMPT = (
    "You explain things like the reader is five years old. Use tiny words, "
    "a fun everyday comparison, and at most 3 short sentences. "
    "Reply with only the explanation, no preamble."
)


@app.get("/")
def health():
    return "ELI5 backend is awake!"


@app.post("/eli5")
def eli5():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    # validate input before spending money on the API
    if not text:
        return jsonify(error="No text provided."), 400
    if len(text) > MAX_CHARS:
        return jsonify(error=f"Please select under {MAX_CHARS} characters."), 400

    try:
        response = client.chat.completions.create(
            model=MODEL,
            max_tokens=300,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
        )
        return jsonify(explanation=response.choices[0].message.content)
    except Exception as e:
        app.logger.error(e)
        return jsonify(error="The crayon broke. Try again!"), 500