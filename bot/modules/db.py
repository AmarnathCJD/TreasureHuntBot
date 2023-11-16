from pymongo import MongoClient

mdb = MongoClient(
    "mongodb+srv://user:user@cluster0.1vyhuye.mongodb.net/?retryWrites=true&w=majority"
)

db = mdb["mvh"]

print(list(db["teams"].find()))


def reset_qrs():
    db["qr"].delete_one({"qr_type": 1})
    db["qr"].update_many({}, {"$set": {"teams": []}})


def reset_teams():
    db["teams"].update_many({}, {"$set": {"points": 0, "last_qr_type": 0}})

def purge_teams():
    db["teams"].delete_many({})


def is_team_exists(team_name):
    team = db["teams"].find_one({"team_name": team_name})
    if team:
        return True, team["chat_id"]
    else:
        return False, None


def add_member_to_team(team_name, chat_id):
    db["teams"].update_one({"team_name": team_name}, {"$push": {"members": chat_id}})


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
        for team in db["teams"].find():
            if chat_id in team["members"]:
                return team

        return None


def remove_member_from_team(chat_id):
    db["teams"].update_one({"members": chat_id}, {"$pull": {"members": chat_id}})


def get_team_name(chat_id):
    team = db["teams"].find_one({"chat_id": chat_id})
    if team:
        return team["team_name"]
    else:
        for team in db["teams"].find():
            if chat_id in team["members"]:
                return team["team_name"]

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


def increment_team_points(team_name, points):
    db["teams"].update_one(
        {"team_name": team_name}, {"$inc": {"points": points}}, upsert=True
    )


def add_new_qr(qr_id, qr_type):
    db["qr"].update_one(
        {"qr_id": qr_id}, {"$set": {"qr_type": qr_type, "teams": []}}, upsert=True
    )


def add_new_qr_team_return_points(qr_id, team_name):
    qr = db["qr"].find_one({"qr_id": qr_id})
    if qr:
        if team_name in qr["teams"]:
            return -2, qr["qr_type"]
        else:
            if get_team_last_scan_qr_type(team_name) + 1 != qr["qr_type"]:
                return -3, qr["qr_type"]
            db["qr"].update_one({"qr_id": qr_id}, {"$push": {"teams": team_name}})
            qr = db["qr"].find_one({"qr_id": qr_id})
            set_team_last_scan_qr_type(team_name, qr["qr_type"])
            teams = qr["teams"]
            if len(teams) == 1:
                increment_team_points(team_name, 10)
                return 10, qr["qr_type"]
            elif len(teams) == 2:
                increment_team_points(team_name, 8)
                return 8, qr["qr_type"]
            elif len(teams) == 3:
                increment_team_points(team_name, 6)
                return 6, qr["qr_type"]
            else:
                increment_team_points(team_name, 5)
                return 5, qr["qr_type"]
    else:
        return -1, 1


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


def get_all_qr():
    return db["qr"].find()


def set_team_last_scan_qr_type(team_name, qr_type):
    db["teams"].update_one(
        {"team_name": team_name}, {"$set": {"last_qr_type": qr_type}}, upsert=True
    )


def get_team_last_scan_qr_type(team_name):
    team = db["teams"].find_one({"team_name": team_name})
    if team:
        t = team.get("last_qr_type", 1)
        if t != 0:
            return t
        else:
            return 1
    else:
        return 1
