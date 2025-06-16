import os
from dotenv import load_dotenv

from flask import Flask, redirect, render_template, request, url_for, flash
from wtforms.validators import DataRequired
from api_setup.chat_api import main_func
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


app = Flask(__name__, template_folder='templates', static_folder='static')

load_dotenv()
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

# Form Classes:
class ChatAI_Form(FlaskForm):
    prompt = StringField("ChatPrompt", validators=[DataRequired()])
    submit_chatAI = SubmitField('chatAI')


# Page Routes
@app.route('/')
def main():
    return redirect(url_for('home'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    chatAI_form = ChatAI_Form()

    script_prompt = "Say Hello World!"
    chat_reply = "No AI response yet. Type a prompt to get started!"

    if request.method == 'POST':
        if chatAI_form.validate_on_submit():
            script_prompt = chatAI_form.prompt.data
            flash(f'Sent prompt: "{script_prompt}" to the AI.', 'success')
            chat_reply = main_func(script_prompt)
            #return redirect(url_for('home'))
        else:
            flash('Chat Prompt validation failed. Please enter something.', 'danger')
            chat_reply = "Please fix the errors in your prompt."
    else:
        chat_reply = main_func(script_prompt)

    return render_template("home.html", chatAI_form=chatAI_form, chat_reply=chat_reply)


if __name__ == '__main__':
    app.run(debug=True)
