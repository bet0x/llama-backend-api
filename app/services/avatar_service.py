from flask import jsonify

bots = [{"id": "97832", "name": "Pixie", "description": "Your creative companion for inspiration and personalized assistance.",
         "avatar_image": "https://lh3.googleusercontent.com/drive-viewer/AITFw-ztDPQsnjvnlzSr0RTgpoWy8i2mfJVjgIkZhze3lqxHMiHppmcfGOcsbVVEJ54jfABYIfxMAmfw7aQ3ZhHoCw0qpqZrYw=w944-h929"},
        {"id": "97831", "name": "Bruce", "description": "Simplifying tasks and providing instant solutions with a touch of personality",
         "avatar_image": "https://lh3.googleusercontent.com/drive-viewer/AITFw-zNIVKeHKHIOI6upJjXeCDowKc0rXsXe76HA1V_3rF0pyaw6KYBQXYApnOWzV4Xi2W6qF4069HEpIsB2nj2wPof7kOX0Q=w630-h929"},
        {"id": "97835", "name": "Ana", "description": "A reliable AI partner streamlining your workflow and enhancing productivity",
         "avatar_image": "https://lh3.googleusercontent.com/drive-viewer/AITFw-wJWlNxOOnqWiIiAbBLXcBZNzZjq-89NL05OeHryjbVuVHxpuEA4Ahen_qCkDATxG9qTRiO_qeIDowQkGXRKOky3ynbww=w379-h929"}]


def get_avatars():
    return jsonify({
        "bots": bots
    })


def get_bot_name_by_bot_id(bot_id: str) -> str:
    for bot in bots:
        if bot["id"] == bot_id:
            return bot["name"]
    return "bot"

