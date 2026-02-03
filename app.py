from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.collegeDB
collection = db.students

@app.route("/")
def index():
    students = []
    for student in collection.find():
        students.append({
            "_id": str(student["_id"]),
            "name": student["name"],
            "age": student["age"],
            "email": student["email"],
            "course": student["course"]
        })
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    age = int(request.form["age"])
    email = request.form["email"]
    course = request.form["course"]

    collection.insert_one({
        "name": name,
        "age": age,
        "email": email,
        "course": course
    })
    return redirect(url_for("index"))

@app.route("/delete/<student_id>")
def delete_student(student_id):
    collection.delete_one({"_id": ObjectId(student_id)})
    return redirect(url_for("index"))

@app.route("/edit/<student_id>")
def edit_student(student_id):
    student = collection.find_one({"_id": ObjectId(student_id)})
    student["_id"] = str(student["_id"])
    return render_template("edit.html", student=student)

@app.route("/update/<student_id>", methods=["POST"])
def update_student(student_id):
    name = request.form["name"]
    age = int(request.form["age"])
    email = request.form["email"]
    course = request.form["course"]

    collection.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": {"name": name, "age": age, "email": email, "course": course}}
    )
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
