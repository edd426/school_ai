import mysql.connector
from mysql.connector import Error

def create_server_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Swordfish'  # Replace with your MySQL root password
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Server: {e}")
        return None

def create_database(connection, database_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"Database '{database_name}' created successfully")
    except Error as e:
        print(f"Error creating database: {e}")

def create_db_connection(database_name):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_password_here',  # Replace with your MySQL root password
            database=database_name
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"Error executing query: {e}")

def create_tables(connection):
    create_students_table = """
    CREATE TABLE IF NOT EXISTS students (
        student_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        date_of_birth DATE NOT NULL,
        grade_level INT NOT NULL
    );
    """

    create_teachers_table = """
    CREATE TABLE IF NOT EXISTS teachers (
        teacher_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        subject VARCHAR(50) NOT NULL
    );
    """

    create_courses_table = """
    CREATE TABLE IF NOT EXISTS courses (
        course_id INT AUTO_INCREMENT PRIMARY KEY,
        course_name VARCHAR(100) NOT NULL,
        teacher_id INT,
        FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
    );
    """

    create_enrollments_table = """
    CREATE TABLE IF NOT EXISTS enrollments (
        enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT,
        course_id INT,
        FOREIGN KEY (student_id) REFERENCES students(student_id),
        FOREIGN KEY (course_id) REFERENCES courses(course_id)
    );
    """

    create_grades_table = """
    CREATE TABLE IF NOT EXISTS grades (
        grade_id INT AUTO_INCREMENT PRIMARY KEY,
        enrollment_id INT,
        grade_value DECIMAL(5,2) NOT NULL,
        FOREIGN KEY (enrollment_id) REFERENCES enrollments(enrollment_id)
    );
    """

    execute_query(connection, create_students_table)
    execute_query(connection, create_teachers_table)
    execute_query(connection, create_courses_table)
    execute_query(connection, create_enrollments_table)
    execute_query(connection, create_grades_table)

def insert_sample_data(connection):
    insert_students = """
    INSERT INTO students (first_name, last_name, date_of_birth, grade_level)
    VALUES 
    ('John', 'Doe', '2005-05-15', 10),
    ('Jane', 'Smith', '2006-02-20', 9),
    ('Mike', 'Johnson', '2004-11-30', 11);
    """

    insert_teachers = """
    INSERT INTO teachers (first_name, last_name, subject)
    VALUES 
    ('Alice', 'Brown', 'Mathematics'),
    ('Bob', 'Wilson', 'Science'),
    ('Carol', 'Taylor', 'English');
    """

    insert_courses = """
    INSERT INTO courses (course_name, teacher_id)
    VALUES 
    ('Algebra', 1),
    ('Biology', 2),
    ('Literature', 3);
    """

    insert_enrollments = """
    INSERT INTO enrollments (student_id, course_id)
    VALUES 
    (1, 1), (1, 2), (1, 3),
    (2, 1), (2, 2),
    (3, 2), (3, 3);
    """

    insert_grades = """
    INSERT INTO grades (enrollment_id, grade_value)
    VALUES 
    (1, 85.5), (2, 92.0), (3, 78.5),
    (4, 88.0), (5, 90.5),
    (6, 95.0), (7, 89.5);
    """

    execute_query(connection, insert_students)
    execute_query(connection, insert_teachers)
    execute_query(connection, insert_courses)
    execute_query(connection, insert_enrollments)
    execute_query(connection, insert_grades)

def main():
    # Connect to the MySQL server
    server_connection = create_server_connection()
    if server_connection is not None:
        # Create the database
        create_database(server_connection, "school_database")
        server_connection.close()

        # Connect to the newly created database
        db_connection = create_db_connection("school_database")
        if db_connection is not None:
            create_tables(db_connection)
            insert_sample_data(db_connection)
            db_connection.close()
        else:
            print("Failed to connect to the database.")
    else:
        print("Failed to connect to the MySQL server.")

if __name__ == "__main__":
    main()