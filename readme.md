# 🦸‍♂️ DevOps Hero: Terminal Quest

Welcome to **DevOps Terminal Quest** — a web-based interactive game that helps you learn and practice essential Linux and DevOps commands in a fun, challenge-based format.

## 🎯 Objective

Type the correct Linux/DevOps command for each mission. Progress through stages, earn points, and climb the leaderboard!

---

## 🌟 Features

- ✅ Realistic terminal-like interface
- 📦 Flask backend with mission logic
- 🔐 Session-based score tracking
- 🎮 Missions on:
  - Nginx restart
  - Disk/memory check
  - Permissions
  - Logs
  - Process management
  - File handling
- 📊 Leaderboard system
- ☁️ Built for DevOps learners & enthusiasts

---

## 📁 Project Structure

```bash
.
├── app.py                 # Flask application
├── mission.json           # All command missions
├── leaderboard.json       # Stores top scores
├── templates/
│   ├── index.html
│   ├── game.html
│   ├── complete.html
│   └── leaderboard.html
├── static/
│   └── styles.css         # Optional styles
└── README.md
