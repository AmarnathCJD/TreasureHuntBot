from random import choice

normal_qr = ['Congratulations, your team just scored a point!','Hooray! Your team has earned a point!','Wow, your team just added a point to the scoreboard!','Well done, your team has earned a valuable point!','Amazing, your team just got a point on the board!']
hidden_qr = ["Congratulations, you've discovered the hidden QR code, earning your team 3 points!","Well done, your team just found the hidden QR code and won 3 points!","Excellent work, your team has earned 3 points by uncovering the hidden QR code!","Impressive, your team has just gained 3 points by uncovering the hidden QR code!"]

def onNewQR(qr_id, qr_type):
    if qr_type == 'normal':
        return choice(normal_qr)
    elif qr_type == 'hidden':
        return choice(hidden_qr)
    else:
        return "Error: Unknown QR type"