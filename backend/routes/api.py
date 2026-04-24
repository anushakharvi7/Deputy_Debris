from flask import Blueprint, jsonify, request
from backend.models.db import db
from datetime import datetime, timedelta
from bson import ObjectId

api = Blueprint("api", __name__)


# ✅ GET ALL REPORTS (FOR FRONTEND)
@api.route("/reports", methods=["GET"])
def get_reports():
    reports = list(db.reports.find())

    formatted = []
    for r in reports:
        formatted.append({
            "id": str(r["_id"]),
            "image": r.get("image_path", ""),
            "location": r.get("location", "Unknown"),
            "status": r.get("status", "Pending").capitalize(),
            "timestamp": r.get("timestamp", "")
        })

    return jsonify(formatted)


# ✅ UPDATE STATUS (YES / NO)
@api.route("/reports/<id>", methods=["PUT"])
def update_report(id):
    data = request.json
    status = data.get("status")

    if status not in ["Confirmed", "Rejected"]:
        return jsonify({"error": "Invalid status"}), 400

    db.reports.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": status}}
    )

    # 🔕 DND logic
    if status == "Rejected":
        dnd_time = datetime.utcnow() + timedelta(minutes=10)

        db.settings.update_one(
            {},
            {"$set": {"dnd_until": dnd_time}},
            upsert=True
        )

    return jsonify({"message": "Status updated"})
from bson.objectid import ObjectId

# UPDATE STATUS
@api.route("/update-status/<id>", methods=["PUT"])
def update_status(id):
    data = request.json
    status = data.get("status")

    db.reports.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"status": status}}
    )

    return jsonify({"message": "Status updated"})