Instructions (Mac/Linux)
- Download and install Docker
    - https://docs.docker.com/engine/installation/
- Clone from git
- Once repository is created, change directory to HTML-Tag-Scorer and execute “./run.sh” in command line.
- A web server and directory watchdog will be running concurrently so that you can call web methods in the web browser to view the results. 
- Once the application finishes running (takes a few minutes to finish), open a web browser to call methods to print to the web browser:
    - To run the lowest score method:
        - http://0.0.0.0:5000/retrievelowestscore 
    - To run the highest score method:
        - http://0.0.0.0:5000/retrievehighestscore 
    - To run the average score method
        - http://0.0.0.0:5000/retrieveaveragescore 
    - To run retrieve score method given a unique id:
        - http://0.0.0.0:5000/retrievescore/{unique_id}  
            - For unique_id, enter a name
    - To run retrieve score within a ranged date:
        - http://0.0.0.0:5000/retrievescorerange?start={startDate}&end={endDate}
            - For startDate and endDate, use format yyyy_mm_dd without quotes 
            - ex: ...?start=2000_01_01&end=2020_01_01 
    - To print the database table:
        - http://0.0.0.0:5000/print 
- The polling of a directory allows you to drop off an .html file in the ./data folder. The application automatically parses the file and stores the results into the database.
    - Drop off .html file in data folder to insert into database
- The application will continue to run in the background. To stop the application use Ctrl-c
