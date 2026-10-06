from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

students = [
    {"id": 1, "name": "Arun Kumar", "department": "Computer Science", "year": "3rd Year"},
    {"id": 2, "name": "Priya S", "department": "Information Technology", "year": "2nd Year"},
    {"id": 3, "name": "Rahul M", "department": "Electronics", "year": "4th Year"}
]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Campus Management System</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            color: #1e293b;
        }

        .header {
            background: linear-gradient(135deg, #1e3a8a, #2563eb);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            margin-bottom: 8px;
        }

        .container {
            width: 90%;
            max-width: 1100px;
            margin: 30px auto;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
            text-align: center;
        }

        .card h2 {
            color: #2563eb;
            font-size: 32px;
        }

        .form-box, .table-box {
            background: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }

        input, select {
            padding: 12px;
            margin: 8px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
        }

        button {
            padding: 12px 20px;
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }

        button:hover {
            background: #1d4ed8;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        th, td {
            padding: 14px;
            border-bottom: 1px solid #e2e8f0;
            text-align: left;
        }

        th {
            background: #eff6ff;
            color: #1e3a8a;
        }

        .delete {
            color: white;
            background: #dc2626;
            padding: 7px 12px;
            border-radius: 5px;
            text-decoration: none;
        }

        .footer {
            text-align: center;
            padding: 20px;
            color: #64748b;
        }

        @media(max-width: 700px) {
            .cards {
                grid-template-columns: 1fr;
            }

            input, select {
                width: 90%;
            }
        }
    </style>
</head>

<body>

<div class="header">
    <h1>🎓 Campus Management System</h1>
    <p>Student Management Dashboard</p>
</div>

<div class="container">

    <div class="cards">
        <div class="card">
            <h2>{{ students|length }}</h2>
            <p>Total Students</p>
        </div>

        <div class="card">
            <h2>6</h2>
            <p>Departments</p>
        </div>

        <div class="card">
            <h2>120</h2>
            <p>Faculty Members</p>
        </div>
    </div>

    <div class="form-box">
        <h2>➕ Add Student</h2>

        <form action="/add" method="POST">
            <input type="text" name="name" placeholder="Student Name" required>

            <select name="department" required>
                <option value="">Select Department</option>
                <option>Computer Science</option>
                <option>Information Technology</option>
                <option>Electronics</option>
                <option>Mechanical</option>
                <option>Civil</option>
                <option>Commerce</option>
            </select>

            <select name="year" required>
                <option value="">Select Year</option>
                <option>1st Year</option>
                <option>2nd Year</option>
                <option>3rd Year</option>
                <option>4th Year</option>
            </select>

            <button type="submit">Add Student</button>
        </form>
    </div>

    <div class="table-box">
        <h2>👨‍🎓 Student Records</h2>

        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Department</th>
                <th>Year</th>
                <th>Action</th>
            </tr>

            {% for student in students %}
            <tr>
                <td>{{ student.id }}</td>
                <td>{{ student.name }}</td>
                <td>{{ student.department }}</td>
                <td>{{ student.year }}</td>
                <td>
                    <a class="delete"
                       href="/delete/{{ student.id }}"
                       onclick="return confirm('Delete this student?')">
                       Delete
                    </a>
                </td>
            </tr>
            {% endfor %}
        </table>
    </div>

</div>

<div class="footer">
    Campus Management System | CI/CD Demo
</div>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML, students=students)


@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    department = request.form["department"]
    year = request.form["year"]

    new_id = max([s["id"] for s in students], default=0) + 1

    students.append({
        "id": new_id,
        "name": name,
        "department": department,
        "year": year
    })

    return redirect("/")


@app.route("/delete/<int:student_id>")
def delete_student(student_id):
    global students

    students = [
        student for student in students
        if student["id"] != student_id
    ]

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
