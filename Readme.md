# Telegram Music Bot

A Telegram userbot that can:

- Join voice chats and play music from YouTube
- Broadcast messages to multiple groups
- Ban/unban groups from bot access

## Setup

1. Get your `API_ID` and `API_HASH` from https://my.telegram.org.
2. Generate a Pyrogram session string using: `pyrogram` or use Telethon for the same.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Place a `silent.mp3` file in the root directory. To generate one:

```bash
ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 1 silent.mp3
```

5. Run the bot:

```bash
python music_bot.py
```

## Commands

- `!join` - Join the group voice chat
- `!play <YouTube URL>` - Play music
- `!leave` - Leave the voice chat
- `!broadcast <message>` - Broadcast to all registered groups
- `!ban_group` / `!unban_group` / `!banned_groups`
