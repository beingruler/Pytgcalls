import os
import asyncio
import json
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream.quality import HighQualityAudio
from pytgcalls.types.stream import StreamAudioEnded
from pyrogram.idle import idle
import yt_dlp

# Replace with your own credentials
API_ID = 8217159
API_HASH = "fd7a9938ef92663a435a682ad2a8913f"
SESSION_STRING = "your_session_string"
OWNER_ID = 5776889746  # Replace with your Telegram user ID

# Load or initialize data
if os.path.exists("data.json"):
    with open("data.json", "r") as f:
        saved_data = json.load(f)
        group_chats = set(saved_data.get("groups", []))
        banned_groups = set(saved_data.get("banned", []))
else:
    group_chats = set()
    banned_groups = set()

search_results = {}  # Stores last search results per chat

def save_data():
    with open("data.json", "w") as f:
        json.dump({
            "groups": list(group_chats),
            "banned": list(banned_groups)
        }, f)

app = Client(session_name=SESSION_STRING, api_id=API_ID, api_hash=API_HASH)
pytgcalls = PyTgCalls(app)

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return f"downloads/{info['title']}.mp3"

@app.on_message(filters.group & ~filters.service)
async def register_group(client, message):
    if message.chat.id in banned_groups:
        return
    group_chats.add(message.chat.id)
    save_data()

@app.on_message(filters.command("join", prefixes="!") & filters.group)
async def join_vc(client, message):
    if message.chat.id in banned_groups:
        return
    await pytgcalls.join_group_call(
        message.chat.id,
        InputAudioStream("silent.mp3", HighQualityAudio())
    )
    await message.reply("Joined voice chat!")

@app.on_message(filters.command("play", prefixes="!") & filters.group)
async def play_audio(client, message):
    if message.chat.id in banned_groups:
        return
    if len(message.command) < 2:
        return await message.reply("Please provide a YouTube URL, song name, or a search result number.")

    query = " ".join(message.command[1:])

    # If user provides a number after using !search
    if query.isdigit():
        index = int(query) - 1
        results = search_results.get(message.chat.id)
        if not results or index < 0 or index >= len(results):
            return await message.reply("Invalid selection. Use !search first and then choose a number from the list.")
        url = results[index]["webpage_url"]
    elif not query.startswith("http"):
        # Treat as a song name
        ydl_opts = {
            'quiet': True,
            'format': 'bestaudio/best',
            'noplaylist': True,
            'default_search': 'ytsearch1',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(query, download=False)
                video = info["entries"][0] if "entries" in info else info
                url = video["webpage_url"]
            except Exception as e:
                return await message.reply(f"Error finding video: {e}")
    else:
        url = query

    try:
        audio_file = download_audio(url)
        await pytgcalls.change_stream(
            message.chat.id,
            InputAudioStream(audio_file, HighQualityAudio())
        )
        await message.reply(f"Now playing: {url}")
    except Exception as e:
        await message.reply(f"Failed to play audio: {e}")

@app.on_message(filters.command("search", prefixes="!") & filters.group)
async def search_youtube(client, message):
    if len(message.command) < 2:
        return await message.reply("Please provide a search query. Example: `!search despacito`")

    query = " ".join(message.command[1:])
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'noplaylist': True,
        'default_search': 'ytsearch5',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
            videos = info["entries"]
            if not videos:
                return await message.reply("No results found.")
            search_results[message.chat.id] = videos
            reply_text = "**Top Results:**\n\n"
            for idx, video in enumerate(videos, start=1):
                reply_text += f"`{idx}.` [{video['title']}]({video['webpage_url']}) - {video['duration_string']}\n"
            reply_text += "\nReply with `!play <number>` to play one of the results."
            await message.reply(reply_text, disable_web_page_preview=True)
        except Exception as e:
            await message.reply(f"Search failed: {e}")

@app.on_message(filters.command("leave", prefixes="!") & filters.group)
async def leave_vc(client, message):
    if message.chat.id in banned_groups:
        return
    await pytgcalls.leave_group_call(message.chat.id)
    await message.reply("Left voice chat!")

@app.on_message(filters.command("broadcast", prefixes="!") & filters.user(OWNER_ID))
async def broadcast_message(client, message):
    if len(message.command) < 2:
        return await message.reply("Usage: !broadcast <your message>")
    text = message.text.split(" ", 1)[1]
    success = 0
    fail = 0
    for chat_id in group_chats:
        if chat_id in banned_groups:
            continue
        try:
            await app.send_message(chat_id, text)
            success += 1
        except Exception as e:
            print(f"Failed in {chat_id}: {e}")
            fail += 1
    await message.reply(f"Broadcast complete: {success} success, {fail} failed.")

@app.on_message(filters.command("ban_group", prefixes="!") & filters.user(OWNER_ID))
async def ban_current_group(client, message):
    banned_groups.add(message.chat.id)
    save_data()
    await message.reply(f"Group {message.chat.id} has been banned.")

@app.on_message(filters.command("unban_group", prefixes="!") & filters.user(OWNER_ID))
async def unban_current_group(client, message):
    if message.chat.id in banned_groups:
        banned_groups.remove(message.chat.id)
        save_data()
        await message.reply(f"Group {message.chat.id} has been unbanned.")
    else:
        await message.reply("This group is not in the banned list.")

@app.on_message(filters.command("banned_groups", prefixes="!") & filters.user(OWNER_ID))
async def list_banned_groups(client, message):
    if not banned_groups:
        await message.reply("No banned groups.")
    else:
        text = "**Banned Groups:**\n" + "\n".join([str(gid) for gid in banned_groups])
        await message.reply(text)

@pytgcalls.on_stream_end()
async def on_stream_end(_, update: StreamAudioEnded):
    await pytgcalls.leave_group_call(update.chat_id)

async def main():
    await app.start()
    await pytgcalls.start()
    print("Bot is online!")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())

