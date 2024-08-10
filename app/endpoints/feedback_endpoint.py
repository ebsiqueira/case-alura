from flask import request, jsonify, Blueprint
from app.utils.feedback_utils import analyze_feedback, analyze_spam
from app.utils.database_utils import *
import json

feedback = Blueprint('feedback', __name__)

@feedback.route('/feedback', methods=['POST'])
def receive_feedback():
        try:
                data = request.get_json()
                
                feedback_data = data.get('feedback')
                
                if(analyze_spam(feedback_data) == 'Sim'):
                        return jsonify({"processed": False, "message": "SPAM detectado"})

                feedback_processed = analyze_feedback(feedback_data)
                response = json.loads(feedback_processed)
                
                code_id = insert_code(response['requested_features'][0]['code'])
                sentiment_id = select_sentiment(response['sentiment'])
                feedback_id = insert_feedback(feedback_data, code_id, sentiment_id, response['requested_features'][0]['reason'])
                
                response["id"] = feedback_id
                
                return response
        except Exception as e:
                return {"error": "Ocorreu um erro durante a análise do feedback"}