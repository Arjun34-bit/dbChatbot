from flask import Flask
from flask_cors import CORS


app=Flask(__name__)
CORS(app)

#Default Route
@app.route("/",methods=["GET"])
def welcome():
    return "API Running Successfully"


try:
    from controllers.users_controller import *
    from controllers.query_controller import *
except Exception as e:
    print(e)

if __name__ == '__main__':
    app.run(debug=True)