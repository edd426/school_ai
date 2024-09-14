import unittest
from langchain_db_query import query_database

class TestLangChainDBQuery(unittest.TestCase):
    def test_total_students(self):
        question = "How many students are in the school?"
        result = query_database(question)
        self.assertIn("SELECT COUNT(*) FROM students", result)
        self.assertIn("Result:", result)

    def test_students_in_year_11(self):
        question = "How many students are in year 11?"
        result = query_database(question)
        self.assertIn("SELECT COUNT(*) FROM students WHERE year = 11", result)
        self.assertIn("Result:", result)

    def test_average_age_of_teachers(self):
        question = "What is the average age of teachers?"
        result = query_database(question)
        self.assertIn("SELECT AVG(age) FROM teachers", result)
        self.assertIn("Result:", result)

    def test_students_per_year(self):
        question = "How many students are there in each year?"
        result = query_database(question)
        self.assertIn("SELECT year, COUNT(*) FROM students GROUP BY year", result)
        self.assertIn("Result:", result)

    def test_teachers_by_subject(self):
        question = "List the number of teachers for each subject"
        result = query_database(question)
        self.assertIn("SELECT subject, COUNT(*) FROM teachers GROUP BY subject", result)
        self.assertIn("Result:", result)

    def test_youngest_teacher(self):
        question = "Who is the youngest teacher and what subject do they teach?"
        result = query_database(question)
        self.assertIn("SELECT name, subject, MIN(age) FROM teachers", result)
        self.assertIn("Result:", result)

    def test_students_with_highest_grades(self):
        question = "List the top 5 students with the highest average grades across all subjects"
        result = query_database(question)
        self.assertIn("SELECT students.name, AVG(grades.grade) as avg_grade", result)
        self.assertIn("FROM students", result)
        self.assertIn("JOIN grades ON students.id = grades.student_id", result)
        self.assertIn("GROUP BY students.id", result)
        self.assertIn("ORDER BY avg_grade DESC", result)
        self.assertIn("LIMIT 5", result)
        self.assertIn("Result:", result)

if __name__ == '__main__':
    unittest.main()
