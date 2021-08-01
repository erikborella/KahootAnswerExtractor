from flask import Flask, render_template, request
from flask.helpers import url_for
import requests
import os

template_dir = os.path.abspath("views/")

app = Flask(__name__, template_folder=template_dir)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/answers", methods=["POST"])
def answers():
    kahootId = request.form['kahootId']

    answers = getAnswers(kahootId)

    if answers == None:
        return render_template(url_for("index"))

    return render_template("answers.html", answers=answers)

def getAnswers(kahootId):
    r = requests.get(f"https://kahoot.it/rest/challenges/{kahootId}/progress/")

    if not r.ok:
        return None

    questions = []

    for bruteQuestion in r.json()['questions']:
        question = {
            'index': bruteQuestion['index'],
            'title': bruteQuestion['title'],
            'answer': getCorrectAnswer(bruteQuestion['choices'])
        }

        questions.append(question)

    return questions

def getCorrectAnswer(questionChoices):
    for choice in questionChoices:
        if (choice['correct'] == True):
            return choice['answer']

if __name__ == "__main__":
    app.run()