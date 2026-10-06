from flask import Flask, request, redirect, render_template_string
import sqlite3
from datetime import date

app = Flask(__name__)
DB = "campus.db"


# ---------------- DATABASE ----------------

def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            year TEXT NOT NULL,
            phone TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            expense_date TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_name TEXT NOT NULL,
            person_type TEXT NOT NULL,
            status TEXT NOT NULL,
            attendance_date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- HTML ----------------

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Campus Management System</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f1f5f9;
    color: #1e293b;
}

/* NAVBAR */

nav {
    background: linear-gradient(135deg,#172554,#2563eb);
    color: white;
    padding: 18px 5%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
}

.logo {
    font-size: 24px;
    font-weight: bold;
}

nav a {
    color: white;
    text-decoration: none;
    margin: 8px;
    font-size: 14px;
}

nav a:hover {
    color: #bfdbfe;
}

/* MAIN */

.container {
    width: 90%;
    max-width: 1200px;
    margin: 30px auto;
}

/* HERO */

.hero {
    background: linear-gradient(135deg,#1e3a8a,#3b82f6);
    color: white;
    padding: 45px;
    border-radius: 18px;
    margin-bottom: 30px;
}

.hero h1 {
    font-size: 38px;
    margin-bottom: 10px;
}

/* CARDS */

.cards {
    display: grid;
    grid-template-columns: repeat(4,1fr);
    gap: 20px;
    margin-bottom: 30px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,.08);
}

.card h2 {
    font-size: 32px;
    color: #2563eb;
    margin: 5px;
}

/* FORM */

.box {
    background: white;
    padding: 25px;
    border-radius: 14px;
    margin-bottom: 25px;
    box-shadow: 0 4px 12px rgba(0,0,0,.08);
}

input, select {
    width: 100%;
    padding: 12px;
    margin: 7px 0 15px;
    border: 1px solid #cbd5e1;
    border-radius: 7px;
}

button {
    background: #2563eb;
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 7px;
    cursor: pointer;
}

button:hover {
    background: #1d4ed8;
}

/* TABLE */

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
}

th, td {
    padding: 13px;
    border-bottom: 1px solid #e2e8f0;
    text-align: left;
}

th {
    background: #eff6ff;
    color: #1e3a8a;
}

.delete {
    color: #dc2626;
    text-decoration: none;
}

/* STATUS */

.present {
    color: green;
    font-weight: bold;
}

.absent {
    color: red;
    font-weight: bold;
}

/* FOOTER */

footer {
    text-align: center;
    padding: 25px;
    color: #64748b;
}

/* MOBILE */

@media(max-width:800px) {

    .cards {
        grid-template-columns: repeat(2,1fr);
    }

    nav {
        flex-direction: column;
    }

}

@media(max-width:500px) {

    .cards {
        grid-template-columns: 1fr;
    }

    .hero h1 {
        font-size: 28px;
    }

    table {
        font-size: 12px;
    }

}

</style>
</head>

<body>

<nav>

<div class="logo">
🎓 Campus Management
</div>

<div>
<a href="/">Dashboard</a>
<a href="/students">Students</a>
<a href="/staff">Staff</a>
<a href="/salary">Salary</a>
<a href="/expenses">Expenses</a>
<a href="/attendance">Attendance</a>
</div>

</nav>


<div class="container">

{% if page == "dashboard" %}

<div class="hero">

<h1>Campus Management System</h1>

<p>
Complete management system for students, staff,
salary, expenses and attendance.
</p>

</div>


<div class="cards">

<div class="card">
<h2>{{ students }}</h2>
<p>👨‍🎓 Students</p>
</div>

<div class="card">
<h2>{{ staff }}</h2>
<p>👨‍🏫 Staff</p>
</div>

<div class="card">
<h2>₹{{ salary }}</h2>
<p>💰 Monthly Salary</p>
</div>

<div class="card">
<h2>₹{{ expenses }}</h2>
<p>💸 Total Expenses</p>
</div>

</div>


<div class="box">

<h2>📊 Campus Overview</h2>

<p>
The system manages student records, staff information,
salary payments, campus expenses and daily attendance.
</p>

</div>


{% elif page == "students" %}

<div class="box">

<h2>👨‍🎓 Student Management</h2>

<form method="POST" action="/add_student">

<input name="name" placeholder="Student Name" required>

<input name="department" placeholder="Department" required>

<select name="year" required>

<option value="">Select Year</option>
<option>1st Year</option>
<option>2nd Year</option>
<option>3rd Year</option>
<option>4th Year</option>

</select>

<input name="phone" placeholder="Phone Number">

<button>Add Student</button>

</form>

</div>


<div class="box">

<h2>Student Records</h2>

<table>

<tr>
<th>ID</th>
<th>Name</th>
<th>Department</th>
<th>Year</th>
<th>Phone</th>
<th>Action</th>
</tr>

{% for s in data %}

<tr>

<td>{{ s.id }}</td>
<td>{{ s.name }}</td>
<td>{{ s.department }}</td>
<td>{{ s.year }}</td>
<td>{{ s.phone }}</td>

<td>
<a class="delete"
href="/delete_student/{{ s.id }}">
Delete
</a>
</td>

</tr>

{% endfor %}

</table>

</div>


{% elif page == "staff" %}

<div class="box">

<h2>👨‍🏫 Staff Management</h2>

<form method="POST" action="/add_staff">

<input name="name" placeholder="Staff Name" required>

<input name="role" placeholder="Role (Professor / Admin)" required>

<input name="department" placeholder="Department" required>

<input name="salary" type="number"
placeholder="Monthly Salary" required>

<button>Add Staff</button>

</form>

</div>


<div class="box">

<h2>Staff Records</h2>

<table>

<tr>
<th>ID</th>
<th>Name</th>
<th>Role</th>
<th>Department</th>
<th>Salary</th>
<th>Action</th>
</tr>

{% for s in data %}

<tr>

<td>{{ s.id }}</td>
<td>{{ s.name }}</td>
<td>{{ s.role }}</td>
<td>{{ s.department }}</td>
<td>₹{{ s.salary }}</td>

<td>
<a class="delete"
href="/delete_staff/{{ s.id }}">
Delete
</a>
</td>

</tr>

{% endfor %}

</table>

</div>


{% elif page == "salary" %}

<div class="box">

<h2>💰 Salary Management</h2>

<table>

<tr>
<th>Staff</th>
<th>Role</th>
<th>Department</th>
<th>Monthly Salary</th>
</tr>

{% for s in data %}

<tr>
<td>{{ s.name }}</td>
<td>{{ s.role }}</td>
<td>{{ s.department }}</td>
<td>₹{{ s.salary }}</td>
</tr>

{% endfor %}

</table>

</div>


{% elif page == "expenses" %}

<div class="box">

<h2>💸 Expense Management</h2>

<form method="POST" action="/add_expense">

<input name="title"
placeholder="Expense Title" required>

<select name="category" required>

<option value="">Category</option>
<option>Electricity</option>
<option>Maintenance</option>
<option>Equipment</option>
<option>Transport</option>
<option>Events</option>
<option>Other</option>

</select>

<input name="amount"
type="number"
step="0.01"
placeholder="Amount" required>

<input name="expense_date"
type="date"
value="{{ today }}"
required>

<button>Add Expense</button>

</form>

</div>


<div class="box">

<h2>Expense Records</h2>

<table>

<tr>
<th>Title</th>
<th>Category</th>
<th>Amount</th>
<th>Date</th>
<th>Action</th>
</tr>

{% for e in data %}

<tr>

<td>{{ e.title }}</td>
<td>{{ e.category }}</td>
<td>₹{{ e.amount }}</td>
<td>{{ e.expense_date }}</td>

<td>
<a class="delete"
href="/delete_expense/{{ e.id }}">
Delete
</a>
</td>

</tr>

{% endfor %}

</table>

</div>


{% elif page == "attendance" %}

<div class="box">

<h2>🕐 Mark Attendance</h2>

<form method="POST" action="/mark_attendance">

<input name="person_name"
placeholder="Student / Staff Name"
required>

<select name="person_type" required>

<option>Student</option>
<option>Staff</option>

</select>

<select name="status" required>

<option>Present</option>
<option>Absent</option>

</select>

<input
name="attendance_date"
type="date"
value="{{ today }}"
required>

<button>Mark Attendance</button>

</form>

</div>


<div class="box">

<h2>Attendance Records</h2>

<table>

<tr>
<th>Name</th>
<th>Type</th>
<th>Status</th>
<th>Date</th>
</tr>

{% for a in data %}

<tr>

<td>{{ a.person_name }}</td>
<td>{{ a.person_type }}</td>

<td class="{{ 'present' if a.status == 'Present' else 'absent' }}">
{{ a.status }}
</td>

<td>{{ a.attendance_date }}</td>

</tr>

{% endfor %}

</table>

</div>

{% endif %}

</div>


<footer>

Campus Management System | CI/CD Project 🚀

</footer>

</body>
</html>
"""


# ---------------- DASHBOARD ----------------

@app.route("/")
def home():

    conn = db()

    students = conn.execute(
        "SELECT COUNT(*) FROM students"
    ).fetchone()[0]

    staff = conn.execute(
        "SELECT COUNT(*) FROM staff"
    ).fetchone()[0]

    salary = conn.execute(
        "SELECT COALESCE(SUM(salary),0) FROM staff"
    ).fetchone()[0]

    expenses = conn.execute(
        "SELECT COALESCE(SUM(amount),0) FROM expenses"
    ).fetchone()[0]

    conn.close()

    return render_template_string(
        HTML,
        page="dashboard",
        students=students,
        staff=staff,
        salary=salary,
        expenses=expenses
    )


# ---------------- STUDENTS ----------------

@app.route("/students")
def students_page():

    conn = db()

    data = conn.execute(
        "SELECT * FROM students ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template_string(
        HTML,
        page="students",
        data=data
    )


@app.route("/add_student", methods=["POST"])
def add_student():

    conn = db()

    conn.execute("""
        INSERT INTO students
        (name, department, year, phone)
        VALUES (?, ?, ?, ?)
    """, (
        request.form["name"],
        request.form["department"],
        request.form["year"],
        request.form["phone"]
    ))

    conn.commit()
    conn.close()

    return redirect("/students")


@app.route("/delete_student/<int:id>")
def delete_student(id):

    conn = db()

    conn.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/students")


# ---------------- STAFF ----------------

@app.route("/staff")
def staff_page():

    conn = db()

    data = conn.execute(
        "SELECT * FROM staff ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template_string(
        HTML,
        page="staff",
        data=data
    )


@app.route("/add_staff", methods=["POST"])
def add_staff():

    conn = db()

    conn.execute("""
        INSERT INTO staff
        (name, role, department, salary)
        VALUES (?, ?, ?, ?)
    """, (
        request.form["name"],
        request.form["role"],
        request.form["department"],
        request.form["salary"]
    ))

    conn.commit()
    conn.close()

    return redirect("/staff")


@app.route("/delete_staff/<int:id>")
def delete_staff(id):

    conn = db()

    conn.execute(
        "DELETE FROM staff WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/staff")


# ---------------- SALARY ----------------

@app.route("/salary")
def salary_page():

    conn = db()

    data = conn.execute(
        "SELECT * FROM staff ORDER BY name"
    ).fetchall()

    conn.close()

    return render_template_string(
        HTML,
        page="salary",
        data=data
    )


# ---------------- EXPENSES ----------------

@app.route("/expenses")
def expenses_page():

    conn = db()

    data = conn.execute(
        "SELECT * FROM expenses ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template_string(
        HTML,
        page="expenses",
        data=data,
        today=date.today().isoformat()
    )


@app.route("/add_expense", methods=["POST"])
def add_expense():

    conn = db()

    conn.execute("""
        INSERT INTO expenses
        (title, category, amount, expense_date)
        VALUES (?, ?, ?, ?)
    """, (
        request.form["title"],
        request.form["category"],
        request.form["amount"],
        request.form["expense_date"]
    ))

    conn.commit()
    conn.close()

    return redirect("/expenses")


@app.route("/delete_expense/<int:id>")
def delete_expense(id):

    conn = db()

    conn.execute(
        "DELETE FROM expenses WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/expenses")


# ---------------- ATTENDANCE ----------------

@app.route("/attendance")
def attendance_page():

    conn = db()

    data = conn.execute("""
        SELECT * FROM attendance
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template_string(
        HTML,
        page="attendance",
        data=data,
        today=date.today().isoformat()
    )


@app.route("/mark_attendance", methods=["POST"])
def mark_attendance():

    conn = db()

    conn.execute("""
        INSERT INTO attendance
        (person_name, person_type, status, attendance_date)
        VALUES (?, ?, ?, ?)
    """, (
        request.form["person_name"],
        request.form["person_type"],
        request.form["status"],
        request.form["attendance_date"]
    ))

    conn.commit()
    conn.close()

    return redirect("/attendance")


# ---------------- START ----------------

init_db()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
