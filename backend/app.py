import os
from flask import Flask
from flask_cors import CORS


app=Flask(__name__)
CORS(app,origins= ["https://db-chatbot.vercel.app"])

@app.before_request
def before_request():
    if request.method == 'OPTIONS':  # Handle preflight requests
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Origin'] = '*'  # Allow all origins or specify your frontend URL
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'  # Allowed methods
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'  # Allowed headers
        return response

#Default Route
@app.route("/",methods=["GET"])
def welcome():
    return "API Running Successfully",200


try:
    from controllers.users_controller import *
    from controllers.query_controller import *
except Exception as e:
    print(e)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True,host="0.0.0.0", port=port)