from flask import Flask, request, redirect, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    key = db.Column(db.Integer, primary_key=True)
    tasks = db.Column(db.String(100), nullable=True)
    done = db.Column(db.Boolean, default=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        task = request.form["task"]
        db.session.add(ToDo(tasks=task))
        db.session.commit()
        return redirect("/")
    tasks = ToDo.query.order_by(ToDo.time).all()
    return render_template("index.html", tasks=tasks)

@app.route('/remove/<int:key>')
def remove(key):
    row = ToDo.query.get_or_404(key)
    db.session.delete(row)
    db.session.commit()
    return redirect("/")

@app.route("/edit/<int:key>", methods=['GET', 'POST'])
def edit(key):
    row = ToDo.query.get_or_404(key)
    if request.method == "POST":
        row.tasks = request.form["task"]
        db.session.commit()
        return redirect("/")
    return render_template("edit.html", row=row)

@app.route("/complete/<int:key>")
def done(key):
    row = ToDo.query.get_or_404(key)
    row.done = not row.done
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
