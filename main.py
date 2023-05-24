from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sp.db"
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    importance = db.Column(db.Text(25), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)


@app.route("/")
def head():
    return redirect("/notes")


@app.route("/notes", methods=["POST", "GET"])
def notes():
    if request.method == "POST":
        importance = request.form["importance"]
        text = request.form["text"]
        if len(text.strip()) == 0 or len(importance.strip()) == 0:
            return "Error"
        note = Note(importance=importance, text=text)
        try:
            db.session.add(note)
            db.session.commit()
            return redirect("/list")
        except:
            return "Error"
    else:
        return render_template("notes.html")


@app.route("/list")
def list():
    lists = Note.query.order_by(Note.date.desc()).all()
    return render_template("list.html", list=lists)


if __name__ == "__main__":
    app.run(debug=True)
