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

Commands:
----------
- `!play [search query]`: Searches YouTube for the provided query and adds the first result to the queue. If no song is playing, it will start playing immediately.
- `!skip`: Skips the currently playing song and plays the next one in the queue.
- `!shuffle`: Shuffles songs in a queue.
- `!queue`: Lists all songs in the queue.
