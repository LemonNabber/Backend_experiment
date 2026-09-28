import os
from openai import OpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Only allow requests from your own site (set ALLOWED_ORIGIN on Render,
# e.g. https://yourname.github.io). Falls back to "*" for local testing.
CORS(app, origins=[os.environ.get("ALLOWED_ORIGIN", "*")])

# Groq has a free tier and speaks the same API as OpenAI, so we reuse the
# OpenAI library and just point it at Groq. Key comes from GROQ_API_KEY.
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

# Change the model on Render (LLM_MODEL) without touching the code
MODEL = os.environ.get("LLM_MODEL", "openai/gpt-oss-120b")
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
            max_tokens=1000,  # headroom in case the model "thinks" before answering
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
        )
        answer = (response.choices[0].message.content or "").strip()
        if not answer:
            return jsonify(error="The crayon ran out of ink. Try again!"), 500
        return jsonify(explanation=answer)
    except Exception as e:
        app.logger.error(e)
        return jsonify(error="The crayon broke. Try again!"), 500