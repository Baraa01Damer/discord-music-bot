Discord Music Bot
=================

Overview
--------
A simple Discord music bot that can search for and play audio from YouTube¹ directly in a voice channel. The bot supports basic functionalities like playing songs based on a search query, managing a queue, and skipping currently playing songs.

¹I'm planning on adding Soundcloud, Spotify, and maybe local file support in the future.

Features
--------
- Play audio from YouTube using search queries.
- Manage a queue of songs.
- Skip the currently playing song.
- Automatically play the next song in the queue.

Requirements
------------
- Python 3.8 or higher
- `discord.py` library (specifically the `discord.ext.commands` extension)
- `yt_dlp` library for downloading and processing YouTube content
- `ffmpeg` installed and added to system PATH for audio streaming

Installation
------------
1. **Clone the repository** or download the code files.

2. **Install the required Python packages** using pip: pip install discord.py yt_dlp

3. **Install FFMPEG**:
- Download FFMPEG from the official website: https://ffmpeg.org/download.html
- Follow the installation instructions and make sure to add FFMPEG to your system's PATH.

4. **Set up your Discord bot**:
- Create a new bot on the Discord Developer Portal: https://discord.com/developers/applications
- Get the bot token and replace `"TOKEN"` in the code with your actual bot token.

5. **Run the bot**:
- Execute the Python script using: python your_bot_script.py


How to Use
----------
1. **Invite the bot** to your Discord server using the OAuth2 URL generated in the Discord Developer Portal.
2. **Join a voice channel** on your server.
3. **Use the bot commands**:
- `!play [search query]`: Searches YouTube for the provided query and adds the first result to the queue. If no song is playing, it will start playing immediately.
- `!skip`: Skips the currently playing song and plays the next one in the queue.
- The bot automatically handles queue management and will notify users if the queue is empty.

Customization
-------------
- **Command Prefix**: You can change the command prefix by modifying the `command_prefix` parameter in the `commands.Bot` initialization.
- **Audio Quality**: Adjust the `FFMPEG_OPTIONS` and `YDL_OPTIONS` dictionaries to change the audio quality and streaming behavior.
- **Queue Management**: The bot currently manages a simple queue. You can extend its functionality to include more sophisticated queue controls like `pause`, `resume`, `stop`, etc.

Troubleshooting
---------------
- Make sure FFMPEG is correctly installed and accessible from the command line.
- Ensure that the bot has the necessary permissions to read messages, connect to voice channels, and speak in voice channels on your Discord server.
- Check the bot's token is correctly set and that the bot is invited to your server using the appropriate permissions.
