from flask import jsonify

bots = [{"id": "97832", "name": "Pixie", "description": "Your creative companion for inspiration and personalized assistance.",
         "avatar_image": "https://lh3.googleusercontent.com/u/0/drive-viewer/AITFw-xYqLiLXXcNX_X-ZHpGTiH9lEpjaqVj-O4GeK9T0yjfERg6LvEDWs4f0vNcoyc8jiYDkKJ_Ihd9LznWcH5cjS2Q7mLrCg=w1920-h876"},
        {"id": "97831", "name": "Bruce", "description": "Simplifying tasks and providing instant solutions with a touch of personality",
         "avatar_image": "https://lh3.googleusercontent.com/u/0/drive-viewer/AITFw-zhnVZTh-wXGtax_FyF2HpmCp_e2t5H7TH7VoCdONpY-EFqW8857h-iH8zDI5p1VypXNeVi9PIoMPVR6I4khggJk_Ad3Q=w1175-h876"},
        {"id": "97835", "name": "Ana", "description": "A reliable AI partner streamlining your workflow and enhancing productivity",
         "avatar_image": "https://lh3.googleusercontent.com/u/0/drive-viewer/AITFw-zK9j_Ifc8H80W1CwXGXT8qCr1kNta2LnlX8Gx8PM_SZmDEPTFcQF3fb4yZREYEpEfiSij5JKGoG-s87JMDvMAb5Xo0SA=w1920-h876"}]


def get_avatars():
    return jsonify({
        "bots": bots
    })


def get_bot_name_by_bot_id(bot_id: str) -> str:
    for bot in bots:
        if bot["id"] == bot_id:
            return bot["name"]
    return "bot"

