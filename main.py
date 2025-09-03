# 📌 Imports
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)
from openai import OpenAI
import nest_asyncio
import asyncio

# 🧠 Your Groq API setup
client = OpenAI(
    api_key="GROQ_API_KEY",  # <-- hidden
    base_url="https://api.groq.com/openai/v1"
)

# 📄 Your notes (replace ... with your real notes or load from file)
notes_text = "These are my module notes..."

# 🤖 AI answer function using notes
def ask_question(question):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful digital trainer. Use the following notes to answer student questions."
        },
        {
            "role": "user",
            "content": f"Notes:\n{notes_text}\n\nQuestion: {question}"
        }
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    return response.choices[0].message.content

# 👋 /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Haii everyone!👋\n I'm your hybrid digital electronic trainer AI chatbot🤖\n\n"
        "You can ask me anything based on our module. Just type your question below!"
    )

# 💬 Normal message handler with typing animation
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text

    # 👀 Simulate human typing
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    await asyncio.sleep(1.5)  # Optional delay

    # 🧠 Get answer
    answer = ask_question(user_question)

    # 💬 Send reply
    await update.message.reply_text(answer)

# 🚀 Telegram Bot Setup
BOT_TOKEN = "BOT_TOKEN"  # 🔒 hidden
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# 🛠 Colab fix for event loop
nest_asyncio.apply()

# ▶️ Async main loop (Render-friendly)
async def main():
    await app.run_polling()

if name == "__main__":
    asyncio.run(main())