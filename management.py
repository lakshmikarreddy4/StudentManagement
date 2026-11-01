from flask import Blueprint, render_template, request, redirect, session
from database import get_db

management_bp = Blueprint("management", __name__)

@management_bp.route("/students")
def students():

    if "student_id" not in session:
        return redirect("/login")

    with get_db() as con:
        student = con.execute(
            "SELECT * FROM students WHERE id = ?",
            (session["student_id"],)
        ).fetchone()

    if student is None:
        session.clear()
        return redirect("/login")

    return render_template("students.html", student=student)


@management_bp.route("/update", methods=["POST"])
def update():

    if "student_id" not in session:
        return redirect("/login")

    name = request.form["name"].strip()
    department = request.form["department"].strip()

    if not name or not department:
        return "All fields are required", 400

    with get_db() as con:
        con.execute("""
            UPDATE students
            SET name = ?, department = ?
            WHERE id = ?
        """, (name, department, session["student_id"]))

    return redirect("/students")


@management_bp.route("/delete", methods=["POST"])
def delete():

    if "student_id" not in session:
        return redirect("/login")

    with get_db() as con:
        con.execute(
            "DELETE FROM students WHERE id = ?",
            (session["student_id"],)
        )

    session.clear()
    return redirect("/")