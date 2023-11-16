from random import choice
from .db import get_chat_team, new_qr_scan, set_new_qr

normal_qr = [
    "Congratulations, your team just scored a point!",
    "Hooray! Your team has earned a point!",
    "Wow, your team just added a point to the scoreboard!",
    "Well done, your team has earned a valuable point!",
    "Amazing, your team just got a point on the board!",
]
hidden_qr = [
    "Congratulations, you've discovered the hidden QR code, earning your team 3 points!",
    "Well done, your team just found the hidden QR code and won 3 points!",
    "Excellent work, your team has earned 3 points by uncovering the hidden QR code!",
    "Impressive, your team has just gained 3 points by uncovering the hidden QR code!",
]

with open("qr_links.txt", "r") as f:
    import json

    qr_links = json.loads(f.read())
    for i in qr_links:
        print(i)
        set_new_qr(i, "normal")


async def onNewQR(e):
    m = await e.reply("Analyzing QR code...")
    try:
        qr_hex = e.text.split("qr_")[1]
    except IndexError:
        await m.edit("Some Error, Please provide the unique QR code.")
        return

    team = await get_chat_team(e.chat_id)
    if not team:
        await m.edit("You are not in a team. Use `/start` to set one.")
        return

    m = await m.edit("Team: **{}**, Analyzing QR code...".format(team))
    scan = await new_qr_scan(qr_hex, team)

    print(scan)
