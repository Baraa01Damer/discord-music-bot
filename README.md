Discord Music Bot
=================

Overview
--------
A simple Discord music bot that can search for and play audio from YouTube¹ directly in a voice channel. The bot supports basic functionalities like playing songs based on a search query, managing a queue, and skipping currently playing songs.

¹I'm planning on adding Soundcloud, Spotify, and maybe local file support in the future.

Commands:
----------
- `!play [search query]`: Searches YouTube for the provided query and adds the first result to the queue. If no song is playing, it will start playing immediately.
- `!skip`: Skips the currently playing song and plays the next one in the queue.
- `!shuffle`: Shuffles songs in a queue.
- `!queue`: Lists all songs in the queue.
- `!leave`: Leaves the voice channel and clears the queue.
- `!clear`: Clears the queue
- `!playtop`: Queues a song and places it as first position in the queue
- `!remove #`: Removes a specific song from the queue