from app import app
from flask import request,jsonify
from models.response_model import run_workflow

from configs.helpers import decode_token

from configs.config import get_connection


@app.route("/api/query",methods=["POST"])
def get_query():
    data = request.json
    user_query = data.get("user_query", "")
    token=data.get("token","")

    user_id=decode_token(token)
    print("user_id",user_id)

    if not user_query:
        return jsonify({"error": "user_query is required"}), 400
    try:
        response = run_workflow(user_query)

        conn = db.get_connection()  # Adjust if using a different method for database connection
        cursor = conn.cursor()
        
        # Save the chat history into the database
        insert_history_query = "INSERT INTO chathistory (user_id, query,response) VALUES (%s, %s, %s)"
        cursor.execute(insert_history_query, (user_id.get("user_id"), user_query, response))
        
        # Commit the transaction
        conn.commit()

        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/api/chat-history", methods=["GET"])
def get_chat_history():
    try:
        # Establish database connection
        conn = get_connection()
        cursor = conn.cursor()

        # Query to fetch all chat history records
        fetch_history_query = "SELECT * FROM chathistory"
        cursor.execute(fetch_history_query)
        chat_history = cursor.fetchall()



        # Prepare the response data
        history_data = []
        for record in chat_history:
            history_data.append({
                "user_id": record[1],  
                "query": record[2],
                "response": record[3],
                "createdAt": record[4]
            })

        return jsonify({"chat_history": history_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500