CREATE DATABASE IF NOT EXISTS alumind;
USE alumind;

CREATE TABLE code (
    code_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(100) NOT NULL
);

CREATE TABLE sentiment (
    sentiment_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    sentiment VARCHAR(50) NOT NULL
);

CREATE TABLE feedbacks (
    feedback_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    feedback VARCHAR(1000) NOT NULL, 
    sentiment_id INT NOT NULL,
    code_id INT NOT NULL,
    reason VARCHAR(500) NOT NULL,
    FOREIGN KEY (sentiment_id) REFERENCES sentiment(sentiment_id),
    FOREIGN KEY (code_id) REFERENCES code(code_id)
);

INSERT INTO sentiment(sentiment) VALUES 
("POSITIVO"),
("NEGATIVO"),
("INCONCLUSIVO");