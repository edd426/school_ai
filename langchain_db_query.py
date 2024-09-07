import os
import yaml
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
# from langchain_community.chains import SQLDatabaseChain
from langchain.chains import create_sql_query_chain
from langchain_anthropic import ChatAnthropic
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

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
        result = db_chain.run(question)
        return result
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    question = "How many students are in the database?"
    answer = query_database(question)
    print(f"Question: {question}")
    print(f"Answer: {answer}")

if __name__ == "__main__":
    main()
