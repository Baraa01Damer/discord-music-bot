# Importing necessary libraries for the Discord bot
import discord
from discord.ext import commands  # Extension for adding commands to the bot
import yt_dlp  # Library for downloading and extracting info from YouTube videos
import asyncio  # Library to handle asynchronous operations

# Define the bot's intents, specifying what events the bot should listen for
intents = discord.Intents.default()
intents.message_content = True  # Allows the bot to read message content
intents.voice_states = True  # Allows the bot to connect to voice channels

# FFMPEG options for audio streaming, including reconnect options for stream stability
FFMPEG_OPTIONS = {
    "options": "-vn",  # No video
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
}

# yt_dlp options for audio extraction, specifying to get the best audio and avoid playlists
YDL_OPTIONS = {"format": "bestaudio", "noplaylist": True}

# Defining the MusicBot class, which is a Discord bot cog for music-related commands
class MusicBot(commands.Cog):
    def __init__(self, client):
        self.client = client  # Reference to the bot client
        self.queue = []  # Queue to store songs to be played

    @commands.command()
    async def play(self, ctx, *, search):
        """
        Command to play a song based on a search query.
        If the bot is not connected to a voice channel, it will connect.
        Adds the song to the queue and starts playing if not already.
        """
        # Check if the user is in a voice channel
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if not voice_channel:
            return await ctx.send("ur not in a vc dumbass")

        # Connect to the voice channel if the bot is not already connected
        if not ctx.voice_client:
            await voice_channel.connect()

        async with ctx.typing():  # Indicate that the bot is processing
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                # Search for the video using yt_dlp
                info = ydl.extract_info(f"ytsearch:{search}", download=False)
                if "entries" in info:
                    info = info["entries"][0]  # Get the first search result
                url = info["url"]
                title = info["title"]
                self.queue.append((url, title))  # Add the song to the queue
                await ctx.send(f"Added to queue: **{title}**")

            # Play the next song if the bot is not currently playing
            if not ctx.voice_client.is_playing():
                await self.play_next(ctx)

    async def play_next(self, ctx):
        """
        Helper method to play the next song in the queue.
        Called automatically after the current song finishes.
        """
        if self.queue:
            url, title = self.queue.pop(0)  # Get the next song from the queue
            # Create an audio source from the URL
            source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
            # Play the audio and set up a callback to play the next song when done
            ctx.voice_client.play(
                source, after=lambda _: self.client.loop.create_task(self.play_next(ctx))
            )
            await ctx.send(f"Now Playing **{title}**")
        elif not ctx.voice_client.is_playing():
            await ctx.send("queue is empty dumbass")  # Notify when the queue is empty

    @commands.command()
    async def skip(self, ctx):
        """
        Command to skip the currently playing song.
        """
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()  # Stop the current song, triggering the next one
            await ctx.send("who tf played this shit?? Skipped.")

# Creating a bot instance with the specified command prefix and intents
client = commands.Bot(command_prefix="!", intents=intents)

# Main function to add the MusicBot cog and start the bot
async def main():
    await client.add_cog(MusicBot(client))  # Add the MusicBot cog to the bot
    await client.start("TOKEN")  # Start the bot with the provided token

# Run the main function using asyncio
asyncio.run(main())