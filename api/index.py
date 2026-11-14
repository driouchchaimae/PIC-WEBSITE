from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="templates")

MOLECULES_DB = {
    "ethanol": {
        "groupes": {"-CH3": 1, "-CH2-": 1, "-OH (alcool)": 1},
        "xyz": "9\nEthanol\nC -0.047 0.663 0.000\nC -1.213 -0.312 0.000\nO 1.158 -0.092 0.000\nH -0.056 1.312 0.882\nH -0.056 1.312 -0.882\nH -2.156 0.239 0.000\nH -1.196 -0.955 0.883\nH -1.196 -0.955 -0.883\nH 1.915 0.506 0.000"
    },
    "éthanol": {
        "groupes": {"-CH3": 1, "-CH2-": 1, "-OH (alcool)": 1},
        "xyz": "9\nEthanol\nC -0.047 0.663 0.000\nC -1.213 -0.312 0.000\nO 1.158 -0.092 0.000\nH -0.056 1.312 0.882\nH -0.056 1.312 -0.882\nH -2.156 0.239 0.000\nH -1.196 -0.955 0.883\nH -1.196 -0.955 -0.883\nH 1.915 0.506 0.000"
    },
    "benzene": {
        "groupes": {"=CH- (aromatique)": 6},
        "xyz": "12\nBenzene\nC 0.000 1.396 0.000\nC 1.209 0.698 0.000\nC 1.209 -0.698 0.000\nC 0.000 -1.396 0.000\nC -1.209 -0.698 0.000\nC -1.209 0.698 0.000\nH 0.000 2.479 0.000\nH 2.147 1.240 0.000\nH 2.147 -1.240 0.000\nH 0.000 -2.479 0.000\nH -2.147 -1.240 0.000\nH -2.147 1.240 0.000"
    },
    "acetone": {
        "groupes": {"-CH3": 2, ">C=O (cétone)": 1},
        "xyz": "10\nAcetone\nC 0.000 0.186 0.000\nO 0.000 1.402 0.000\nC -1.286 -0.608 0.000\nC 1.286 -0.608 0.000\nH -2.155 0.052 0.000\nH -1.321 -1.253 0.882\nH -1.321 -1.253 -0.882\nH 2.155 0.052 0.000\nH 1.321 -1.253 0.882\nH 1.321 -1.253 -0.882"
    },
    "methanol": {
        "groupes": {"-CH3": 1, "-OH (alcool)": 1},
        "xyz": "6\nMethanol\nC -0.047 0.663 0.000\nO 1.158 -0.092 0.000\nH -0.056 1.312 0.882\nH -0.056 1.312 -0.882\nH -0.950 0.050 0.000\nH 1.915 0.506 0.000"
    }
}

CONTRIBUTIONS = {
    "-CH3": 23.58,
    "-CH2-": 22.88,
    "-OH (alcool)": 92.88,
    "=CH- (aromatique)": 26.73,
    ">C=O (cétone)": 76.75
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api", methods=["POST", "OPTIONS"])
@app.route("/api/<path:subpath>", methods=["POST", "OPTIONS"])
def handle_api(subpath=""):
    if request.method == "OPTIONS":
        return ("", 204)

    data = request.get_json(silent=True) or {}
    nom = str(data.get("nom", "")).strip().lower()

    if not nom:
        return jsonify({"success": False, "erreur": "Veuillez saisir le nom d'une molécule."}), 400

    if nom in MOLECULES_DB:
        mol = MOLECULES_DB[nom]
        groupes = mol["groupes"]
        tb = round(198.2 + sum(CONTRIBUTIONS[g] * n for g, n in groupes.items()), 2)
        groupes_str = ", ".join(f"{n}x {g}" for g, n in groupes.items())

        return jsonify({
            "success": True,
            "nom": nom,
            "groupes": groupes_str,
            "temperature": tb,
            "tb_kelvin": tb,
            "tb_celsius": round(tb - 273.15, 2),
            "xyz": mol["xyz"]
        })

    return jsonify({
        "success": False,
        "erreur": f"Molécule '{nom}' non trouvée. Essayez : ethanol, methanol, benzene ou acetone."
    }), 404

   
        
    

    
            
