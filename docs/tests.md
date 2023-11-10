# Testing the server

## Running Unit test for Server
We have unit tests in run_test.py. The purpose of this unit tests is to make sure that we didn't break any code when we made any changes. The unit test currently only checks if the code successfuly run. It doesn't check the accuracy fo the results. 
The unit tests currently checks:
1. The CLI command to run the analytics and validation server
2. The API endpoints that run the analytics and validation server. We check for all 4 environments (Docker, Production, Staging and Local)
3. The server performance via Locust Load Test. We check the performance for all 4 environments

To run the tests:
Run `python3 run_test.py` to run the unit tests

## Load testing the server
The run_load_test.py script is used to stress test the analytics services. The testing is performed using Locust, a powerful open-source load testing tool that allows you to define user behavior with Python code.
To start the load testing:
1. Start locust by running `locust -f run_load_test.py --class-picker`
2. Once Locust is running, you can access its web interface at: http://localhost:8089
3. In the Locust web UI, you'll have the option to configure the number of users to simulate, the spawn rate, the host to attack and the API to test. 
- UserClasses: The API endpoint to test
- Number of Users: The total number of simulated users to spawn.
- Spawn Rate: The rate at which to spawn the users (users per second).
- Host: The target host for the testing (e.g., http://localhost:8000). If no host is given, the code will run against local by default.
4. Click the "Start Swarming" button to initiate the test.


### Metrics Provided by Locust
Locust provides real-time statistics on the web UI, including:
- RPS (Requests Per Second): The number of requests made per second.
- Average Response Time: The average response time for requests.
- Min/Max Response Time: The minimum and maximum response times.
- Number of Failures: The number of failed requests.
- Users: The current number of active simulated users.
You can also download the statistics as a CSV file for further analysis.

