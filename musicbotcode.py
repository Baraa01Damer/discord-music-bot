import discord
from discord.ext import commands
import yt_dlp
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

FFMPEG_OPTIONS = {
    "options": "-vn",
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
}

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'quiet': True,
    'extract_flat': False,
    'skip_download': True
}

class MusicBot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []

    @commands.command()
    async def play(self, ctx, *, search):
        voice_channel = ctx.author.voice.channel if ctx.author.voice else None
        if not voice_channel:
            return await ctx.send("You're not in a voice channel!")

        if not ctx.voice_client:
            await voice_channel.connect()

        async with ctx.typing():
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(search, download=False)

                if 'entries' in info:  # If it's a playlist
                    for entry in info['entries']:
                        url = entry['url']
                        title = entry['title']
                        self.queue.append((url, title))
                    await ctx.send(f"Added {len(info['entries'])} songs to the queue from playlist.")
                else:  # If it's a single video
                    url = info['url']
                    title = info['title']
                    self.queue.append((url, title))
                    await ctx.send(f"Added to queue: **{title}**")

            if not ctx.voice_client.is_playing():
                await self.play_next(ctx)

    async def play_next(self, ctx):
        if self.queue:
            url, title = self.queue.pop(0)
            try:
                with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(url, download=False)
                    url = info['url']  # Ensure we get the direct URL for the audio stream

                source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
                ctx.voice_client.play(
                    source, after=lambda _: self.client.loop.create_task(self.play_next(ctx))
                )
                await ctx.send(f"Now Playing **{title}**")
            except Exception as e:
                await ctx.send(f"An error occurred while trying to play **{title}**: {e}")
                await self.play_next(ctx)  # Try to play the next song in case of an error
        elif not ctx.voice_client.is_playing():
            await ctx.send("The queue is empty.")

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipped the current song.")

    @commands.command(name="queue")
    async def show_queue(self, ctx):
        if self.queue:
            queue_str = "\n".join([f"{idx + 1}. {title}" for idx, (_, title) in enumerate(self.queue)])
            await ctx.send(f"**Current Queue:**\n{queue_str}")
        else:
            await ctx.send("The queue is currently empty.")

client = commands.Bot(command_prefix="!", intents=intents)

async def main():
    try:
        await client.add_cog(MusicBot(client))
        await client.start("TOKEN")
    except asyncio.CancelledError:
        print("Bot task was cancelled")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped manually")
