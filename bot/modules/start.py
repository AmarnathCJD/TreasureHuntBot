from bot.util import new_cmd, new_inline
from telethon import Button, events
from .db import (
    get_chat_team,
    get_team_points,
    add_new_team,
    add_new_qr_team_return_points,
    get_team_name,
    reset_qrs,
    reset_teams,
    is_team_exists,
    add_member_to_team,
    generate_leaderboard,
    purge_teams,
)
from .qr_events import onNewQR

reset_qrs()
purge_teams()


@new_cmd(pattern="start")
async def start_cmd(e):
    if "qr_" in e.text:
        return await onNewQR(e)
    msg = await e.reply(
        "Welcome to **QrQuest!**\n\nYour mission, should you choose to accept it, is to locate the hidden QR codes scattered across the campus. Keep your wits about you, as the locations of the codes are shrouded in mystery. To help you on your quest, be sure to stay tuned to Telegram for clues and hints.",
        buttons=[
            [Button.inline("Set Team Name", b"set_team_name")],
            [Button.inline("Help", b"help")],
        ],
    )
    team = get_team_name(e.chat_id)
    if team:
        await msg.edit(
            "Welcome to **QrQuest!**\n\nYour mission, should you choose to accept it, is to locate the hidden QR codes scattered across the campus. Keep your wits about you, as the locations of the codes are shrouded in mystery. To help you on your quest, be sure to stay tuned to Telegram for clues and hints.\n\nYour team name is **{}**\n".format(
                team
            ),
            buttons=[
                [Button.inline("Check Points", b"check_points")],
                [Button.inline("Help", b"help")],
            ],
        )
        return


@new_inline(pattern="back")
async def start_cmd_cb(e):
    msg = await e.reply(
        "Welcome to **QrQuest!**\n\nYour mission, should you choose to accept it, is to locate the hidden QR codes scattered across the campus. Keep your wits about you, as the locations of the codes are shrouded in mystery. To help you on your quest, be sure to stay tuned to Telegram for clues and hints.",
        buttons=[
            [Button.inline("Set Team Name", b"set_team_name")],
            [Button.inline("Help", b"help")],
        ],
    )
    team = get_team_name(e.chat_id)
    if team:
        await msg.edit(
            "Welcome to **QrQuest!**\n\nYour mission, should you choose to accept it, is to locate the hidden QR codes scattered across the campus. Keep your wits about you, as the locations of the codes are shrouded in mystery. To help you on your quest, be sure to stay tuned to Telegram for clues and hints.\n\nYour team name is **{}**\n".format(
                team
            ),
            buttons=[
                [Button.inline("Check Points", b"check_points")],
                [Button.inline("Help", b"help")],
            ],
        )
        return


help_msg = (
    "**Help Menu: **\n\nThis is the list of commands\n"
    "`/start` : used to start a bot and set Team Name\n"
    "`/race` : displays the current Leaderboard\n"
    "`/contact` : use this to contact the coordinators\n"
    "`/team` : displays your team name and points\n"
    "`/help` : display's all the commands\n"
    "\n if You are facing issue while scanning QR:\n"
    "send message to the coordinators with the QR code number that is written at the bottom side of QR\n"
    "\nif you are facing issues with the bot:\n"
    "Firstly check your internet connection and try again and if doesn't work you can contact the event coordinators"
)


@new_inline(pattern="help")
async def help_inline(e):
    await e.edit(help_msg)


@new_cmd(pattern="help")
async def help_cmd(e):
    await e.reply(help_msg)


@new_cmd(pattern="contact")
async def contact_cmd(e):
    await e.reply(
        "Contact the event coordinators:\n" "- [RoseLoverX](https://t.me/roseloverx)\n",
        link_preview=False,
    )


@new_cmd(pattern="race")
async def current_leaderboard(e):
    lead = generate_leaderboard()
    msg = "**Current Leaderboard:**\n\n"
    q = 0
    gold_emoji = "🥇"
    silver_emoji = "🥈"
    bronze_emoji = "🥉"

    for x in list(lead):
        msg += "**{}.** {} - ({}) ".format(q + 1, x["team_name"], x["points"])
        msg += (
            gold_emoji + "\n"
            if q == 0
            else (
                silver_emoji + "\n"
                if q == 1
                else (bronze_emoji + "\n" if q == 2 else "\n")
            )
        )
        q += 1
    await e.reply(msg)


@new_cmd(pattern="team")
async def _team(e):
    team = get_team_name(e.chat_id)
    if team:
        points = get_team_points(team)
        await e.reply(
            "Your team name is **{}**\n\nQrPoints: **{}**".format(team, points),
            buttons=[[Button.inline("Edit Team Name", b"set_team_name")]],
        )
    else:
        await e.reply("You have not set a team name yet. Use `/start` to set one.")


@new_inline(pattern="set_team_name")
async def set_team_name(e):
    async with e.client.conversation(e.chat, timeout=600) as conv:
        await conv.send_message("Please enter your team name:")
        team_name = await conv.get_response()
        already, lead = is_team_exists(team_name=team_name.text)
        if already:
            await conv.send_message("Request sent to the Team Leader, Please wait.")
            await e.client.send_message(
                lead,
                "[{}]({}) wants to join your team. Do you want to add him/her?".format(
                    e.chat.first_name, e.chat.username
                ),
                buttons=[
                    [
                        Button.inline("Yes ✅", data="add_{}".format(e.chat_id)),
                        Button.inline("No ❌", data="no"),
                    ]
                ],
            )
            return
        msg = await conv.send_message(
            "**{}** is your team name. Is this correct?".format(team_name.text),
            buttons=[Button.inline("Yes ✅", b"yes"), Button.inline("No ❌", b"no")],
        )
        response = await conv.wait_event(events.CallbackQuery)
        if response.data == b"yes":
            await conv.send_message("Great!")
            await msg.delete()
            add_new_team(e.chat_id, team_name.text)
        else:
            await conv.send_message("Oops, let's try again.")
            set_team_name(e)


@new_inline(pattern="add_(.*)")
async def add_to_team(e):
    to_add = int(e.data.decode().split("_")[1])
    team = get_team_name(e.chat_id)
    if team:
        add_member_to_team(team, to_add)
        await e.client.send_message(
            to_add,
            "You have been added to **{}** team.".format(team),
            buttons=[
                [
                    Button.inline("Check Points", b"check_points"),
                ],
            ],
        )
        await e.edit("Team member added.")
    else:
        await e.answer("Team not found.")


@new_inline(pattern="no")
async def no_add_to_team(e):
    await e.edit("Request declined.")


@new_inline(pattern="check_points")
async def check_points(e):
    team = get_team_name(e.chat_id)
    if team:
        points = get_team_points(team)
        await e.edit(
            "Your team name is **{}**\n\nQrPoints: **{}**".format(team, points),
            buttons=[[Button.inline("Back", b"back")]],
        )
    else:
        await e.edit("You have not set a team name yet. Use `/start` to set one.")


@new_cmd(pattern="qr")
async def qr_cmd(e):
    try:
        hexCode = e.text.split(" ")[1]
    except IndexError:
        await e.reply("Please provide the unique QR code.")
        return
    team = get_chat_team(e.chat_id)
    if not team:
        await e.reply(
            "You have not Entered your team name yet. Use `/start` to set one."
        )
        return
    scan = await add_new_qr_team_return_points(hexCode, team)
    if scan == -1:
        await e.reply("Sorry, that QR code is invalid.")

    if scan == 10:
        await e.reply(
            "Congratulations! You are the first team to scan this QR code. You have been awarded **10** points."
        )
        return

    if scan == 8:
        await e.reply(
            "Congo! You are the second team to scan this QR code. You have been awarded **8** points."
        )
        return

    if scan == 6:
        await e.reply(
            "Good job! You are the third team to scan this QR code. You have been awarded **6** points."
        )
        return

    if scan == 5:
        await e.reply(
            "Ouch! Top 3 teams have already scanned this QR code. You have been awarded **5** points."
        )
        return
