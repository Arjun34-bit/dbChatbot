from flask import request,jsonify
from configs.config import get_connection

from configs.helpers import generate_token

from werkzeug.security import generate_password_hash, check_password_hash



class user_model():
    def __init__(self):
        self.conn=get_connection()

    def register(self):
        data=request.json
        username=data.get("username")
        email=data.get("email")
        password=data.get("password")

        if not username or not password or not email:
            return jsonify({"message":"All fields are required"}),400
        
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        
        try:
            cursor=self.conn.cursor()
            allReadyExists=cursor.execute("SELECT * FROM users WHERE email=%s",(email,))
            allReadyExists=cursor.fetchone()

            if allReadyExists:
                return jsonify({"message":"User already exists"}),400
            
            cursor.execute("INSERT INTO users (username,email,password) VALUES (%s,%s,%s)",(username,email,hashed_password))
            self.conn.commit()
            return jsonify({'message': 'User registered successfully.'}), 201
        except Exception as e:
            return jsonify({'message': 'Error occurred: ' + str(e)}), 500
        
        
        
    def login(self):
        data=request.json
        email=data.get("email")
        password=data.get("password")

        if not email or not password:
            return jsonify({"message":"All fields are required"}),400

        try:
            cursor=self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email=%s",(email,))
            isUser=cursor.fetchone()

            if not isUser:
                return jsonify({"message":"User not registered"}),404
                        
            stored_password = isUser["password"]  
            if not check_password_hash(stored_password, password):
                return jsonify({"message": "Invalid email or password"}), 401

            token = generate_token(isUser["id"])
            return jsonify({"token": token}), 200
        except Exception as e:
            return jsonify({'message': 'Error occurred: ' + str(e)}), 500
        



