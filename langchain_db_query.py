import os
import yaml
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_anthropic import ChatAnthropic
from sqlalchemy import create_engine
from tabulate import tabulate

# Load environment variables
load_dotenv()

# Function to format the result as a table
def format_result(result):
    if isinstance(result, list) and len(result) > 0:
        if isinstance(result[0], tuple):
            headers = [f"Column {i+1}" for i in range(len(result[0]))]
            return tabulate(result, headers=headers, tablefmt="grid")
        elif isinstance(result[0], dict):
            return tabulate(result, headers="keys", tablefmt="grid")
    return str(result)

# Load database configuration
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Database connection details
DB_USER = config['mysql']['user']
DB_PASSWORD = os.getenv('MYSQL_PASSWORD')
DB_HOST = config['mysql']['host']
DB_NAME = config['mysql']['database']

# Create SQLAlchemy engine
db_url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
engine = create_engine(db_url)

# Create SQLDatabase object
db = SQLDatabase(engine)

# Initialize Claude AI model
llm = ChatAnthropic(model='claude-3-5-sonnet-20240620')

# Create SQLDatabaseChain
db_chain = create_sql_query_chain(llm, db)

def query_database(question: str) -> str:
    """
    Execute a natural language query on the database using LangChain and Claude AI.
    
    :param question: A natural language question about the database
    :return: The answer to the question based on the database content
    """
    try:
        response = db_chain.invoke({"question": question})
        sql_query = extract_sql_query(response)
        if sql_query:
            try:
                result = db.run(sql_query)
                formatted_result = format_result(result)
                return f"SQL Query: {sql_query}\n\nResult:\n{formatted_result}"
            except Exception as sql_error:
                # If there's an error, ask the LLM to fix it
                fix_prompt = f"The following SQL query resulted in an error: {sql_query}\n\nError: {str(sql_error)}\n\nPlease provide a corrected version of this SQL query that will work with MySQL."
                fixed_response = llm.invoke(fix_prompt)
                fixed_sql_query = extract_sql_query(fixed_response)
                if fixed_sql_query:
                    try:
                        result = db.run(fixed_sql_query)
                        formatted_result = format_result(result)
                        return f"Original SQL Query (with error): {sql_query}\n\nCorrected SQL Query: {fixed_sql_query}\n\nResult:\n{formatted_result}"
                    except Exception as new_error:
                        return f"Unable to execute the corrected SQL query. Error: {str(new_error)}"
                else:
                    return f"Unable to correct the SQL query. Original error: {str(sql_error)}"
        else:
            return "Unable to generate a valid SQL query."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def extract_sql_query(response: str) -> str:
    """
    Extract the SQL query from the LLM's response.
    
    :param response: The full response from the LLM
    :return: The extracted SQL query, or None if not found
    """
    import re
    if not isinstance(response, str):
        return None
    
    # Look for SQL keywords to identify the start of the query
    sql_keywords = r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP)\b'
    match = re.search(sql_keywords, response, re.IGNORECASE)
    
    if match:
        # Extract from the first SQL keyword to the end of the string
        query = response[match.start():].strip()
        
        # Remove any text after the last semicolon (if present)
        last_semicolon = query.rfind(';')
        if last_semicolon != -1:
            query = query[:last_semicolon + 1]
        
        # Ensure the query ends with a semicolon
        if not query.endswith(';'):
            query += ';'
        
        return query.strip()
    
    return None

def main():
    question = "Which student has the top grade in each year group?"
    answer = query_database(question)
    print(f"Question: {question}")
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
