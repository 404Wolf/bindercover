from flask import Flask, render_template, request, url_for, flash, redirect
from utils import BinderCover
app = Flask(__name__)


@app.route('/', methods=("GET", "POST"))
def index():
    if request.method == "POST":
        bindercover = BinderCover(
            name=request.form["name"],
            course=request.form["course"],
            semester=request.form["semester"],
            email=request.form["email"],
            phone=request.form["phone"],
        )
        print(bindercover)
        exit()
    elif request.method == "GET":
        return render_template("index.html")

if __name__ == '__main__':
    app.run()
