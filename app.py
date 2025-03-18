import google.generativeai as genai
import telegram
from datetime import datetime
import asyncio
import os

# Set your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Telegram bot token and chat ID
telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

# Generate interview questions using Gemini
def generate_interview_questions():
    prompt = (
        "Generate 20 interview questions with answers for a Python Developer role and Data Scientist role "
        "with 1-3 years of experience. Return the questions and answers in a numbered list."
    )
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(prompt, generation_config=genai.GenerationConfig(max_output_tokens=2000))
        return response.text
    except Exception as e:
        print(f"Error generating questions: {e}")
        return "Failed to generate questions."

# Send Telegram message (async)
async def send_telegram_message(content):
    try:
        bot = telegram.Bot(token=telegram_bot_token)
        await bot.send_message(chat_id=chat_id, text=content)
        print("Message sent successfully!")
    except Exception as e:
        print(f"Error sending message: {e}")

# Main function to execute the job
async def main():
    print(f"Running job at {datetime.now()}")
    questions_answers = generate_interview_questions()

    # Split the questions and answers into individual items
    items = questions_answers.split('\n')
    valid_items = [item.strip() for item in items if item.strip()]  # Remove empty lines

    for item in valid_items:
        await send_telegram_message(item)
        await asyncio.sleep(2)  # Delay to avoid rate limiting

if __name__ == "__main__":
    asyncio.run(main())
