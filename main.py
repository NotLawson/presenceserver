from flask import Flask, render_template
from threading import Thread
import json

import discord
from discord import Client
import asyncio

intents = discord.Intents.all()

secrets = json.load(open("secrets.json"))

status = {
    "main": "offline",
    "activities": [
        {"type": "playing", "name": "with your feelings"}
    ]

}

class Bot(Client):
    async def on_ready(self):
        global status
        print("Bot Username:", self.user)
        print("Guild ID:", secrets["guildId"])
        print("User ID:", secrets["userId"])
        print("")
        l = 20
        # start loop
        while True:
            try:
                member = self.get_guild(secrets["guildId"]).get_member(secrets["userId"])
                activities = ""
                activities_list = []
                for activity in list(member.activities):
                    if type(activity) == (discord.Game):
                        activities += f"Playing {activity.name} ({activity.state}, {activity.details}), "
                        activities_list.append({"type": "playing", "name": activity.name, "state": activity.state, "details": activity.details})
                    elif type(activity) == (discord.Streaming):
                        activities += f"Streaming {activity.name} ({activity.url}, {activity.twitch_name}, {activity.details}), "
                        activities_list.append({"type": "streaming", "name": activity.name, "url": activity.url, "twitch_name": activity.twitch_name, "details": activity.details})
                    elif type(activity) == (discord.Spotify):
                        activities += f"Listening to {activity.title} by {activity.artist},  "
                        activities_list.append({"type": "listening", "title": activity.title, "artist": activity.artist, "cover":activity.album_cover_url})
                    elif type(activity) == (discord.CustomActivity):
                        activities += f"{activity.state}, "
                        if activity.emoji.url == None:
                            activities_list.append({"type": "custom", "name": activity.state, "emoji": activity.emoji.to_dict(), "customemoji": False})
                        activities_list.append({"type": "custom", "name": activity.state, "emoji": activity.emoji.url, "customemoji": True})
                    else:
                        activities += f"{activity.name}, "
                        activities_list.append({"type": "unknown", "name": activity.name})
                status = {
                    "main": str(member.status),
                    "activities": activities_list
                }
            except Exception as e:
                print("=====ERROR=====")
                print(e)
                print("===============")
                pass

            if l == 20:
                l = 0
                print(f"{member.display_name} is {member.status}, activities: ({activities})")
            l+=1
            await asyncio.sleep(5)

def run_bot_in_thread():
    # Important to make an event loop for the new thread
    asyncio.set_event_loop(asyncio.new_event_loop())
    bot = Bot(intents=intents)
    bot.run(secrets["botToken"])


app = Flask(__name__)

@app.route('/', methods=['get'])
def get_discord_status():
    return render_template("discord.html", status=status, json=json)

@app.route("/raw")
def raw():
    return json.dumps(status, indent=4)
Thread(target=run_bot_in_thread, daemon=True).start()

app.run("0.0.0.0", 5000)