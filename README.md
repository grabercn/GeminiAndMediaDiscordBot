# Bard Discord Bot

Bard Discord Bot is a Python-based Discord bot that can respond to messages using AI. It can play music from local files, download music from YouTube, and perform various other functions.

## Prerequisites

Before running the bot, make sure you have the following:

- Python 3.x installed
- Discord.py library installed (`pip install discord.py`)
- PyTube library installed (`pip install pytube`)
- FFmpeg installed and added to the system's PATH
- __Check requirements.txt for further requirements!__

## Getting Started

1. Clone this repository to your local machine.
2. Create a `credentials.py` file in the same directory as `main.py` and define the following variables:
  - `bot_token`: Your Discord bot token
  - `geminiCookie`: Your Gemini API cookie
  - `music_dir`: The directory where your music files are stored
3. Customize the bot's behavior by modifying the `personality` variable in the `CallAI` function.
4. Run the bot by executing the `main.py` file (`python main.py`).

## Usage

The bot responds to the following commands:

- `!echo <message>`: Echoes the provided message.
- `!play <song>`: Plays the specified song from a local file or downloads and plays it.
- `!download <video_url>`: Downloads audio from the provided YouTube video URL or search term.
- `!list music`: Lists all the music files in the music directory.
- `!stop` or `!quit` or `!leave`: Stops playing music and leaves the voice channel.
- `!queue <song>`: Adds the specified song to the music queue.
- `!clear queue`: Clears the music queue.
- `!list queue`: Lists all the songs in the music queue.
- `!skip queue`: Skips the current song in the music queue.
- `!delete <file>`: Deletes the specified music file (admin user only).
- `!speak <text>`: Makes the bot speak the provided text in the voice channel.
- `!status <status>`: Sets the bot's status to the provided status.
- `!message <username> <message>`: Sends a message to the specified user.
- `!personality <number>`: Changes the bot's personality.
- `!quote`: Quotes the last user's message and adds it to a quotes list.
- `!list quotes`: Lists all the quotes in the quotes list.
- `!delete quotes`: Deletes all the quotes in the quotes list (admin user only).

## Contributing

Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
