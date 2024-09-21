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
        self.assertIn("[(6, 7), (7, 4), (8, 9), (9, 9), (10, 8), (11, 4), (12, 9)]", result)

    def test_teachers_by_subject(self):
        question = "How many teachers are there for each subject?"
        result = query_database(question)
        self.assertIn("Result:", result)
        self.assertIn("[('Art', 4), ('English', 2), ('History', 2), ('Mathematics', 1), ('Science', 1)]", result)

    def test_students_with_highest_grades(self):
        question = "List the top 5 students with the highest average grades across all subjects"
        result = query_database(question)
        self.assertIn("Result:", result)
        self.assertIn("[(7, 'Anthony', 'Evans', Decimal('98.090000')), (1, 'David', 'Greene', Decimal('94.503333')), (6, 'Ronald', 'Moran', Decimal('89.132500')), (21, 'Ashley', 'Jackson', Decimal('88.912500')), (4, 'Derek', 'Fowler', Decimal('87.580000'))]", result)

    def test_student_with_highest_score(self):
        question = "Give the name of the student with the top score out of all classes."
        result = query_database(question)
        self.assertIn("Result:", result)
        self.assertIn("[('James', 'Lewis', Decimal('99.92'))]", result)


if __name__ == '__main__':
    unittest.main()
