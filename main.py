from flask import Flask, render_template, url_for


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/Lesson')
def Lesson():
    return render_template("Lesson.html")

@app.route('/Lesson_1')
def Lesson_1():
    return render_template("Lesson_1.html")

@app.route('/Lesson_2')
def Lesson_2():
    return render_template("Lesson_2.html")

@app.route('/Lesson_3')
def Lesson_3():
    return render_template("Lesson_3.html")

@app.route('/users')
def user():
    content = sqlite3.connect('db_students.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM Students')
    botinfo = cursor.fetchall()
    print(botinfo)
    return render_template("users.html", botinfo=botinfo)

if __name__ == '__main__':
    app.run(debug=True)