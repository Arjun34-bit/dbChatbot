from app import app
from flask import request,jsonify
from models.user_model import user_model


user=user_model()

@app.route("/api/register",methods=["POST"])
def add_user():
    return user.register()

@app.route("/api/login",methods=["POST"])
def login():
    return user.login()

# @app.route("/api/test",methods=["GET"])
# def api_test():
#     print("Testing")
#     return jsonify({"message":"Testing the api"})