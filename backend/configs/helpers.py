import os
import datetime
from dotenv import load_dotenv
import jwt

load_dotenv()

def generate_token(user_id):
    token=jwt.encode(
        {
        'user_id': user_id,  
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  
    },
    os.getenv("SECRET_KEY"),  # Secret key for signing the token
    algorithm='HS256'  # Algorithm used for token encoding
    )

    return token


def decode_token(token):
    try:
        # Get the secret key from the environment variables
        secret_key = os.getenv("SECRET_KEY")
        
        if not secret_key:
            raise ValueError("SECRET_KEY is not set in environment variables")

        # Decode the token using the secret key and the algorithm used for encoding (HS256)
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        
        # Return the decoded payload (which includes the user_id and expiration time)
        return payload

    except jwt.ExpiredSignatureError:
        # This exception is raised when the token has expired
        return {"error": "Token has expired"}
    
    except jwt.InvalidTokenError:
        # This exception is raised when the token is invalid
        return {"error": "Invalid token"}