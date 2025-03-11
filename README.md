# Presence Server

Just a small embed thingo that shows your Discord status.

## Get Started

First, create and app at [discord.com/developers](https://discord.com/developers).

Name it whatever, enable every single "Privelleged Gateway intent" under the Bot Section.

Next, create a blank server in Discord. Name it anything, unimportant.

Add your Bot to it and grab your userID and guildID.

Enter your bot token, userID and guildID into a file named "secrets.json" (use the example.secrets.json as a template) and start main.py.

It will then start a webserver on whatever port is specified in secrets.json (default: 3000)