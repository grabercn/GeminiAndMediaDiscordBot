import discord
from discord.ext import commands
from credentials import *
# define the credentials file (credentials.py) with the following variables:
# bot_token
# geminiCookie
# music_dir
# See readme for more information


# define bot token in credentials file
global pickP
pickP = 0
global queue
queue = []
prefix = "!"
admin = "chrismslist"

# HELPER FUNCTIONS---------------------------------------------

# define function to queue music
async def queueMusic(name, message):
  import os
  files = os.listdir(music_dir)
  # Check if the file exists in the music directory
  for file in files:
    if name.lower() in file.lower():
      # Add the name to the queue
      queue.append(file)
      await message.channel.send(f"{file} added to the queue.")
      return
  await message.channel.send("File not found.")
  
# define function to download music from youtube
async def download_audio(name, message):
  from pytube import YouTube
  from py_youtube import Search
  videos = Search(name).videos()
  try:
    yt_id = videos[0]['id']
  except: 
    await message.channel.send("Failed to find video.")
    return
  # Check if the name is a valid YouTube link
  if "youtube.com" in name or "youtu.be" in name:
    video_url = name
  else:
    # Download the audio from YouTube using the video ID
    video_url = f"https://www.youtube.com/watch?v={yt_id}"
  try:
    yt = YouTube(video_url)
    audio = yt.streams.filter(only_audio=True).first()
    audio.download(output_path=music_dir)
    await message.channel.send(f"Audio downloaded: {audio.title}")
    return audio.title
  except Exception as e:
    await message.channel.send(f"Failed to download audio: {str(e)}")
    
# define function to play music from local file
async def play_local_file(name, message):
  import os
  import asyncio
  # Get the list of files in the music directory
  files = os.listdir(music_dir)

  # Check if "queue" is in the message content
  if "queue" in message.content:
    import asyncio
    # Check if the queue is empty
    global queue
    if queue.count == 0:
      await message.channel.send("Queue is empty.")
    else:
      print("Queue:", queue)
      # Play files from the queue in order
      for file in queue:
        print("Playing file:", file)
        await message.channel.send(f"Playing {file}...")
        # Check if the bot is already connected to a voice channel
        if bot.voice_clients:
          voice_client = bot.voice_clients[0]
        else:
          # Connect to the voice channel
          voice_channel = message.author.voice.channel
          voice_client = await voice_channel.connect()
        
        # Check if audio is already playing
        if voice_client.is_playing():
          # Stop the current audio
          voice_client.stop()
        
        # Play the file using FFmpegPCMAudio
        source = discord.FFmpegPCMAudio(os.path.join(music_dir, file))
        voice_client.play(source)

        while voice_client.is_playing():
          await asyncio.sleep(1)
        await voice_client.disconnect()
        
        return  # Exit the function if the file is found
    # If no matching file is found
  else:
    print("Searching for file in...")
    for file in files:
      if name.lower() in file.lower():
        # Check if the bot is already connected to a voice channel
        if bot.voice_clients:
          voice_client = bot.voice_clients[0]
        else:
          # Connect to the voice channel
          voice_channel = message.author.voice.channel
          voice_client = await voice_channel.connect()
        
        #send message to channel
        await message.channel.send(f"Playing {file}...")
        
        # Check if audio is already playing
        if voice_client.is_playing():
          # Stop the current audio
          voice_client.stop()
        
        # Play the file using FFmpegPCMAudio
        source = discord.FFmpegPCMAudio(os.path.join(music_dir, file))
        voice_client.play(source)
        
        while voice_client.is_playing():
          await asyncio.sleep(1)
        await voice_client.disconnect()
        
        return  # Exit the function if the file is found
    else:
      # If no matching file is found
      await message.channel.send("File not found. Downloading and playing...")
      # Download the audio from YouTube
      name = await download_audio(name, message)
      await play_local_file(name, message)
      return

# Define a function to quit the current voice channel
async def quit_voice_channel(bot):
  if bot.voice_clients:
    for vc in bot.voice_clients:
      await vc.disconnect()

# define function to call AI
async def CallAI(text):
  from gemini import Gemini
  global pickP

  #gemini = Gemini(auto_cookies=False, cookies=geminiCookie)
  gemini = Gemini(auto_cookies=True, cookies=geminiCookie) 

  # Define the personality based on the number
  if pickP == 0:
    personality = "You are now a discord bot. Respond like this to the text beyond the ':'. DO not say anything else except for the response to the text beyond the :. After you respond, put 'START' and after you finish that part of the response put 'END': "
  elif pickP == 1:
    personality = "You are now a discord bot and you only respond in sarcastic tones. Respond like this to the text beyond the ':'. DO not say anything else except for the response to the text beyond the :. After you respond, put 'START' and after you finish that part of the response put 'END': "
  elif pickP == 2:
    personality = "You are now a discord bot. When you speak you say japanese english sounding puns like arregato-full and similar. You also love japan and love to boast about your manga collection. You are very nerdy and are obsessed with anime. Respond like this to the text beyond the ':'. DO not say anything else except for the response to the text beyond the :. After you respond, put 'START' and after you finish that part of the response put 'END': "
  elif pickP == 3:
    personality = "You are now a discord bot. When you respond you are off topic. You avoid talking about whatever is asked, and you make really bad knock knock jokes all the time. Sometimes you do answer the prompts, but with really generic or odly specific answers. You love cows and the farm, and love farming. Respond like this to the text beyond the ':'. DO not say anything else except for the response to the text beyond the :. After you respond, put 'START' and after you finish that part of the response put 'END': "
  elif pickP == 4:
    personality = "You are now a discord bot. Lets do some roleplay. Your name is now Lukas Graber. You are a boy from Medina Ohio. You love anime and love to talk about your school work and 5.0 gpa. Your best friend is Andrew Novotny. You are in boy scouts and highschool. You are aged 17, born 2006. You enjoy being smart and like to brag about it. Respond like this to the text beyond the ':'. DO not say anything else except for the response to the text beyond the :. After you respond, put 'START' and after you finish that part of the response put 'END': "
  else:
    personality = ""

  response = gemini.generate_content(personality + text)
  response = str(response.payload['candidates'][0]['text'])
  print(response)

  # Find the starting and ending positions of the desired data
  start_pos = response.find("START")
  end_pos = response.find("END")

  # Extract the data between "START" and "END"
  desired_data = response[start_pos + len("START"):end_pos].strip()

  return (desired_data)


#BOT STARTS HERE---------------------------------------------

# Replace 'bot_token' with your actual bot token
BOT_TOKEN = bot_token

# Define the intents your bot requires.
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create a bot instance with some parameters
bot = discord.Client(intents=intents)

# Event: Bot is ready and connected to Discord.
@bot.event
async def on_ready():
  print(f'{bot.user.name} has connected to Discord!')
  print(f'Bot ID: {bot.user.id}')
  print('------')


# Event: Check if the bot is mentioned and respond with the same message.
# WARNING: this event is order specific, use caution
@bot.event
async def on_message(message):
  # Check if the message does not start with the command prefix
  if not message.content.startswith(prefix):
    return
  else:
    # Remove the command prefix from the message content
    message.content = message.content.replace(prefix, '').strip()
    # Assign the value of message.content to the variable 'content'
    print("Message Received: " + message.content)

  # Don't respond to the bot's own messages
  if (message.author == bot.user):
    return
    
  #HELP---------------------------------------------
  if message.content.startswith(
      f'help'):
    print("Event fired: help")
    response = "Hello! I am a Discord bot that can respond to messages using AI. Here are the available commands:\n"
    response += "- `!echo <message>`: Echoes the provided message.\n"
    response += "- `!play <song>`: Plays the specified song from a local file, or download and play one.\n"
    response += "- `!download <video_url>`: Downloads audio from the provided YouTube video URL or a Search Term\n"
    response += "- `!list music`: Lists all the music files in the music directory.\n"
    response += "- `!stop` or `!quit` or `!leave`: Stops playing music and leaves the voice channel.\n"
    response += "- `!queue <song>`: Adds the specified song to the music queue.\n"
    response += "- `!clear queue`: Clears the music queue.\n"
    response += "- `!list queue`: Lists all the songs in the music queue.\n"
    response += "- `!skip queue`: Skips the current song in the music queue.\n"
    response += "- `!delete <file>`: Deletes the specified music file with either name, or order number. (Admin user only)\n"
    response += "- `!speak <text>`: Makes the bot speak the provided text in the voice channel.\n"
    response += "- `!status <status>`: Sets the bot's status to the provided status.\n"
    response += "- `!message <username> <message>`: Sends a message to the specified user.\n"
    response += "- `!personality <number>`: Changes the bot's personality.\n"
    response += "- `!quote`: Quotes the last user's message and adds it to a quotes list.\n"
    response += "- `!list quotes`: Lists all the quotes in the quotes list.\n"
    response += "- `!delete quotes`: Deletes all the quotes in the quotes list. (Admin user only)\n"
    response += "Feel free to try out these commands and have fun!"
    await message.channel.send(response)
  
  #ECHO---------------------------------------------
  elif message.content.startswith(
      f'echo'):
    print("Event fired: echo")
    # Extract the word after the mention in the message content
    response = message.clean_content.replace(f'echo', '').strip()
    await message.channel.send(response)
  # END OF METHOD ----------------
  
  #PLAY MUSIC FROM LOCAL FILE---------------------------------------------
  elif message.content.startswith(
      f'play'):
    print("Event fired: play music")
    # Extract the word after the mention in the message content
    response = message.clean_content.replace(f'play', '').strip()
    await play_local_file(response, message)
  # END OF METHOD ----------------
  
  #DOWNLOAD MUSIC FROM YOUTUBE---------------------------------------------
  elif message.content.startswith(
      f'download'):
    print("Event fired: download music")
    # Extract the word after the mention in the message content
    response = message.clean_content.replace(f'download', '').strip()
    await download_audio(response, message)
  
  #LIST ALL FILES IN MUSIC DIRECTORY---------------------------------------------
  elif message.content.startswith(
      f'list music'):
    print("Event fired: list music files")
    import os
    # Get the list of files in the music directory
    files = os.listdir(music_dir)
    await message.channel.send("List of music files:")
    counter = 1
    # Create a text file to store the list of music files
    file_path = "music_files.txt"
    file_content = ""
    for file in files:
      try:
        file_content += f"{counter}. {file}\n"
      except UnicodeEncodeError:
        file_content += f"{counter}. {file.encode('utf-8').decode('utf-8', 'ignore')}\n"
      counter += 1
    with open(file_path, "w", encoding="utf-8") as file:
      file.write(file_content)

    # Send the text file
    await message.channel.send(file=discord.File(file_path))

    # Delete the text file after sending
    os.remove(file_path)
  
  #STOP PLAYING MUSIC---------------------------------------------
  elif message.content.startswith(
      f'stop' or f'quit' or f'leave'):
    print("Event fired: stop playing music")
    await quit_voice_channel(bot)
    await message.channel.send("Bot has left.")
  # END OF METHOD ----------------
  
  #QUEUE MUSIC---------------------------------------------
  elif message.content.startswith(
      f'queue'):
    print("Event fired: queue music")
    print(bot.user.id, bot.user.mention, bot.user.name, message.content)
    response = message.clean_content.replace(f'queue', '').strip()
    await queueMusic(response, message)
  # END OF METHOD ----------------
  
  #CLEAR QUEUE---------------------------------------------
  elif message.content.startswith(
      f'clear queue'):
    print("Event fired: clear queue")
    queue.clear()
    await message.channel.send("Queue cleared.")
    
  #SKIP QUEUE---------------------------------------------
  elif message.content.startswith(
      f'skip queue'):
    print("Event fired: skip queue")
    if len(queue) == 0:
      await message.channel.send("Queue is empty.")
    else:
      queue.pop(0)
      await message.channel.send("Skipped the current song.")
      
  #LIST QUEUED MUSIC---------------------------------------------
  elif message.content.startswith(
      f'list queue'):
    print("Event fired: list queued music")
    if len(queue) == 0:
      await message.channel.send("Queue is empty.")
    else:
      await message.channel.send("List of queued music:")
      for i, file in enumerate(queue, start=1):
        await message.channel.send(f"{i}. {file}")
    
  #DELETE MUSIC FILE---------------------------------------------
  elif message.content.startswith(
      f'delete'):
    print("Event fired: delete music file")
    # Extract the word after the mention in the message content
    response = message.clean_content.replace(f'delete', '').strip()
    import os
    # Get the list of files in the music directory
    files = os.listdir(music_dir)
    
    
    # Search for the file based on the given name or number
    if response.isdigit():
      file_index = int(response)
      if file_index > 0 and file_index <= len(files):
        file = files[file_index - 1]
        if message.author.name == admin:
          os.remove(os.path.join(music_dir, file))
          await message.channel.send(f"{file} deleted.")
        else:
          await message.channel.send("You do not have permission to delete files.")
      else:
        await message.channel.send("Invalid file number.")
    else:
      for file in files:
        if response.lower() in file.lower():
          if message.author.name == admin:
            os.remove(os.path.join(music_dir, file))
            await message.channel.send(f"{file} deleted.")
          else:
            await message.channel.send("You do not have permission to delete files.")
          return
      # If no matching file is found
      await message.channel.send("File not found.")
        
  #SPEAK VIA BOT---------------------------------------------
  elif message.content.startswith(
      f'speak'):
    print("Event fired: speak via bot")
    import os
    import asyncio
    import subprocess

    # Extract the text to speak from the message (linux only)
    parts = message.content.split()
    if len(parts) >= 3:
    
      text_to_speak = ' '.join(parts[1:])
      # Join the voice channel of the user who sent the message
      voice_channel = message.author.voice.channel
      voice_client = await voice_channel.connect()
      
      # Import the necessary libraries

      # Set the command to convert text to speech using a Linux TTS engine
      command = f"espeak-ng -w output.wav '{text_to_speak}'"

      # Execute the command
      subprocess.run(command, shell=True)

      # Convert the WAV file to MP3
      command = "ffmpeg -i output.wav -y output.mp3"
      subprocess.run(command, shell=True)

      # Play the saved audio file
      voice_client.play(discord.FFmpegPCMAudio('output.wav'))
    
      # Wait for the audio to finish playing
      while voice_client.is_playing():
        await asyncio.sleep(1)
        
      # Delete the temporary WAV file
      command = "rm output.wav"
      subprocess.run(command, shell=True)
      
      # Leave the voice channel
      await voice_client.disconnect()
      
    else:
        await message.channel.send(
          "Invalid input. Please use '@bot speak <text>'.")
  
  #QUOTE LAST USER AND ADD TO A QUOTES LIST (txt file)---------------------------------------------
  elif message.content.startswith(
      f'quote'):
    
    import os
    #if message mentions list, list all quotes
    if "list" in message.content:
      print("Event fired: list quotes")
      file_path = "quotes.txt"
      if os.path.isfile(file_path) and os.stat(file_path).st_size == 0:
        await message.channel.send("No quotes available.")
      await message.channel.send(file=discord.File(file_path))
      return
    
    #if message mentions delete, delete all quotes
    if "delete" in message.content and message.author.name == admin:
      print("Event fired: delete quotes")
      with open("quotes.txt", "w") as file:
        file.write("")
      await message.channel.send("Quotes deleted.")
      return
    
    print("Event fired: quote last user")
    # Extract the quote from the message
    parts = message.content.split()
    if len(parts) == 1:
      try:
        # Get the last message sent in the server channel by any user
        last_message = None
        async for msg in message.channel.history(limit=2):
          if msg.author != bot.user and not(msg.content.startswith(prefix)):
            last_message = msg
            break
        if last_message:
          # Format the quote with username
          formatted_quote = f"\"{last_message.content}\" -{last_message.author.name}"
          # Save the quote to a text file
          with open("quotes.txt", "a") as file:
            file.write(formatted_quote + "\n")
          await message.channel.send("Quote added.")
        else:
          await message.channel.send("No previous message found.")
      except ValueError:
        await message.channel.send(
          "Invalid quote. Please use '!quote'.")
    else:
      await message.channel.send(
      "Invalid input. Please use '!quote'.")
  
  #SET STATUS OF BOT---------------------------------------------
  elif message.content.startswith(
      f'status'):
    print("Event fired: set status")
    # Extract the status from the message
    parts = message.content.split()
    if len(parts) >= 2:
      try:
        status = ' '.join(parts[1:])
        await bot.change_presence(activity=discord.Game(name=status))
        await message.channel.send(f"Status set to '{status}'.")
      except ValueError:
        await message.channel.send(
          "Invalid status. Please use '!status <status>'.")
    else:
      await message.channel.send(
        "Invalid input. Please use '!status <status>'.")
  
  #MESSAGE A USER---------------------------------------------
  elif message.content.startswith(
      f'message'):
    print("Event fired: message a user")
    # Extract the username and message content from the message
    parts = message.content.split()
    if len(parts) >= 4:
      try:
        username = parts[2]
        user = discord.utils.get(bot.users, name=username)
        print(user)
        if user:
          message_content = ' '.join(parts[3:])
          await user.send(message_content)
          await message.channel.send(f"Message sent to {user.name}.")
        else:
          await message.channel.send("User not found.")
      except ValueError:
        await message.channel.send(
          "Invalid username. Please use '@bot message <username> <message>'.")
    else:
      await message.channel.send(
        "Invalid input. Please use '@bot message <username> <message>'.")
  # END OF METHOD ----------------

  #CHANGE PERSONALITY---------------------------------------------
  elif message.content.startswith(
      f'personality'):
    print("Event fired: change personality")
    # Extract the personality number from the message
    parts = message.content.split()
    if len(parts) == 3:
      try:
        new_personality = int(parts[2])
        if new_personality in range(0, 5):
          global pickP
          pickP = new_personality
          await message.channel.send(f"Personality set to {new_personality}")
        else:
          await message.channel.send(
            "Invalid personality number. Please choose a number between 1 and 4."
          )
      except ValueError:
        await message.channel.send(
          "Invalid input.")
    else:
      await message.channel.send(
        "Invalid input.")
  # END OF METHOD ----------------

  # RESPOND VIA BARD METHOD---------------------------------------------
  else:
    print("Event fired: respond via Bard")
    ## Call the AI to get the response
    try: 
      response = await CallAI(response)
    except Exception as e:
      response = "Unable to call AI: " + str(e)

    await message.channel.send(response)
  # END OF METHOD -------------------  

# Run the bot with the specified token.
bot.run(BOT_TOKEN)
