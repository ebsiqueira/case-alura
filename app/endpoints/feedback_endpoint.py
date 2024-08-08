from flask import Flask, request, jsonify
from app.services.feedback_services import analyze_feedback, analyze_spam
import json

feedback = Flask(__name__)

@feedback.route('/feedback', methods=['POST'])
def receive_feedback():
        try:
                data = request.get_json()
                
                feedback_data = data.get('feedback')
                
                if(analyze_spam(feedback_data) == 'Sim'):
                        return jsonify({
                                "processed": False, "message": "SPAM detectado"
                        })

                feedback_processed = analyze_feedback(feedback_data)
                print(feedback_processed)
                response = json.loads(feedback_processed)
                
                response["id"] = "123"
                
                return response
        except Exception as e:
                return {"error": "Ocorreu um erro durante a análise do feedback"}

if __name__ == '__main__':
    feedback.run(debug=True)