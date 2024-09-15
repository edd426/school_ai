import unittest
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_db_query import query_database

class TestLangChainDBQuery(unittest.TestCase):
    def test_total_students(self):
        question = "How many students are in the school?"
        result = query_database(question)
        self.assertIn("Result:", result)
        self.assertIn("[(50,)]", result)

    def test_students_in_year_11(self):
        question = "How many students are in year 11?"
        result = query_database(question)
        self.assertIn("Result:", result)
        self.assertIn("[(4,)]", result)

    def test_students_per_year(self):
        question = "How many students are there in each year?"
        result = query_database(question)
        self.assertIn("Result:", result)
        self.assertRegex(result, r"\(\d+,\s*\d+\)")

    def test_teachers_by_subject(self):
        question = "List the number of teachers for each subject"
        result = query_database(question)
        self.assertIn("Result:", result)
        self.assertRegex(result, r"\('\w+',\s*\d+\)")

    def test_students_with_highest_grades(self):
        question = "List the top 5 students with the highest average grades across all subjects"
        result = query_database(question)
        self.assertIn("Result:", result)
        self.assertRegex(result, r"\(\d+,\s*'\w+',\s*'\w+',\s*Decimal\('\d+\.\d+'\)\)")

if __name__ == '__main__':
    unittest.main()
