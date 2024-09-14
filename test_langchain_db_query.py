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
        self.assertIn("SELECT COUNT(`student_id`) AS `total_students` FROM `students`", result)
        self.assertIn("Result:", result)

    def test_students_in_year_11(self):
        question = "How many students are in year 11?"
        result = query_database(question)
        self.assertIn("SELECT COUNT(*) as `count` FROM `students` WHERE `grade_level` = 11", result)
        self.assertIn("Result:", result)

    def test_average_age_of_teachers(self):
        question = "What is the average age of teachers?"
        result = query_database(question)
        self.assertIn("SELECT AVG(`age`) as `average_age` FROM `teachers`", result)
        self.assertIn("Result:", result)

    def test_students_per_year(self):
        question = "How many students are there in each year?"
        result = query_database(question)
        self.assertIn("SELECT `grade_level`, COUNT(*) AS `student_count`", result)
        self.assertIn("FROM `students`", result)
        self.assertIn("GROUP BY `grade_level`", result)
        self.assertIn("ORDER BY `grade_level`", result)
        self.assertIn("Result:", result)

    def test_teachers_by_subject(self):
        question = "List the number of teachers for each subject"
        result = query_database(question)
        self.assertIn("SELECT `subject`, COUNT(*) AS `number_of_teachers`", result)
        self.assertIn("FROM `teachers`", result)
        self.assertIn("GROUP BY `subject`", result)
        self.assertIn("ORDER BY `number_of_teachers` DESC", result)
        self.assertIn("Result:", result)

    def test_youngest_teacher(self):
        question = "Who is the youngest teacher and what subject do they teach?"
        result = query_database(question)
        self.assertIn("SELECT `first_name`, `last_name`, `subject`, `age`", result)
        self.assertIn("FROM `teachers`", result)
        self.assertIn("ORDER BY `age` ASC", result)
        self.assertIn("LIMIT 1", result)
        self.assertIn("Result:", result)

    def test_students_with_highest_grades(self):
        question = "List the top 5 students with the highest average grades across all subjects"
        result = query_database(question)
        self.assertIn("SELECT s.`student_id`, s.`first_name`, s.`last_name`, AVG(g.`grade_value`) AS average_grade", result)
        self.assertIn("FROM `students` s", result)
        self.assertIn("JOIN `enrollments` e ON s.`student_id` = e.`student_id`", result)
        self.assertIn("JOIN `grades` g ON e.`enrollment_id` = g.`enrollment_id`", result)
        self.assertIn("GROUP BY s.`student_id`, s.`first_name`, s.`last_name`", result)
        self.assertIn("ORDER BY average_grade DESC", result)
        self.assertIn("LIMIT 5", result)
        self.assertIn("Result:", result)

if __name__ == '__main__':
    unittest.main()
