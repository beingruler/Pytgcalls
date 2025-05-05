# Telegram Music Bot with Voice Chat Support

A feature-rich Telegram music bot that supports playing music in group voice chats using YouTube search and streaming. Built using Pyrogram and PyTgCalls.

## 🚀 Features

- Join/Leave group voice chats
- Play audio by:
  - YouTube link
  - Song name
  - Selecting from search results (`!search`)
- YouTube audio streaming via `yt_dlp`
- Owner-only commands:
  - Ban/unban groups
  - Broadcast message
- Auto-registration of active groups

## 🔧 Requirements

- Python 3.7+
- `ffmpeg` installed and added to PATH

## 📦 Dependencies

Install required packages using:

```bash
pip install -r requirements.txt
```

**requirements.txt**:
```text
pyrogram
tgcrypto
pytgcalls
yt-dlp
```

## 📁 Setup

1. Clone the repository:
```bash
git clone <repo-url>
cd <repo-folder>
```

2. Create `data.json` manually or let the bot generate it.

3. Generate a session string with Pyrogram or use tools like [StringSession generator](https://docs.pyrogram.org/start/auth#generating-the-string-session).

4. Replace these values in the script:
```python
API_ID = 123456
API_HASH = "your_api_hash"
SESSION_STRING = "your_session_string"
OWNER_ID = 123456789
```

5. Create a silent mp3 file named `silent.mp3` or download one and place it in the bot's root folder.

6. Create a folder called `downloads`:
```bash
mkdir downloads
```

7. Run the bot:
```bash
python music_bot.py
```

## 📜 Commands

| Command | Description |
|--------|-------------|
| `!join` | Join the voice chat |
| `!play <song name/url/index>` | Play a song from name, URL, or previous search |
| `!search <query>` | Search YouTube and return top 5 results |
| `!leave` | Leave the voice chat |
| `!broadcast <message>` | (Owner) Send message to all groups |
| `!ban_group` | (Owner) Ban the current group |
| `!unban_group` | (Owner) Unban the current group |
| `!banned_groups` | (Owner) List banned groups |

## 🧑 Author

- Telegram: [Who?](https://t.me/beingruler)
- GitHub: [Mine!!](https://github.com/beingruler)

## 📄 License

MIT License. See [LICENSE]() file for details.

---

Feel free to modify this bot and submit pull requests to contribute!
