import discord
from discord.ext import commands
import youtube_dl as yt_dlp
import asyncio

# Defining intents to save on resources...
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

FFMPEG_OPTIONS = {'options': '-vn'} # Config for FFMPEG to process audio
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True} # Config for youtube-dl to download the best audio format from a video

class MusicBot(commands.Cog):
    def __init__(self, client  ):
        self.client = client
        self.queue = [] # Where music info is stored

    @commands.command()
    async def play(self, ctx, *, search): # "*" allows for more than one search when searching for a song
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None # Fetches the vc, if there isn't one then it's set to None
        if not voice_channel:
            return await ctx.send("ur not in a vc dumbass")
        if not ctx.voice.client:
            await voice_channel.connect()

        async with ctx.typing(): # Will make it look like the bot is "typing" while it's getting info
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f"ytsearch:{search}", download=False)
                if 'entries' in info: # Extracting info after searching YouTube, just need title & URL
                    info = info['entries'][0]
                url = info['url']
                title = info['title']
                self.queue.append((url, title)) # Info will be added to queue
                await ctx.send(f'Added to queue: **{title}**')
        if not ctx.voice_client.is_playing(): # If nothing playing, play next in queue
            await self.play_next(ctx)

    async def play_next(self, ctx):
        if self.queue:
            url, title = self.queue.pop(0) # Takes from front of queue, also removes from queue
            source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
            ctx.voice_client.play(source, after=lambda _:self.client.loop.create_task(self.play_next(ctx))) # Plays the audio
            await ctx.send(f'Now playing: **{title}**')
        elif not ctx.voice_client.is_playing():
            await ctx.send("Queue is empty")

    @commands.command() # Skip command
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing(): # Condition so audio will pause if only if something is playing
            ctx.voice_client.stop()
            await ctx.send("Skipped")

client = commands.Bot(command_prefix="!", intents=intents)

async def main():
    await client.add_cog(MusicBot(client)) # Makes bot modular