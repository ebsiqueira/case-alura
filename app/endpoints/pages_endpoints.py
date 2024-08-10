from flask import request, render_template, Blueprint
from app.utils.database_utils import *
import requests

pages = Blueprint('pages', __name__, template_folder='../templates')

@pages.route('/home')
def home():
    return render_template('home.html')

@pages.route('/send_feedback', methods=['GET', 'POST'])
def send_feedback():
    
    if request.method == 'POST':
        text = request.form.get('textarea')
        
        rq = requests.post("http://127.0.0.1:5000/feedback", json = {"feedback": text})
        
    return render_template('send_feedback.html')

@pages.route('/display_feedbacks')
def display_feedbacks():
    
    feedbacks = select_feedbacks()

    return render_template('display_feedbacks.html', data=feedbacks)

@pages.route('/display_statistics')
def display_statistics():
    
    statistics = select_sentiments()

    return render_template('display_statistics.html', json_data=statistics)