from bot.util import new_cmd, new_inline
from telethon import Button, events
from .db import set_team, get_chat_team, get_team_points, new_qr_scan

@new_cmd(pattern="start")
async def start_cmd(e):
    team = await get_chat_team(e.chat_id)
    if team:
        await e.reply("Welcome to **CODE QUEST!**\n\nYour mission, should you choose to accept it, is to locate the hidden QR codes scattered across the campus. Keep your wits about you, as the locations of the codes are shrouded in mystery. To help you on your quest, be sure to stay tuned to Telegram for clues and hints.\n\nYour team name is **{}**\n\nQrPoints: **{}**".format(team, await get_team_points(team)),
        buttons=[
            [Button.inline("Start Quest", b"start_quest")]
        ])
        return
    await e.reply("Welcome to **CODE QUEST!**\n\nYour mission, should you choose to accept it, is to locate the hidden QR codes scattered across the campus. Keep your wits about you, as the locations of the codes are shrouded in mystery. To help you on your quest, be sure to stay tuned to Telegram for clues and hints.",
    buttons=[
        [Button.inline("Set Team Name", b"set_team_name")]
    ])

@new_cmd(pattern="help")
async def help_cmd(e):
    help_msg = ("**Help Menu: **\n\nThis is the list of commands\n"
                "`/start` : used to start a bot and set Team Name\n"
                "`/race` : displays the current Leaderboard\n"
                "`/contact` : use this to contact the coordinators\n"
                "`/team` : displays your team name and points\n"
                "`/help` : display's all the commands\n"
                "\n if You are facing issue while scanning QR:\n"
                "send message to the coordinators with the QR code number that is written at the bottom side of QR\n"
                "\nif you are facing issues with the bot:\n"
                "Firstly check your internet connection and try again and if doesn't work you can contact the event coordinators")
 
    await e.reply(help_msg)

@new_cmd(pattern="contact")
async def contact_cmd(e):
    await e.reply("Contact the event coordinators:\n"
                  "- [RoseLoverX](https://t.me/roseloverx)\n")
    
@new_cmd(pattern="/race")
async def _current_leaderboard(e):
    # gen_leaderboard()

    await e.reply("Current Leaderboard: TODO")

@new_cmd(pattern="team")
async def _team(e):
    team = await get_chat_team(e.chat_id)
    if team:
        points = await get_team_points(team)
        await e.reply("Your team name is **{}**\n\nQrPoints: **{}**".format(team, points),
        buttons=[
            [Button.inline("Edit Team Name", b"set_team_name")]
        ])
    else:
        await e.reply("You have not set a team name yet. Use `/start` to set one.")


@new_inline(pattern="set_team_name")
async def set_team_name(e):
    async with e.client.conversation(e.chat, timeout=600) as conv:
        await conv.send_message("Please enter your team name:")
        team_name = await conv.get_response()
        await conv.send_message("**{}** is your team name. Is this correct?".format(team_name.text),
        buttons=[
            Button.inline("Yes ✅", b"yes"),
            Button.inline("No ❌", b"no")
        ])
        response = await conv.wait_event(events.CallbackQuery)
        if response.data == b"yes":
            await conv.send_message("Great!")
            await set_team(team_name.text, e.chat_id)
        else:
            await conv.send_message("Oops, let's try again.")
            await set_team_name(e)


@new_cmd(pattern="qr")
async def qr_cmd(e):
    try:
        hexCode = e.text.split(" ")[1]
    except IndexError:
        await e.reply("Please provide the unique QR code.")
        return
    team = await get_chat_team(e.chat_id)
    if not team:
        await e.reply("You have not Entered your team name yet. Use `/start` to set one.")
        return
    scan = await new_qr_scan(hexCode, team)
    if scan == -1:
        await e.reply("Sorry, that QR code is invalid.")

    if scan == 10:
        await e.reply("Congratulations! You are the first team to scan this QR code. You have been awarded **10** points.")
        return
    
    if scan == 8:
        await e.reply("Congo! You are the second team to scan this QR code. You have been awarded **8** points.")
        return
    
    if scan == 6:
        await e.reply("Good job! You are the third team to scan this QR code. You have been awarded **6** points.")
        return
    
    if scan == 5:
        await e.reply("Ouch! Top 3 teams have already scanned this QR code. You have been awarded **5** points.")
        return