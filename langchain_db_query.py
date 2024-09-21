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

def query_database(question: str, max_attempts: int = 3) -> str:
    """
    Execute a natural language query on the database using LangChain and Claude AI.
    
    :param question: A natural language question about the database
    :param max_attempts: Maximum number of attempts to correct the SQL query
    :return: The answer to the question based on the database content
    """
    try:
        # Modify the prompt to instruct LangChain not to use LIMIT clauses
        prompt = f"Generate an SQL query for the following question without using LIMIT clauses: {question}"
        response = db_chain.invoke({"question": prompt})
        sql_query = extract_sql_query(response)
        if not sql_query:
            return "Unable to generate a valid SQL query."

        for attempt in range(max_attempts):
            try:
                result = db.run(sql_query)
                formatted_result = format_result(result)
                return f"SQL Query (Attempt {attempt + 1}):\n{sql_query}\n\nResult:\n{formatted_result}"
            except Exception as sql_error:
                if attempt == max_attempts - 1:
                    return f"Unable to execute the SQL query after {max_attempts} attempts. Final error: {str(sql_error)}"
                
                # Ask the LLM to fix the query
                fix_prompt = f"""
                The following SQL query resulted in an error:
                {sql_query}

                Error: {str(sql_error)}

                Please provide a corrected version of this SQL query that will work with MySQL.
                Consider the following:
                1. Ensure all columns in the SELECT statement are either in the GROUP BY clause or used with an aggregate function.
                2. Check for proper table joins and aliasing.
                3. Verify the syntax is compatible with MySQL.
                4. Make sure all referenced columns and tables exist in the database.
                5. Do not use LIMIT clauses.

                Provide only the corrected SQL query without any explanations.
                """
                fixed_response = llm.invoke(fix_prompt)
                sql_query = extract_sql_query(fixed_response)
                if not sql_query:
                    return f"Unable to generate a valid SQL query after attempt {attempt + 1}."

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
    questions = [
        "How many students are in the school?",
        "How many students are in year 11?",
        "How many students are there in each year?",
        "How many teachers are there for each subject?",
        "List the top 5 students with the highest average grades across all subjects",
        "Give the name of the student with the top score out of all classes."
    ]
    
    for question in questions:
        answer = query_database(question)
        print(f"Question: {question}")
        print(f"Answer: {answer}")
        print("-" * 50)

if __name__ == "__main__":
    main()
