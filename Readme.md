# ELI5 Backend

A small Flask server that explains any piece of text "like I'm five." It powers the crayon button on my portfolio site: highlight some text, click the crayon, and a bubble shows a simple explanation.

Live backend: https://backend-experiment-test.onrender.com

## What the backend does

The server has two endpoints.

### `GET /`
Health check. Returns the plain text `ELI5 backend is awake!`. Handy for checking that the server is running (and for waking it up, since the free Render tier sleeps).

### `POST /eli5`
Takes some text and returns a simple explanation of it.

**Request body (JSON):**

```json
{ "text": "A REST API exposes resources as URIs..." }
```

| Field | Type   | Rules                                   |
|-------|--------|-----------------------------------------|
| text  | string | Required. Can't be empty or over 1000 characters. |

**Success (200):**

```json
{ "explanation": "It's like a menu at a restaurant..." }
```

**Errors:**

| Status | Body                                          | When                                   |
|--------|-----------------------------------------------|----------------------------------------|
| 400    | `{ "error": "No text provided." }`            | Missing or empty `text`                |
| 400    | `{ "error": "Please select under 1000 characters." }` | Text is too long               |
| 500    | `{ "error": "The crayon broke. Try again!" }` | The AI request failed (see server logs) |
| 500    | `{ "error": "The crayon ran out of ink. Try again!" }` | The model returned nothing    |

Under the hood, the server sends the text to an LLM (Groq's free API, using the `openai/gpt-oss-120b` model) with a system prompt that says to use tiny words, a fun everyday comparison, and at most 3 short sentences.

## How the frontend talks to the backend

The frontend is a single script, `eli5-widget.js`, that lives in my portfolio repo and is loaded with one `<script>` tag.

1. When the visitor highlights text on the page, a small crayon button appears next to the selection. Nothing is sent to the backend yet.
2. When they click the crayon, the script makes a `POST` request to `/eli5` with the highlighted text as JSON.
3. While it waits, the bubble shows "thinking in crayon...". If it takes more than 6 seconds it says the server is waking up, since the free Render tier can take up to a minute to start after sitting idle.
4. When the response comes back, the script puts the `explanation` into the bubble (as plain text, not HTML). If the backend returns an `error`, that message is shown instead. Network failures show a generic "couldn't reach the server" message.

The bubble is placed above or below the highlight so it never covers the selected text, and its tail points at the selection.

## Setup and running locally

You need Python 3.9 or newer and a free Groq API key (get one at console.groq.com, no credit card needed).

```bash
# 1. install dependencies
pip install -r requirements.txt

# 2. set environment variables (Mac/Linux)
export GROQ_API_KEY="your-key-here"
export ALLOWED_ORIGIN="http://localhost:5500"   # where your frontend is served from

# 3. run the server
flask --app app run
```

On Windows PowerShell, use `$env:GROQ_API_KEY="your-key-here"` instead of `export`.

The server runs at `http://127.0.0.1:5000`. To test it without the frontend:

```bash
curl -X POST http://127.0.0.1:5000/eli5 \
  -H "Content-Type: application/json" \
  -d '{"text": "Photosynthesis converts light energy into chemical energy."}'
```

### Environment variables

| Variable         | Required | What it does                                                        |
|------------------|----------|---------------------------------------------------------------------|
| `GROQ_API_KEY`   | Yes      | API key for Groq. The server won't start without it.                |
| `ALLOWED_ORIGIN` | Recommended | The website allowed to call the backend, e.g. `https://yourname.github.io`. Defaults to `*` (anyone) if not set. |
| `LLM_MODEL`      | No       | Overrides the default model (`openai/gpt-oss-120b`).                |

### Deploying on Render

- Runtime: Python
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Add the environment variables above in the service's **Environment** tab.

## Authentication and secrets

- The Groq API key only exists as an environment variable on the backend (Render, or my own terminal when running locally). It is never in the frontend code and never committed to GitHub.
- Since the browser only talks to my backend, and my backend talks to Groq, visitors can't see or steal the key by viewing the page source.
- CORS is set up with `ALLOWED_ORIGIN`, so browsers will only allow my portfolio site to call the backend. This isn't real authentication (someone could still call it with a tool like curl), but it stops other websites from using it in their pages.
- Input is checked before any AI call: empty text and anything over 1000 characters is rejected. That protects the free API limits.
- The backend has no user accounts and doesn't store anything. Highlighted text is sent to the AI provider to generate the answer and isn't saved by my server.