from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["debris_deputy"]
collection = db["reports"]


# 📊 Get all reports
def get_all_reports():
    reports = collection.find()

    for report in reports:
        print(report)


# 📊 Get only pending reports
def get_pending_reports():
    reports = collection.find({"status": "pending"})

    for report in reports:
        print(report)


# 📊 Get reports by location (example)
def get_reports_by_location(lat, lng):
    reports = collection.find({
        "location.lat": lat,
        "location.lng": lng
    })

    for report in reports:
        print(report)


# 🔥 Test
print("---- ALL REPORTS ----")
get_all_reports()

print("\n---- PENDING REPORTS ----")
get_pending_reports()