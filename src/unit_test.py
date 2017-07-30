import unittest
from html.parser import HTMLParser
import os
import MySQLdb
import MarkupProject

db = MySQLdb.connect(host="172.17.0.1", user="root", passwd="password", db="ssheffie")
cur = db.cursor()

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
        expected = "(('bob', -1),)"
        result = MarkupProject.retrieveLowestScored()
        self.assertEqual(result, expected)

    # Testing retrieve score given a unique id
    def test_retrieve_score(self):
        expected = "(('mark', 12),)"
        name = 'mark'
        result = MarkupProject.retrieveScore(name)
        self.assertEqual(result, expected)

    # Testing average score for all unique ids
    def test_average_score(self):
        expected = "(('bob', Decimal('4.5000')), ('mark', Decimal('12.0000')))"
        result = MarkupProject.averageScore()
        self.assertEqual(result, expected)

    # Testing retrieve highest score
    def test_retrieve_highest_scored(self):
        expected = "(('mark', 12),)"
        result = MarkupProject.retrieveHighestScored()
        self.assertEqual(result, expected)

    # Testing retrieve scores within a date range
    def test_retrieve_date_range(self):
        expected = "(('bob', -1), ('mark', 12))"
        startDate = "2000_01_01"
        endDate = "2007_01_01"
        result = MarkupProject.retrieveDateRange(startDate, endDate)
        self.assertEqual(result, expected)
    
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
