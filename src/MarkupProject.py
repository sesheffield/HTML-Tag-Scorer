from html.parser import HTMLParser
from flask import Flask, request
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import MySQLdb


app = Flask(__name__)

# Connect to MySQLdb with the host default ip gateway for docker (172.17.0.1)
# In docker made mysql password = password
db = MySQLdb.connect(host="172.17.0.1", user="root", passwd="password",
        db="RedVenture")
cur = db.cursor()

# Folder location
data_file = "/HTML-Tag-Scorer/data"

# Retrieve the unique id and the unique id date
def unique_id_and_date(infilename):
    # dirname is the directory, while fullfilename is the filename with extension
    # (.html)
    (dirname, fullfilename) = os.path.split(infilename)

    # filename without .html extension
    basename = os.path.splitext(fullfilename)[0]

    # split the filename for unique id name and date
    unique_id, unique_id_date = basename.split("_", 1)

    return unique_id, unique_id_date

# Scoring dictionary
tagDict = {"div": 3,
           "p": 1,
           "h1": 3,
           "h2": 2,
           "html": 5,
           "body": 5,
           "header": 10,
           "footer": 10,
           "font": -1,
           "center": -2,
           "big": -2,
           "strike": -1,
           "tt": -2,
           "frameset": -5,
           "frame": -5}

# Retrieve score given the unique id name
@app.route("/retrievescore/<name>")
def retrieveScore(name):
    cur.execute("SELECT name, score FROM markupProject WHERE name = %s", (name,))
    rows = cur.fetchall()
    return str(rows)

# Retrieve highest score 
@app.route("/retrievehighestscore")
def retrieveHighestScored():
    cur.execute('''SELECT name, score FROM markupProject 
            WHERE score = (SELECT max(score) FROM markupProject)''')
    rows = cur.fetchall()
    return str(rows)

# Retrieve lowest score
@app.route("/retrievelowestscore")
def retrieveLowestScored():
    cur.execute('''SELECT name, score FROM markupProject 
            WHERE score = (SELECT min(score) FROM markupProject)''')
    rows = cur.fetchall()
    return str(rows)

# Retrieve score within a certain date range
@app.route("/retrievescorerange")
def retrieveDateRange():
    startDate = request.args.get('start')
    endDate = request.args.get('end')
    return retreiveDateRange(startDate, endDate)

def retrieveDateRange(startDate, endDate):
    cur.execute('''SELECT name, score FROM markupProject 
            WHERE date BETWEEN %s
            AND %s ORDER BY name''', (startDate, endDate,))
    rows = cur.fetchall()
    return str(rows)

# Return the average score for each unique id
@app.route("/averagescore")
def averageScore():
    cur.execute('''SELECT name, AVG(score) FROM markupProject GROUP BY name
            ORDER BY name''')
    rows = cur.fetchall()
    return str(rows)

# Upsert command to insert into table if unique id and date are unique,
# otherwise, update the row
def upsert(unique_id, unique_id_score, unique_id_date):
    cur.execute('''INSERT INTO markupProject 
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
            score = %s;''', 
            (unique_id, unique_id_score, unique_id_date, unique_id_score))

# Print the contents of the table
@app.route("/print")
def printTable():
    cur.execute("SELECT name, score, date FROM markupProject")
    rows = cur.fetchall()
    return str(rows)

# Create the table
def createTable():
    cur.execute('''CREATE TABLE IF NOT EXISTS markupProject
            (name VARCHAR(255) NOT NULL,
            score INT NOT NULL,
            date date NOT NULL,
            UNIQUE KEY (name, date));''')

# Score the html file and store the results into database
def store_results(infilename, unique_id, unique_id_date):
    filename = open(infilename, "r")
    html = filename.read()
    parser = MyHTMLParser()
    parser.feed(html)
    upsert(unique_id, parser.totalScore, unique_id_date)
    db.commit()
    # Rest the total score count to 0
    MyHTMLParser.totalScore = 0

"""
HTML parser class
"""
# Create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    totalScore = 0
    def handle_starttag(self, tag, attrs):
        # Set tag to lower for case-insensitive
        tag = str(tag).lower()
        if tag in tagDict:
            MyHTMLParser.totalScore += tagDict.get(tag)

"""
Watchdog: check for changes in data folder
    Watcher class
    Handler class
"""
class Watcher:
    DIRECTORY_TO_WATCH = "/HTML-Tag-Scorer/data"
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH,
                recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")
        self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created' or event.event_type == 'modified':
            if event.src_path.endswith('.html'):
                unique_id, unique_id_date = unique_id_and_date(event.src_path)
                store_results(event.src_path, unique_id, unique_id_date)


"""
Threading Functions:
    watch_directory()
    web_server()
""" 

# Watch data directory for incoming html files
def watch_directory(w):
    w.run()


# Get requests from web server
def web_server():
    app.run(host='0.0.0.0')


# Main method to extract .html files in folder, calculate score, and store into
# database
def main():
    for directory, subdirectories, files, in os.walk(data_file):
        for file in files:
            if file.endswith(".html"):
                infilename = os.path.join(directory, file)
                unique_id, unique_id_date = unique_id_and_date(infilename)
                store_results(infilename, unique_id, unique_id_date)


if __name__ == "__main__":
    # Call main method to startup entire process
    main()

    # Intantiate a Watcher
    w = Watcher()

    # Create thread for web server 
    web_server_thread = Thread(target=web_server)
    # Create thread for polling directory
    watch_directory_thread = Thread(target=watch_directory, args=(w,))

    # Start up the threads
    web_server_thread.start()
    watch_directory_thread.start()

    #db.close()

