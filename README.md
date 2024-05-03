# Discord AI Bot

This is a Discord bot that utilizes AI to respond to messages and perform various actions, such as playing music from local files, sending messages to users, and changing its personality. The bot uses the (Bard which is now) Gemini model for generating responses.

## Setup Process

To set up and run this bot, follow these steps:

### 1. Clone the Repository

Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/grabercn/BardDiscordBot.git
```

### 2. Install Dependencies

Navigate to the project directory and install the required dependencies using pip:

```bash
cd BardDiscordBot
pip install -r requirements.txt
```

### 3. Set Up Credentials

Create a `credentials.py` file in the project directory. This file should contain sensitive information such as your Discord bot token, Gemini API cookies, and the directory path for your music files. Here's an example of what the `credentials.py` file should look like:

```python
# credentials.py

# Discord bot token
bot_token = "your_discord_bot_token_here"

# Gemini API cookies
geminiCookie = "your_gemini_api_cookies_here"

# Music directory path
music_dir = "C:/Users/yourusername/Music"
```

Replace `"your_discord_bot_token_here"`, `"your_gemini_api_cookies_here"`, and `"C:/Users/yourusername/Music"` with your actual Discord bot token, Gemini API cookies, and the directory path where your music files are stored respectively.

### 4. Run the Bot

Run the bot by executing the main script (`bot.py`):

```bash
python main.py
```

The bot should now be up and running on your Discord server.

## Usage

Once the bot is running, you can interact with it using various commands. Here are some examples:

- Mention the bot with `@bot help` to get a list of available commands.
- Mention the bot with `@bot personality <number>` to change its personality.
- Mention the bot with `@bot play <song_name>` to play a music file from the local directory.
- Mention the bot with `@bot list music` to list all music files in the directory.
- Mention the bot with `@bot stop` to stop playing music and disconnect from the voice channel.
- Mention the bot with `@bot message <username> <message>` to send a message to a user.

For any further customization or troubleshooting, refer to the documentation or reach out to the repository owner.

---

Feel free to modify and expand upon this README as needed for your project! Let me know if you need further assistance.
