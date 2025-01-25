# from langgraph import StateGraph

# # Define states and transitions
# states = {
#     "start": {"next": "processing"},
#     "processing": {"next": "done", "error": "failed"},
#     "done": {},
#     "failed": {}
# }

# # Create a StateGraph instance
# graph = StateGraph(states=states, initial_state="start")

# # Access the current state
# print("Current State:", graph.current_state)

# # Transition to the next state
# graph.transition("next")
# print("After Transition State:", graph.current_state)

# # Handle error state
# graph.transition("error")
# print("Error State:", graph.current_state)

# # Resetting the state to initial
# graph.reset()
# print("Reset State:", graph.current_state)


# llm = OpenAI(api_key=api_key)

#         # LangChain prompt template for translating natural language to SQL
#         prompt_template = """
#         You are a helpful assistant that converts natural language queries into SQL.
#         Here is the user's query: {query}
#         Please provide the SQL query that answers this.
#         """
#         prompt = PromptTemplate(input_variables=["query"], template=prompt_template)
#         chain = LLMChain(llm=llm, prompt=prompt)

#         # Generate the SQL query
#         response = chain.run(query=user_query)
#         print(f"Generated SQL query: {response}")
#         return response