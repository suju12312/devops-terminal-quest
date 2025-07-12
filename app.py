from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = "super-secret"

# Load missions from file
with open("mission.json") as f:
    MISSIONS = json.load(f)

LEADERBOARD_FILE = "leaderboard.json"

# Leaderboard functions
def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE) as f:
        return json.load(f)

def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Home route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["player"] = request.form["name"]
        session["score"] = 0
        session["attempts"] = {}
        return redirect(url_for("game"))
    return render_template("index.html")

# Game screen
@app.route("/game")
def game():
    if "player" not in session:
        return redirect(url_for("index"))
    return render_template("game.html", missions=MISSIONS)

# Command verifier
@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    mission_id = str(data["mission_id"])
    cmd = data["command"].strip()

    mission = next((m for m in MISSIONS if str(m["id"]) == mission_id), None)
    if mission is None:
        return jsonify({"result": "error", "message": "Invalid mission", "score": session.get("score", 0)})

    # Ensure attempts exist
    if "attempts" not in session:
        session["attempts"] = {}

    attempts = session["attempts"].get(mission_id, 0)

    # Already completed
    if attempts >= 3:
        return jsonify({
            "result": "locked",
            "message": f"✅ Mission already completed. Correct command was: {mission['solution']}",
            "score": session["score"]
        })

    # Correct command
    if cmd == mission["solution"]:
        session["score"] += mission.get("points", 10)
        session["attempts"][mission_id] = 3
        session.modified = True
        return jsonify({
            "result": "success",
            "message": "✅ Correct command!",
            "score": session["score"]
        })

    # Wrong answer flow
    attempts += 1
    session["attempts"][mission_id] = attempts
    session.modified = True

    if attempts == 1:
        return jsonify({
            "result": "try_again",
            "message": "❌ Try again!",
            "score": session["score"]
        })
    elif attempts == 2:
        session["score"] -= 5
        session.modified = True
        return jsonify({
            "result": "hint",
            "message": f"🔍 Hint: command starts with {mission['solution'].split()[0]}",
            "score": session["score"]
        })
    else:
        return jsonify({
            "result": "show_answer",
            "message": f"❌ Correct command was: {mission['solution']}",
            "score": session["score"]
        })

# Completion screen
@app.route("/complete")
def complete():
    name = session.get("player")
    score = session.get("score", 0)

    leaderboard = load_leaderboard()

    # Check if player already exists
    existing = next((entry for entry in leaderboard if entry["name"] == name), None)

    if existing:
        if score > existing["score"]:
            existing["score"] = score  # Keep the better score
    else:
        leaderboard.append({"name": name, "score": score})

    # Sort and trim top 10
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
    save_leaderboard(leaderboard)

    return render_template("complete.html", score=score)


# Leaderboard screen
@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html", leaderboard=load_leaderboard())

if __name__ == "__main__":
    app.run(debug=True)