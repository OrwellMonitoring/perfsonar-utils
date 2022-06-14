# PerfSonar Utils

Utils that abstract the interaction with PerfSonar. It includes debugging scripts, code samples, installation scripts and a Kafka connector.

## Esmond Scripts
In the `esmond` folder there are 4 debugging scripts for interacting with the esmond API, which is where test results are stored. 

 - `python3 get-tests.py` - Prints all the tests available
 - `python3 get-test-events.py <test-key>` - Prints all the events for a specific test. Events are the metrics' labels
 - `python3 get-test-event-base-result.py <test-key> <event-type>` - Prints event values' information
 - `python3 get-test-event-summary-result.py <test-key> <event-type> <summary> <window>` - Prints event values' information, but not in its raw form, the data is transformed, usually, by aggregation or statistic analysis

## Pscheduler Scripts
In the `pscheduler` folder there are 3 debugging scripts for interacting with the pscheduler API, which is PerfSonar's component responsible for scheduling test runs. 

 - `python3 get-tasks.py` - Tests loading all tasks' urls
 - `python3 create-tasks.py` - Tests importing the tasks defined in `config.json`
 - `python3 clean-tasks.py` - Cancels all tasks

## Init Scripts
Inside of the `init` folder is where the two PerfSonar's initialization scripts are found, for the Toolkit and Testpoint versions. Both scripts start docker containers but , unfortunatly, we were not able to transform these scripts into Docker images because of the required dependencies of the systemd service while installing.

Both scripts use the included `ntp.conf` file, which sets up the NTP service inside of the containers. If your network blocks some NTP servers you may have to update this file for your situation, as tests will only run if both intervinients are in sync.

For the `perfsonar_toolkit_init.sh` script you should replace the ip address in `esmond_manage add_user_ip_address user 10.0.12.82` for the ip address running any script that interacts with the esmond API. You may run that command as many times as you wish if more than one address is required.

## Pull Service
Service responsible for pulling metrics from the esmond API and sending them to Kafka so that a translator can afterwards integrate PerfSonar's metrics with the rest of the system. For this script both `BASE_URL` (PerfSonar toolkit address) and `KAFKA_URL` source address must be updated for the specific case.
