from flask import Flask, request, redirect, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class ToDo(db.Model):
    key = db.Column(db.Integer, primary_key = True)
    tasks = db.Column(db.String(100), nullable = False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def page():
    if request.method == "POST":
        task = request.form["task"]
        row = ToDo(tasks = task)

        try:
            db.session.add(row)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue adding your task"
    else:
        tasks = ToDo.query.order_by(ToDo.time).all()
        return render_template("index.html", tasks=tasks)

@app.route('/remove/<int:key>')
def remove(key):
    row = ToDo.query.get_or_404(key)

    try:
        db.session.delete(row)
        db.session.commit()
        return redirect("/")
    except:
        return "There was an error while removing your task"

@app.route("/edit/<int:key>", methods=['GET', 'POST'])
def edit(key):
    row = ToDo.query.get_or_404(key)

    if request.method == "POST":
        row.tasks = request.form["task"]

        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an error while updating your task"
    else:
        return render_template("edit.html", row=row)

if __name__ == "__main__":
    app.run(debug=True)