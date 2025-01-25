import os
import openai
from typing_extensions import TypedDict
from langchain.chains import LLMChain
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph, START, END
from configs.config import Database
# from typing import Annotated 
# from langgraph.graph.message import add_message


db = Database()

class State(TypedDict):
    current_user: str


class AgentState(TypedDict):
    user_query:str
    sql_query:str
    execute_sql_query:str
    formatted_response:str
# Define Node Functions

def generate_sql(state:AgentState):
    try:
        user_query = state["user_query"]
        print(f"Received user query: {user_query}")
        # Retrieve the API key securely
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is not set in environment variables.")

        # Set up LangChain with OpenAI for SQL query generation
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Use the desired model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that converts natural language queries into SQL. And return only sql statement skip the explanations"},
                {"role": "user", "content": state["user_query"]},
            ]
        )
        
        # Extract the reply from the response
        bot_reply = response["choices"][0]["message"]["content"]
        start_marker = "```sql\n"
        end_marker = "\n```"

        # Find the SQL query between the markers
        start_index = bot_reply.find(start_marker) + len(start_marker)
        end_index = bot_reply.find(end_marker)

        sql_query = bot_reply[start_index:end_index].strip()

        print(f"Extracted SQL Query: {sql_query}")
        state["sql_query"]=sql_query
        return state
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

def execute_sql(state:AgentState):
    print(f"Getting SQL Query {state["sql_query"]}")

    try:
        query=state["sql_query"]
        print("Executing SQL Query")
        conn = db.get_connection()
        cursor = conn.cursor()

        # Execute the SQL query
        cursor.execute(query)
        result = cursor.fetchall()

        # Store the result in the state
        state["execute_sql_query"] = result
        return state
    except Exception as e: 
        print(f"Error: {str(e)}")
        raise

def human_readable(state:AgentState):
    print("Gnerating Human Readable format")

    try:
        print(f"Getting Output from SQL genrated data {state["execute_sql_query"]}")
        # Retrieve the API key securely
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is not set in environment variables.")

        # Set up LangChain with OpenAI for SQL query generation
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Use the desired model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that converts sql table data into natural human-readable format according to the question. And return only text, skip the explanations"},
                {"role": "user", "content": f"User Query: {state['user_query']}\nSQL Query Result: {state['execute_sql_query']}"},
            ]
        )
        
        # Extract the reply from the response
        bot_reply = response["choices"][0]["message"]["content"]
        state["formatted_response"]=bot_reply
        print(f"Human Readable Response {state['formatted_response']}")
        return state
    except Exception as e:
        print(f"Error: {str(e)}")
        raise


def run_workflow(user_query):
    workflow = StateGraph(AgentState)
    workflow.add_node("generate_sql", generate_sql)
    workflow.add_node("execute_sql", execute_sql)
    workflow.add_node("human_readable", human_readable)
    workflow.add_edge(START, "generate_sql")
    workflow.add_edge("generate_sql", "execute_sql")
    workflow.add_edge("execute_sql", "human_readable")
    workflow.add_edge("human_readable", END)
    


    # Run the workflow
    try:
        work = workflow.compile()
        if work:
            print("Compiled workflow successfully.")
        else:
            print("Failed to compile workflow.")
            return

        # Running the workflow with valid input
        input_state = {"user_query": user_query, "sql_query": ""} #Adjust as per your state schema

        # Debugging intermediate events
        for event in work.stream(input_state):
            print("Event:", event.values())

        final_state = list(event.values())[0]  # Convert dict_values to a list and extract the first dictionary
        return final_state['formatted_response'] 

    except Exception as e:
        print(f"Error running workflow: {str(e)}")