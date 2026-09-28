# Prompt Log

## Tools I used

- **Claude** (Anthropic) for brainstorming, writing the widget and backend code, and debugging deploy errors
- **OpenAI API**: I started with this, but my key had no credits left, so I dropped it
- **Groq API** (free tier, `openai/gpt-oss-120b`): what the backend uses now
- **Render** to host the backend, **GitHub Pages** for the portfolio

## Key prompts

1. **Picking the idea.** I pasted the assignment and asked for a good easy idea. It suggested a chatbot version of me, which felt too expected, so I asked for less obvious ones and picked the "explain like I'm 5" tool.

2. **The main build.** "make it the same as the mini me chatbot idea, but make it look like a craft project w crayon writing and theme it around the explain like im five idea. make it so if the user highlights text on my portfolio the widget becomes a quickselect option to open a little bubble window." This gave me the highlight-to-crayon-button-to-bubble setup.

3. **Design tweaks.** I asked for the button to be just a crayon with no text. Then I asked for the bubble to never cover the highlighted text and for the tail to always point at the highlight, which is why it flips above or below and the tail slides sideways.

4. **Backend.** "how do i implement a render based backend." It gave me the Flask app, `requirements.txt`, and the Render steps. It also suggested locking CORS to my site and rejecting empty or very long text before calling the API.

5. **Putting it on my site.** I pasted my whole `index.html` and asked for the widget to be added. It ended up as one `eli5-widget.js` file so it wouldn't mess with my site's styles.

6. **Fixing errors.** The deploy failed because Render couldn't find the API key name, so I pasted the log and fixed the variable. Later the widget said "the crayon broke," and the Render logs showed I was out of OpenAI credits. I asked "is there a free api i can use??" and switched to Groq, which only needed a few lines changed in `app.py`.

## What I changed myself

- Set up my Render service, environment variables, and `ALLOWED_ORIGIN`
- Tested the widget on my live site and reported what broke
- Picked the theme and decided how the crayon and bubble should behave