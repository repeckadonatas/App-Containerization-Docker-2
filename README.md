# Capstone 2
# Commodities Price Movement Prediction (Precious Metals)


## About

This project is an exercise in translating business requirements into data engineering tasks. The project has to envelop the use of Python, SQL and Docker and the resulting data from the database must be utilised in training the ML model for predicting the priece of commodities (precious metals in this sample case).

For real world price data a **[Metals.Dev](https://metals.dev/)** API is used. After the data is downloaded, it is then transformed and prepared to be uploaded to the database. 

The program uses Threading as a concurrency method. Threading is suitable when looking to parallelize heavy I/O work, such as HTTP calls, reading from files and processing data.


## Tech Stack Used

* Programing language - **Python**;
* Data storage and querying - **PostgreSQL**;
* For testing data preparation functions - **Jupyter Notebook**;
* Data cleaning and normalization - **Pandas**;
* Package and dependency management - **Poetry**;
* Containerization and Image storage - **Docker**, **DockerHub**.


## Project Deliveries Plan(FIX!!!!)

* **Database**:
  * For a database I chose PostgreSQL as it offers more features than some other databases (i.e. MySQL), it is free, easy-to-implement database management system and is better suited for enterprise-level applications. As this project assumes I am a part of a hedge fund specializing in developing bespoke trading strategies by using the latest technologies, a database suited for enterprise is a logical choice.

* **Data preparation**:
  * A successful response to an API call returns JSON files that are then stored in `source/data/` folder. Using **Pandas**, dataframes are created from JSON files. There is only one (1) change done to dataframes of JSON files - the names of the columns are changed to conform to snake case.

* **Data upload to a database**:
  * Once the data is prepared for uploading, datasets are first placed in a queue and after matching the datasets with the tables in a database, the data is then uploaded to corresponding tables.

* **Tables**(FIX!!!!):
  * The database contains multiple tables for data storage. For storing historical real world data, there are separate tables for every metal:
    * `gold_historic`
    * `silver_historic`
    * `platinum_historic`
    * `palladium_historic`
  * For analytical purposes, the data of these tables is contained in a single table `commodities_price_data`.
  * For ML training purposes, ...


## How To Use The Program(FIX!!!!)

### 1. Using Docker

To run the program in a Docker container:
- Download the `docker-compose.yml` file of this project.
- In the terminal window run `docker compose -f docker-compose.yml up` command.
- For **presentation purposes**, environment variables can be baked into the environment of app's Docker Image.
- The Image of the application is pulled from a public repository on Docker Hub.

\
For a **Production application:**
- Create and store `.env` file in the same folder as `docker-compose.yml`.
- For a more secure method of keeping secrects, Dockerfile should first be built using `RUN --mount=type=secret`. This mount type allows the build container to access secure files such as private keys without baking them into the image. Another method would be to utilize **GitHub Secrets** or a similar service to hide secrets.
- The Docker Image should be stored in a secure Image container.

\
Running the project with Docker will use **PostgreSQL** database image from `https://hub.docker.com/_/postgres/` and the image of **Commodities-Price-Movement** app from my publicly available **[Docker Hub](https://hub.docker.com/repository/docker/notexists/kaggle-data-download-app/general)** repository.
The Docker compose YML file should be on a target machine first.

**Note:**

Every time the program runs, a log file is created in `logs` folder for that day. Information about any subsequent run is appended to the log file of that day. The program logs every data download, data transformation and data upload to the database. Errors are also logged into the same log file for the current day of the run.


When running `docker-compose.yml` on a target machine, in order to store logs, the `volumes` section for the `project-app` should be adjusted accordingly. For **presentation purposes** logs are directed to be stored in the projects folder.

- To restart the program, run `docker compose -f docker-compose.yml down` and then `docker compose -f docker-compose.yml up`.


### 2. Running manually locally

Prior to running the program, dependencies from `pyproject.toml` file should be installed. Use `Poetry` package to install project dependencies:
* `pip install poetry`
* `poetry install --no-root`

The basic usage on `Poetry` is **[here](https://python-poetry.org/docs/basic-usage/#installing-dependencies)**.
Once dependency installation is completed, the program can now be used. 

To use the program, run the _`main.py`_ file. Once started, the API data download will begin, followed by data preparation and then data upload to respective tables on a database.

\
**Note:**

Every time the program runs, a log file is created in `logs` folder for that day. Information about any subsequent run is appended to the log file of that day. The program logs every data download, data transformation and data upload to the database. Errors are also logged into the same log file for the current day of the run.

- To restart the program, run _`main.py`_ again if the app is being run locally.

### **Important:**

1. **For database connection:**

To connect to the database, the `source/db_functions/db_functions.py` file needs to read connection values from `.env` file:

|                             |
|-----------------------------|
| PGUSER = db_username        | 
| PGPASSWORD = user_password  | 
| PGHOST = host_name          |
| PGPORT = port               |
| PGDATABASE =  database_name |

\
1.1. **For PostgreSQL Docker image:**

When using Docker, **PostgreSQL** needs **POSTGRES_USER** and **POSTGRES_PASSWORD** environment variables to be passed. For this reason the YML file can be set up to read these environment variables from `.env` file.

For **presentation purposes**, environment variables can be passed securely to Dockerfile first using `RUN --mount=type=secret`.

1.2 **To Connect to a PostgreSQL database from OUTSIDE the Docker container:**

When connecting to a database from **outside** the Docker container, for connection parameters in database connection window use **PORT**, **DATABASE**, **USER** and **PASSWORD** variables (**HOST** variable is not needed in most cases. If needed, use `host.docker.internal`).

\
**Note:**

When using the code manually locally, store the `.env` file in the root directory of the project folder to connect to the database and use it with no issues.

## Using ML model(FIX!!!!)

To use the ML model for price movement prediction of target commodities, ...


## Concurrency method used

The program uses Threading as concurrency method to fetch, transform and upload the data. Threading is suitable when looking to parallelize heavy I/O work, such as HTTP calls, reading from files and processing data. 

Here, Python's own `threading` and `concurrent.futures` modules are used. The `concurrent.futures` module provides a high-level interface for asynchronously executing callables. The asynchronous execution is performed with threads using `threading` module.
The `concurrent.futures` module allows for an easier way to run multiple tasks simultaneously using multi-threading to go around GIL limitations.


Using **ThreadPoolExecutor** subclass uses a pool of threads to execute calls asynchronously. All threads enqueued to **ThreadPoolExecutor** will be joined before the interpreter can exit.
