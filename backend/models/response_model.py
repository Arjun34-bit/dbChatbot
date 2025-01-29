import os
import openai
from openai import OpenAI
from typing_extensions import TypedDict
from langchain.chains import LLMChain
# from langchain_community.llms import OpenAI
# from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langgraph.graph import StateGraph, START, END
from configs.config import get_connection



class AgentState(TypedDict):
    database_schema:str
    user_query:str
    sql_query:str
    execute_sql_query:str
    formatted_response:str
# Define Node Functions

def get_schema(state: AgentState):
    try:
        print("Fetching database schema...")

        conn = get_connection()
        cursor = conn.cursor()  

        # Query to get all tables in the database
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        schema = {}

        for table in tables:
            table_name = table[0]
            # Query to get column information for each table
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            schema[table_name] = [
                {"Field": col[0], "Type": col[1], "Null": col[2], "Key": col[3], "Default": col[4], "Extra": col[5]}
                for col in columns
            ]

        # Store the schema in the state
        print(f"schema : {schema}")
        state["database_schema"] = schema
        print("Database schema fetched successfully.")
        return state
    except Exception as e:
        print(f"Error fetching database schema: {str(e)}")
        raise
    finally:
        cursor.close()
        conn.close()

def generate_sql(state:AgentState):
    try:
        user_query = state["user_query"]
        print(f"Received user query: {user_query}")
        # Retrieve the API key securely
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is not set in environment variables.")
        
        openai.api_key = api_key
        
        client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        message = [
            {"role": "system", "content": "You are a helpful assistant that converts natural language queries into SQL. The database schema is also provided. Return only the SQL statement, skip the explanations."},
            {"role": "user", "content": f"User Query: {state['user_query']}\nDATABASE SCHEMA: {state['database_schema']}"}
        ]

        response =  client.chat.completions.create(
            model='gpt-4o-mini', 
            messages=message
        )

        # response=openai.ChatCompletion.create(
        #     model='gpt-3.5-turbo',
        #     messages=[
        #         {"role": "user", "content": message}
        #     ]
        # )
        
        # Extract the reply from the response
        bot_reply = response.choices[0].message.content
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
    print(f"Getting SQL Query {state['sql_query']}")

    try:
        query=state["sql_query"]
        print("Executing SQL Query")
        conn = get_connection()
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
    finally:
        cursor.close()
        conn.close()

def human_readable(state:AgentState):
    print("Gnerating Human Readable format")

    try:
        print(f"Getting Output from SQL generated data {state['execute_sql_query']}")
        # Retrieve the API key securely
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is not set in environment variables.")
        
        client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # openai.api_key = api_key

        # Set up LangChain with OpenAI for SQL query generation
        messages = [
            {"role": "system", "content": "You are a helpful assistant that converts SQL table data into natural human-readable format according to the question. Return only text, skip the explanations."},
            {"role": "user", "content": f"User Query: {state['user_query']}\nSQL Query Result: {state['execute_sql_query']}"}
        ]


        response =  client.chat.completions.create(
            model='gpt-4o-mini', 
            messages=messages
        )
        
        # Extract the reply from the response
        bot_reply = response.choices[0].message.content
        state["formatted_response"]=bot_reply
        print(f"Human Readable Response {state['formatted_response']}")
        return state
    except Exception as e:
        print(f"Error: {str(e)}")
        raise


def run_workflow(user_query):
    workflow = StateGraph(AgentState)
    workflow.add_node("get_schema", get_schema)
    workflow.add_node("generate_sql", generate_sql)
    workflow.add_node("execute_sql", execute_sql)
    workflow.add_node("human_readable", human_readable)
    workflow.add_edge(START, "get_schema")
    workflow.add_edge("get_schema", "generate_sql")
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