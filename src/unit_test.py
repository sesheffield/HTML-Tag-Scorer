import unittest
from html.parser import HTMLParser
import os
import MySQLdb
import MarkupProject

db = MySQLdb.connect(host="172.17.0.1", user="root", passwd="password", db="RedVenture")
cur = db.cursor()

# Returning the raw data without "pretty" features
def results(result):
    x, result_unique_id, result_score, y = result.split("|")
    result_unique_id = result_unique_id.strip()
    result_score = result_score.strip()
    return result_unique_id, result_score

# Returning the raw data without "pretty" features
def multiresults(result):
    result = result.replace("<br>", "")
    x, result_unique_id1, result_score1, y, result_unique_id2, \
    result_score2, z = result.split("|")
    result_unique_id1 = result_unique_id1.strip()
    result_score1 = result_score1.strip()
    result_unique_id2 = result_unique_id1.strip()
    result_score2 = result_score1.strip()
    return result_unique_id1, result_score1, result_unique_id2, result_score2


class MarkupProjectTestCase(unittest.TestCase):

    # Create table used in MarkupProject.py
    # Insert default values into database for unit testing
    @classmethod
    def setUpClass(cls):
        MarkupProject.createTable()
        query = """
        INSERT INTO markupProject (name, score, date)
        VALUES ('bob', 10, "2010_05_05"),
               ('mark', 12, "2005_07_12"),
               ('bob', -1, "2000_05_01");
        """
        cur.execute(query)
        db.commit()

    # Testing retrieve lowest score
    def test_retrieve_lowest_scored(self):
        expected_unique_id = "bob"
        expected_score = "-1"
        result = MarkupProject.retrieveLowestScored()
        result_unique_id, result_score = results(result)
        self.assertEqual(result_unique_id, expected_unique_id)
        self.assertEqual(result_score, expected_score)

    # Testing retrieve score given a unique id
    def test_retrieve_score(self):
        expected_unique_id = "mark"
        expected_score = "12"
        name = 'mark'
        result = MarkupProject.retrieveScore(name)
        result_unique_id, result_score = results(result)
        self.assertEqual(result_unique_id, expected_unique_id)
        self.assertEqual(result_score, expected_score)

    # Testing average score for all unique ids
    def test_average_score(self):
        expected_unique_id1 = "bob"
        expected_score1 = "4.5000"
        expected_unique_id2 = "mark"
        expected_score2 = "12.000"
        result = MarkupProject.averageScore()
        result_unique_id1, result_score1, result_unique_id2, result_score2 = \
                multiresults(result)
        self.assertEqual(result_unique_id1, expected_unique_id1)
        self.assertEqual(result_score1, expected_score1)
        self.assertEqual(result_unique_id2, expected_unique_id1)
        self.assertEqual(result_score2, expected_score1)


    # Testing retrieve highest score
    def test_retrieve_highest_scored(self):
        expected_unique_id = "mark"
        expected_score = "12"
        result = MarkupProject.retrieveHighestScored()
        result_unique_id, result_score = results(result)
        self.assertEqual(result_unique_id, expected_unique_id)
        self.assertEqual(result_score, expected_score)

    # Testing retrieve scores within a date range
    def test_retrieve_date_range(self):
        expected_unique_id1 = "bob"
        expected_score1 = "-1"
        expected_unique_id2 = "mark"
        expected_score2 = "12"
        startDate = "2000_01_01"
        endDate = "2007_01_01"
        result = MarkupProject.retrieveDateRange(startDate, endDate)
        result_unique_id1, result_score1, result_unique_id2, result_score2 = \
                multiresults(result)
        self.assertEqual(result_unique_id1, expected_unique_id1)
        self.assertEqual(result_score1, expected_score1)
        self.assertEqual(result_unique_id2, expected_unique_id1)
        self.assertEqual(result_score2, expected_score1)
    
    # Remove test data from database
    @classmethod
    def tearDownClass(cls):
        query = """
        DELETE FROM markupProject;
        """
        cur.execute(query)
        db.commit()

if __name__ == '__main__':
    unittest.main()
