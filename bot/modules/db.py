
POINTS = [10, 8, 6, 5]

from firebase_admin import firestore, credentials
import firebase_admin
import time

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def generate_leaderboard():
    pass

async def set_team(name, chat_id):
    doc_ref = db.collection("TeamNames").document("tName")
    doc_ref.set({
        str(chat_id) : name
    },merge=True)

    doc_ref = db.collection("Teams").document(name)
    doc_ref.set({
        'Team Created': time.strftime("%H:%M:%S", time.localtime()),
        'Points' : 0   
    },merge=True)

async def get_chat_team(chat_id):
    doc_ref = db.collection("TeamNames").document("tName")
    doc = doc_ref.get()
    if doc.exists and str(chat_id) in doc.to_dict():
        return doc.to_dict()[str(chat_id)]
    else:
        return None
    
async def get_team_points(team_name):
    doc_ref = db.collection("Teams").document(team_name)
    doc = doc_ref.get()
    if doc.exists and "Points" in doc.to_dict():
        return doc.to_dict()["Points"]
    else:
        return None
    
async def edit_chat_team(chat_id, new_name):
    doc_ref = db.collection("TeamNames").document("tName")
    doc_ref.set({
        str(chat_id) : new_name
    },merge=True)

async def update_team_points(team_name, points):
    doc_ref = db.collection("Teams").document(team_name)
    doc_ref.set({
        'Points' : points
    },merge=True)

async def add_team_points(team_name, points):
    doc_ref = db.collection("Teams").document(team_name)
    doc_ref.set({
        'Points' : firestore.Increment(points)
    },merge=True)

async def set_new_qr(qr_id, qr_type):
    doc_ref = db.collection("QR").document(qr_id)
    doc_ref.set({
        'Type' : qr_type,
        'Teams' : []
    },merge=True)

async def new_qr_scan(qr_id, team_name) -> [int, str]:
    doc_ref = db.collection("QR").document(qr_id)
    doc = doc_ref.get()
    print(doc.to_dict())
    if doc.exists:
        doc_data = doc.to_dict()
        doc_ref.set({
            'Teams' : firestore.ArrayUnion([team_name])
        }, merge=True)
        teams = doc_data.get("Teams")
        qr_type = doc_data.get("Type")
        if teams:
            if team_name in teams:
                ranking = teams.index(team_name)
                if ranking < len(POINTS):
                    return POINTS[ranking], qr_type
                else:
                    return POINTS[-1], qr_type
            else:
                return -1, qr_type
        else:
            return -1, qr_type
    else:
        return -1, None
