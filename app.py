import os
from dotenv import load_dotenv

from flask import Flask, redirect, render_template, request, url_for
from api_setup.chat_api import main_func

app = Flask(__name__, template_folder='templates', static_folder='static')

load_dotenv()
app.secret_key = os.environ['SECRET_KEY']

@app.route('/')
def main():
    return redirect(url_for('home'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    prompt = "Say Hello World!"
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        if prompt: # Only call main_func if a prompt was submitted
            response = main_func(prompt)

    response = main_func(prompt)
    return render_template("home.html", chat_reply=response)


if __name__ == '__main__':
    app.run(debug=True)
