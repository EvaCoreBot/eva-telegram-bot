# Usage Guide for eva-telegram-bot

This guide explains how to set up, run and deploy the Telegram bot on your local machine and on Render.

## Prerequisites

- Python 3.10 or higher.
- A Telegram bot token from BotFather.
- An OpenAI API key.
- (Optional) Bitrix24 webhook URL and folder/task IDs if you plan to use the Bitrix integration.

## Installation

1. Clone this repository and navigate into it:

   ```bash
   git clone https://github.com/EvaCoreBot/eva-telegram-bot.git
   cd eva-telegram-bot
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Copy the `.env.example` file to `.env` and replace placeholder values with your actual tokens and IDs.

   ```bash
   cp .env.example .env
   ```

## Running Locally

Start the Telegram bot using the following command:

```bash
python3 eva_bot.py
```

The bot will start polling Telegram for new messages and respond using OpenAI.

If you need to handle Bitrix24 webhooks, run the Flask app instead:

```bash
python3 bitrix_webhook.py
```

This will start a web server (default port 5000) with an endpoint `/webhook`. Configure your Bitrix24 outgoing webhook to send POST requests to this URL.

## Deployment on Render

To deploy the bot on Render:

1. Create a new Web Service in your Render dashboard and connect this repository.
2. Set the **Environment** to Python.
3. Set the **Build Command** to:

   ```
   pip install -r requirements.txt
   ```

4. Set the **Start Command** to:

   ```
   python3 eva_bot.py
   ```

   - If you also need the Bitrix24 webhook, create a separate service or a background worker with start command `python3 bitrix_webhook.py`.

5. In the **Environment Variables** section, add your `TELEGRAM_TOKEN`, `OPENAI_API_KEY`, and any Bitrix‑related variables defined in `.env.example`.

6. Click **Create Web Service**. Render will build and start your container.

See [Render documentation](https://render.com/docs/web-services) for more details.
