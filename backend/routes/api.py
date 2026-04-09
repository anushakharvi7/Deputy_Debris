from flask import Blueprint, jsonify, request
from models.db import db
from datetime import datetime, timedelta

api = Blueprint("api", __name__)

# ✅ Test API
@api.route("/test", methods=["GET"])
def test_api():
    return jsonify({"message": "Backend is working!"})


# ✅ Feedback API (with DND logic)
@api.route("/feedback", methods=["POST"])
def feedback():
    data = request.json

    if not data:
        return jsonify({"error": "No data received"}), 400

    response = data.get("response")

    if response not in ["yes", "no"]:
        return jsonify({"error": "Invalid response"}), 400

    feedback_data = {
        "response": response,
        "timestamp": datetime.utcnow()
    }

    # Save feedback
    db.feedback.insert_one(feedback_data)

    # 🔕 DND logic
    if response == "no":
        dnd_time = datetime.utcnow() + timedelta(minutes=10)

        db.settings.update_one(
            {},
            {"$set": {"dnd_until": dnd_time}},
            upsert=True
        )

    return jsonify({"message": "Feedback saved successfully!"})


# ✅ Check if alert should be shown
@api.route("/should-alert", methods=["GET"])
def should_alert():
    settings = db.settings.find_one()

    if not settings or "dnd_until" not in settings:
        return jsonify({"alert": True})

    if datetime.utcnow() < settings["dnd_until"]:
        return jsonify({"alert": False})

    return jsonify({"alert": True})


# ✅ Check DND status
@api.route("/check-dnd", methods=["GET"])
def check_dnd():
    settings = db.settings.find_one()

    if not settings or "dnd_until" not in settings:
        return jsonify({"dnd": False})

    if datetime.utcnow() < settings["dnd_until"]:
        return jsonify({"dnd": True})

    return jsonify({"dnd": False})


# ✅ Get all feedbacks
@api.route("/feedbacks", methods=["GET"])
def get_feedbacks():
    feedbacks = list(db.feedback.find({}, {"_id": 0}))
    return jsonify(feedbacks)