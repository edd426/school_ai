import mysql.connector
from mysql.connector import Error
import os
import logging
from dotenv import load_dotenv
import yaml
from faker import Faker
import random
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

def create_server_connection():
    """Create a connection to the MySQL server."""
    try:
        connection = mysql.connector.connect(
            host=config['mysql']['host'],
            user=config['mysql']['user'],
            password=os.getenv('MYSQL_PASSWORD')
        )
        logging.info("Successfully connected to MySQL server")
        return connection
    except Error as e:
        logging.error(f"Error connecting to MySQL Server: {e}")
        return None

def create_database(connection, database_name):
    """Create a new database if it doesn't exist."""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        logging.info(f"Database '{database_name}' created successfully")
    except Error as e:
        logging.error(f"Error creating database: {e}")

def create_db_connection(database_name):
    """Create a connection to the specified database."""
    try:
        connection = mysql.connector.connect(
            host=config['mysql']['host'],
            user=config['mysql']['user'],
            password=os.getenv('MYSQL_PASSWORD'),
            database=database_name
        )
        logging.info(f"Successfully connected to database: {database_name}")
        return connection
    except Error as e:
        logging.error(f"Error connecting to MySQL Database: {e}")
        return None

def execute_query(connection, query):
    """Execute a given SQL query."""
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logging.info("Query executed successfully")
    except Error as e:
        logging.error(f"Error executing query: {e}")

def create_tables(connection):
    """Create the necessary tables in the database."""
    tables = [
        """
        CREATE TABLE IF NOT EXISTS students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            date_of_birth DATE NOT NULL,
            grade_level INT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            subject VARCHAR(50) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS courses (
            course_id INT AUTO_INCREMENT PRIMARY KEY,
            course_name VARCHAR(100) NOT NULL,
            teacher_id INT,
            FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            course_id INT,
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS grades (
            grade_id INT AUTO_INCREMENT PRIMARY KEY,
            enrollment_id INT,
            grade_value DECIMAL(5,2) NOT NULL,
            FOREIGN KEY (enrollment_id) REFERENCES enrollments(enrollment_id)
        )
        """
    ]

    for table in tables:
        execute_query(connection, table)

def generate_sample_data(num_students=50, num_teachers=10):
    """Generate sample data using Faker."""
    fake = Faker()
    
    students = []
    for _ in range(num_students):
        students.append({
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'date_of_birth': fake.date_of_birth(minimum_age=10, maximum_age=18),
            'grade_level': random.randint(6, 12)
        })
    
    teachers = []
    subjects = ['Mathematics', 'Science', 'English', 'History', 'Art', 'Music', 'Physical Education']
    for _ in range(num_teachers):
        teachers.append({
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'subject': random.choice(subjects)
        })
    
    courses = [
        {'name': 'Algebra', 'subject': 'Mathematics'},
        {'name': 'Biology', 'subject': 'Science'},
        {'name': 'Literature', 'subject': 'English'},
        {'name': 'World History', 'subject': 'History'},
        {'name': 'Chemistry', 'subject': 'Science'},
        {'name': 'Geometry', 'subject': 'Mathematics'},
        {'name': 'Physics', 'subject': 'Science'},
        {'name': 'Art History', 'subject': 'Art'},
        {'name': 'Music Theory', 'subject': 'Music'},
        {'name': 'Physical Education', 'subject': 'Physical Education'}
    ]
    
    return students, teachers, courses

def insert_sample_data(connection):
    """Insert generated sample data into the database."""
    students, teachers, courses = generate_sample_data()

    # Insert students
    for student in students:
        query = f"""
        INSERT INTO students (first_name, last_name, date_of_birth, grade_level)
        VALUES ('{student['first_name']}', '{student['last_name']}', '{student['date_of_birth']}', {student['grade_level']})
        """
        execute_query(connection, query)

    # Insert teachers
    for teacher in teachers:
        query = f"""
        INSERT INTO teachers (first_name, last_name, subject)
        VALUES ('{teacher['first_name']}', '{teacher['last_name']}', '{teacher['subject']}')
        """
        execute_query(connection, query)

    # Insert courses
    for course in courses:
        teacher = next((t for t in teachers if t['subject'] == course['subject']), None)
        if teacher:
            query = f"""
            INSERT INTO courses (course_name, teacher_id)
            VALUES ('{course['name']}', (SELECT teacher_id FROM teachers WHERE first_name = '{teacher['first_name']}' AND last_name = '{teacher['last_name']}'))
            """
            execute_query(connection, query)

    # Insert enrollments and grades
    for student in students:
        for _ in range(random.randint(3, 5)):  # Each student enrolls in 3-5 courses
            query = f"""
            INSERT INTO enrollments (student_id, course_id)
            VALUES (
                (SELECT student_id FROM students WHERE first_name = '{student['first_name']}' AND last_name = '{student['last_name']}'),
                (SELECT course_id FROM courses ORDER BY RAND() LIMIT 1)
            )
            """
            execute_query(connection, query)

            # Add a grade for each enrollment
            query = f"""
            INSERT INTO grades (enrollment_id, grade_value)
            VALUES (LAST_INSERT_ID(), {random.uniform(60, 100):.2f})
            """
            execute_query(connection, query)

def main():
    """Main function to initialize the database and insert sample data."""
    # This function orchestrates the entire database initialization process
    # Connect to the MySQL server
    server_connection = create_server_connection()
    if server_connection is not None:
        # Create the database
        create_database(server_connection, config['mysql']['database'])
        server_connection.close()

        # Connect to the newly created database
        db_connection = create_db_connection(config['mysql']['database'])
        if db_connection is not None:
            create_tables(db_connection)
            insert_sample_data(db_connection)
            db_connection.close()
            logging.info("Database initialization completed successfully")
        else:
            logging.error("Failed to connect to the database.")
    else:
        logging.error("Failed to connect to the MySQL server.")

if __name__ == "__main__":
    main()
