from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = "super-secret"

with open("mission.json") as f:
    MISSIONS = json.load(f)

LEADERBOARD_FILE = "leaderboard.json"

# Load or initialize leaderboard
def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE) as f:
        return json.load(f)

def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["player"] = request.form["name"]
        session["score"] = 0
        session["current"] = 0
        return redirect(url_for("game"))
    return render_template("index.html")

@app.route("/game")
def game():
    if "player" not in session:
        return redirect(url_for("index"))
    return render_template("game.html", missions=MISSIONS)

@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    mission_id = data["mission_id"]
    cmd = data["command"].strip()

    mission = next((m for m in MISSIONS if m["id"] == mission_id), None)

    if mission:
        if cmd == mission["solution"]:
            session["score"] += mission.get("points", 10)
            session["current"] += 1
            return jsonify({
                "result": "success",
                "message": "✅ Correct command!",
                "score": session["score"]
            })
        else:
            session["score"] -= 5  # ⛔ Wrong = -5 points
            return jsonify({
                "result": "fail",
                "message": f"❌ Wrong command! `",
                "score": session["score"]
            })

    return jsonify({"result": "error", "message": "Invalid mission", "score": session["score"]})

@app.route("/complete")
def complete():
    name = session.get("player")
    score = session.get("score", 0)
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
    save_leaderboard(leaderboard)
    return render_template("complete.html", score=score)

@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html", leaderboard=load_leaderboard())

if __name__ == "__main__":
    app.run(debug=True)

