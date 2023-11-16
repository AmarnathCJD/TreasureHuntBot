from pymongo import MongoClient

mdb = MongoClient(
    "mongodb+srv://user:user@cluster0.1vyhuye.mongodb.net/?retryWrites=true&w=majority"
)

db = mdb["mvh"]


def add_new_team(chat_id, team_name):
    db["teams"].update_one(
        {"chat_id": chat_id},
        {"$set": {"team_name": team_name, "points": 0}},
        upsert=True,
    )


def get_chat_team(chat_id):
    team = db["teams"].find_one({"chat_id": chat_id})
    if team:
        return team
    else:
        return None


def get_team_name(chat_id):
    team = db["teams"].find_one({"chat_id": chat_id})
    if team:
        return team["team_name"]
    else:
        return None


def get_team_points(team_name):
    team = db["teams"].find_one({"team_name": team_name})
    if team:
        return team["points"]
    else:
        return None


def edit_chat_team(chat_id, new_name):
    db["teams"].update_one(
        {"chat_id": chat_id}, {"$set": {"team_name": new_name}}, upsert=True
    )


def increment_chat_point(chat_id, points):
    db["teams"].update_one(
        {"chat_id": chat_id}, {"$inc": {"points": points}}, upsert=True
    )


def add_new_qr(qr_id, qr_type):
    db["qr"].update_one({"qr_id": qr_id}, {"$set": {"qr_type": qr_type}}, upsert=True)


def add_new_qr_team_return_points(qr_id, team_name):
    qr = db["qr"].find_one({"qr_id": qr_id})
    if qr:
        if team_name in qr["teams"]:
            return -2  # Already scanned
        else:
            db["qr"].update_one({"qr_id": qr_id}, {"$push": {"teams": team_name}})
            qr = db["qr"].find_one({"qr_id": qr_id})
            teams = qr["teams"]
            if len(teams) == 1:
                return 10  # Top 1
            elif len(teams) == 2:
                return 8  # Top 2
            elif len(teams) == 3:
                return 6  # Top 3
            else:
                return 5  # Top 3 already scanned
    else:
        return -1  # Invalid QR


def get_qr_type(qr_id):
    qr = db["qr"].find_one({"qr_id": qr_id})
    if qr:
        return qr["qr_type"]
    else:
        return None


def get_qr_teams(qr_id):
    qr = db["qr"].find_one({"qr_id": qr_id})
    if qr:
        return qr["teams"]
    else:
        return None


def generate_leaderboard():
    return db["teams"].find().sort("points", -1)
