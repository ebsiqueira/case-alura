import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def connect_to_db():
    try:
        connection = mysql.connector.connect(user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PW'), db=os.getenv('MYSQL_DB'), host=os.getenv('MYSQL_HOST'))
        return connection
    except Exception as e:
        raise e 
    
def select_sentiment(sentiment):
    try:
        connection = connect_to_db()
        
        cursor = connection.cursor()
        cursor.execute("SELECT sentiment_id FROM sentiment WHERE sentiment=%s;", (sentiment,))
        sentiment_id = cursor.fetchone()[0]
        
        connection.commit()
        
        cursor.close()
        connection.close()
    
        return sentiment_id
    
    except Exception as e:
        raise e

def insert_code(code):
    try:
        code_id = None
        
        connection = connect_to_db()
        
        cursor = connection.cursor()
        cursor.execute("SELECT code_id FROM code WHERE code = %s;", (code,))
        if(cursor.fetchone()):
            code_id = cursor.fetchone()[0]
        cursor.close()
        
        if(not code_id):
            cursor = connection.cursor()
            cursor.execute("INSERT INTO code (code) VALUES (%s);", (code,))
            cursor.close()
            
            cursor = connection.cursor()
            cursor.execute("SELECT LAST_INSERT_ID();")
            code_id = cursor.fetchone()[0]
            cursor.close()

        connection.commit()
        connection.close()
        
        return code_id
    
    except Exception as e:
        raise e

def insert_feedback(feedback, code_id, sentiment_id, reason):
    try:
        connection = connect_to_db()
        
        cursor = connection.cursor()
        cursor.execute("INSERT INTO feedbacks (feedback, sentiment_id, code_id, reason) VALUES (%s, %s, %s, %s);", (feedback, int(sentiment_id), int(code_id), reason))
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT LAST_INSERT_ID();")
        feedback_id = cursor.fetchone()[0]
        cursor.close()
        
        connection.commit()
        
        cursor.close()
        connection.close()
    
        return feedback_id
    
    except Exception as e:
        raise e
    
def select_feedbacks():
    
    connection = connect_to_db()
     
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM feedbacks")
    feedbacks = cursor.fetchall()
    cursor.close()
    
    connection.commit()
    
    cursor.close()
    connection.close()

    return feedbacks