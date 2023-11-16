from random import choice
from .db import add_new_qr_team_return_points, get_team_name

clue_image_map = {
    # 1: "https://envs.sh/uJW.jpg",
    2: "https://envs.sh/uJB.jpg",
    3: "https://envs.sh/uJI.jpg",
    4: "https://envs.sh/uJn.jpg",
    5: "https://envs.sh/uJT.jpg",
    6: "https://envs.sh/uJp.jpg",
    7: "https://envs.sh/uJA.jpg",
    8: "https://envs.sh/uJ_.jpg",
    9: "https://envs.sh/uJj.TBI.jpg",
    10: "https://envs.sh/uJc.RB.jpg",
}


ten_points = [
    "<b>Congratulations!</b> You've just earned <b>10 points</b> for your team!",
    "<b>Well done!</b> You were the first team to scan this QR code, earning <b>10 points</b>!",
    "<b>Excellent work!</b> Your team has just earned <b>10 points</b> by scanning this QR code!",
]

eight_points = [
    "<b>Good job!</b> You were the second team to scan this QR code, earning <b>8 points</b>!",
    "<b>Nice work!</b> You've just earned <b>8 points</b> for your team!",
    "<b>Well done!</b> Your team has just earned <b>8 points</b> by scanning this QR code!",
]

six_points = [
    "<b>Awesome!</b> You were the third team to scan this QR code, earning <b>6 points</b>!",
    "<b>Great work!</b> You've just earned <b>6 points</b> for your team!",
    "<b>Well done!</b> Your team has just earned <b>6 points</b> by scanning this QR code!",
]

five_points = [
    "<i>Aww snap!</i> Top 3 teams have already scanned this QR code. You have been awarded <b>5 points</b>.",
    "<i>Ouch!</i> Top 3 teams have already scanned this QR code. You have been awarded <b>5 points</b>.",
    "<i>Oops!</i> Top 3 teams have already scanned this QR code. You have been awarded <b>5 points</b>.",
]


async def onNewQR(e):
    m = await e.reply("Analyzing QR code...")
    try:
        qr_hex = e.text.split("qr_")[1]
    except IndexError:
        await m.edit("Some Error, Please provide the unique QR code.")
        return

    team = get_team_name(e.chat_id)
    if not team:
        await m.edit("You are not in a team. Enroll using `/start`")
        return

    m = await m.edit("**Team Name: {}**\n`Scanning QR code...`".format(team))
    scan, qr_type = add_new_qr_team_return_points(qr_hex, team)
    if scan == -1:
        await m.edit("Sorry, that QR code is invalid.")
    elif scan == -2:
        image = clue_image_map[qr_type]
        media = (await e.client._file_to_media(image))[1]
        media.spoiler = True
        await m.reply(
            "**You have already scanned this QR code, Here's The Clue:** ", file=media
        )
    elif scan == -3:
        await m.edit(
            "You jumped ahead, Thats **cheating!!!**, First find the previous Clue."
        )
    elif scan == 10:
        if (qr_type == 10):
            await m.respond("Congratulations! You are the awarded **A** WoW")
            return
        await m.edit(choice(ten_points), parse_mode="html")
        media = (await e.client._file_to_media(clue_image_map[qr_type]))[1]
        media.spoiler = True
        await m.reply("**Here's The Clue**", file=media)
    elif scan == 8:
        if (qr_type == 10):
            await m.respond("Congratulations! You are the awarded **B** WoW")
            return
        await m.edit(choice(eight_points), parse_mode="html")
        media = (await e.client._file_to_media(clue_image_map[qr_type]))[1]
        media.spoiler = True
        await m.reply("**Here's The Clue**", file=media)
    elif scan == 6:
        if (qr_type == 10):
            await m.respond("Oops! You are the awarded **C** WoW, Better luck next time")
            return
        await m.edit(choice(six_points), parse_mode="html")
        media = (await e.client._file_to_media(clue_image_map[qr_type]))[1]
        media.spoiler = True
        await m.reply("**Here's The Clue**", file=media)
    elif scan == 5:
        if (qr_type == 10):
            await m.respond("Aww, You finished last, What a shame! You are the awarded **D** WoW")
            return
        await m.edit(choice(five_points), parse_mode="html")
        media = (await e.client._file_to_media(clue_image_map[qr_type]))[1]
        media.spoiler = True
        await m.reply("**Here's The Clue**", file=media)
    else:
        await m.edit("Some Error, Please report this to the Coordinators.")
