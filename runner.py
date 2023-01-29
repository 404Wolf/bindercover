import os
from random import randint
from threading import Thread
from time import sleep

from flask import Flask, render_template, request, send_file

from utils import BinderCover

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/generate")
def generate():
    # Create a BinderCover object from the user input
    bindercover = BinderCover(
        name=request.form["name"],
        course=request.form["course"],
        semester=request.form["semester"],
        year=request.form["year"],
        email=request.form["email"],
        phone=request.form["phone"],
    )
    # Generate a PDF file from the bindercover template
    bindercover.generate_pdf(filename := f"{randint(1000000, 9999999)}")

    # Schedule the PDF for deletion after 10 seconds
    def delete_file():
        sleep(6)
        os.remove(f"generated/{filename}.pdf")

    Thread(target=delete_file).start()

    # Redirect the user to the generated PDF file
    return send_file(f"generated/{filename}.pdf", mimetype="application/pdf")


if __name__ == "__main__":
    app.run()
