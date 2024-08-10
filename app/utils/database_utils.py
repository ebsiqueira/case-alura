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
        # Pega o id equivalente do sentiment forcenido
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
        connection = connect_to_db()
        
        cursor = connection.cursor()
        # Pega o id do code fornecido
        cursor.execute("SELECT code_id FROM code WHERE code = %s;", (code,))
        response = cursor.fetchone()
        
        if(response != None):
            code_id = response[0]
        else:
            code_id = None
        cursor.close()
        
        if(code_id == None):
            cursor = connection.cursor()
            # Caso não exista código ainda no banco, cria um
            cursor.execute("INSERT INTO code (code) VALUES (%s);", (code,))
            cursor.close()
            
            cursor = connection.cursor()
            # Pega o código do último código inserido
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
        # Insere o feedback no banco
        cursor.execute("INSERT INTO feedbacks (feedback, sentiment_id, code_id, reason) VALUES (%s, %s, %s, %s);", (feedback, int(sentiment_id), int(code_id), reason))
        cursor.close()
        
        cursor = connection.cursor()
        # Pega o id do último feedback inserido
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
    try: 
        connection = connect_to_db()
        
        cursor = connection.cursor()
        # Seleciona todos os feedbacks, assim como o nome dos codigos e sentiments equivalentes aos ids armazenados
        cursor.execute("SELECT * FROM feedbacks LEFT JOIN sentiment ON feedbacks.sentiment_id = sentiment.sentiment_id LEFT JOIN code ON feedbacks.code_id = code.code_id;")
        feedbacks = cursor.fetchall()
        cursor.close()
        
        connection.commit()
        
        cursor.close()
        connection.close()

        return feedbacks
    
    except Exception as e:
        raise e

def select_sentiments():
    try:
        connection = connect_to_db()

        cursor = connection.cursor()
        # Retorna todos os sentiments e as quantidades de vezes que aparecem no banco
        cursor.execute("SELECT sentiment, COUNT(*) AS count FROM feedbacks LEFT JOIN sentiment ON feedbacks.sentiment_id = sentiment.sentiment_id GROUP BY sentiment")
        sentiments = cursor.fetchall()

        sentiment_dict = {}
        for sentiment in sentiments:
            sentiment_dict[str(sentiment[0])] = sentiment[1]

        cursor.close()
        connection.close()

        return sentiment_dict

    except Exception as e:
        raise e