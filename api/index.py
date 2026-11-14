
from flask import Flask, request, jsonify, render_template
from .temperature import calculer_ebullition, JOBACK_TB_CONTRIBUTIONS

app = Flask(__name__, template_folder="templates")

# Base d'utilisateurs autorisés (Identifiant : Mot de passe)
USERS = {
    "admin": "pic2026",
    "etudiant1": "chimie123",
    "user": "password"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    if username in USERS and USERS[username] == password:
        return jsonify({"success": True, "username": username})
    return jsonify({"success": False, "message": "Identifiant ou mot de passe incorrect"}), 401

@app.route("/api/groups", methods=["GET"])
def get_groups():
    return jsonify(list(JOBACK_TB_CONTRIBUTIONS.keys()))

@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.json
    groupes = data.get("groupes", {})
    tb_k = calculer_ebullition(groupes)
    tb_c = round(tb_k - 273.15, 2)
    return jsonify({"tb_kelvin": tb_k, "tb_celsius": tb_c})
           
   
