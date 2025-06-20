import os
from dotenv import load_dotenv

from flask import Flask, redirect, render_template, request, url_for, flash, session
from wtforms.validators import DataRequired
from api_setup.chat_api import main_func
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

load_dotenv()

# Form Classes:
class ChatAI_Form(FlaskForm):
    prompt = StringField("ChatPrompt", validators=[DataRequired()])
    submit_chatAI = SubmitField('chatAI')

class ImageAI_Form(FlaskForm):
    prompt = StringField("ImagePrompt", validators=[DataRequired()])
    submit_imageAI = SubmitField('imageAI')

# Factory Function
def create_app(test_config=None):
    app = Flask(__name__, template_folder='templates', static_folder='../static', instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY = os.environ['SECRET_KEY'],
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Page Routes
    @app.route('/')
    def main():
        return redirect(url_for('home'))

    @app.route('/pop')
    def pop():
        session.pop('prompt_list', None)
        return redirect(url_for('home'))

    @app.route('/home', methods=['GET', 'POST'])
    def home():
        chatAI_form = ChatAI_Form()
        if 'prompt_list' not in session:
            session['prompt_list'] = ['No Data Yet']

        script_prompt = "Hello World!"
        chat_reply = "No AI response yet. Type a prompt to get started!"

        if request.method == 'POST':
            if chatAI_form.validate_on_submit():
                script_prompt = chatAI_form.prompt.data
                flash(f'Sent prompt: "{script_prompt}" to the AI.', 'success')
                (chat_reply, promptList) = main_func(script_prompt)
                session['prompt_list'] = promptList
                #return redirect(url_for('home'))
            else:
                flash('Chat Prompt validation failed. Please enter something.', 'danger')
                chat_reply = "Please fix the errors in your prompt."
        else:
            chat_reply = script_prompt

        return render_template("home.html", chatAI_form=chatAI_form, chat_reply=chat_reply, prompt_list=session.get('prompt_list'))

    return app
