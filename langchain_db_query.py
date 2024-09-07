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
        # Extract and modify the SQL query from the response
        sql_query = extract_sql_query(response)
        if sql_query:
            try:
                result = db.run(sql_query)
                formatted_result = format_result(result)
                return f"SQL Query: {sql_query}\n\nResult:\n{formatted_result}"
            except Exception as sql_error:
                # If there's still an error, we'll ask the LLM to fix it
                fix_prompt = f"The following SQL query resulted in an error: {sql_query}\n\nError: {str(sql_error)}\n\nPlease provide a corrected version of this SQL query that will work with MySQL in ONLY_FULL_GROUP_BY mode."
                fixed_response = llm.invoke(fix_prompt)
                fixed_sql_query = extract_sql_query(fixed_response)
                if fixed_sql_query:
                    result = db.run(fixed_sql_query)
                    formatted_result = format_result(result)
                    return f"Original SQL Query (with error): {sql_query}\n\nCorrected SQL Query: {fixed_sql_query}\n\nResult:\n{formatted_result}"
                else:
                    return f"Unable to correct the SQL query. Original error: {str(sql_error)}"
        else:
            return "Unable to generate a valid SQL query."
    except Exception as e:
        return f"An error occurred: {str(e)}"

def extract_sql_query(response: str) -> str:
    """
    Extract and modify the SQL query from the LLM's response to comply with ONLY_FULL_GROUP_BY mode.
    
    :param response: The full response from the LLM
    :return: The extracted and modified SQL query, or None if not found
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
        
        # Remove any backticks from column names
        query = re.sub(r'`([^`]+)`', r'\1', query)
        
        # Modify the query to comply with ONLY_FULL_GROUP_BY mode
        if 'GROUP BY' in query:
            # Add all non-aggregated columns from SELECT to GROUP BY
            select_columns = re.search(r'SELECT(.*?)FROM', query, re.IGNORECASE | re.DOTALL)
            if select_columns:
                columns = [col.strip() for col in select_columns.group(1).split(',')]
                non_aggregated = [col.split()[-1] for col in columns if not re.search(r'(SUM|COUNT|AVG|MAX|MIN)\(', col, re.IGNORECASE)]
                
                group_by_clause = re.search(r'GROUP BY(.*?)($|\s*ORDER BY|\s*LIMIT)', query, re.IGNORECASE | re.DOTALL)
                if group_by_clause:
                    new_group_by = ', '.join(set(non_aggregated))
                    query = re.sub(r'GROUP BY.*?($|\s*ORDER BY|\s*LIMIT)', f"GROUP BY {new_group_by}", query, flags=re.IGNORECASE | re.DOTALL)
        
        # Ensure there's an ORDER BY clause for the MAX aggregate
        if 'MAX(' in query and 'ORDER BY' not in query:
            query = query.rstrip(';') + f" ORDER BY MAX(grade_value) DESC;"
        
        # Remove any duplicate clauses (like multiple ORDER BY)
        query = re.sub(r'(ORDER BY.*?);?\s*(ORDER BY)', r'\1;', query, flags=re.IGNORECASE)
        
        # Ensure the query ends with a semicolon
        query = query.rstrip(';') + ';'
        
        return query
    return None

def main():
    question = "Which student has the top grade in each year group?"
    answer = query_database(question)
    print(f"Question: {question}")
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
