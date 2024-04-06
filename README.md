# Capstone
# Price Movement Predictions of Precious Metals


## About(FIX!!!!)

This project is an exercise in translating business requirements into data engineering tasks.


This project is an exercise in building a working data pipeline model that would be later containerized for easier future replication on other machines and systems. The program retrieves two CSV files that are a part of **[Loan Eligible Dataset](https://www.kaggle.com/datasets/vikasukani/loan-eligible-dataset)** from Kaggle. After the data is downloaded, it is then transformed and prepared to be uploaded to the database. The program uses Threading as a concurrency method. Threading is suitable when looking to parallelize heavy I/O work, such as HTTP calls, reading from files and processing data.


## Tech Stack Used(FIX!!!!)

* Programing language - **Python**;
* Data storage and querying - **PostgreSQL**;
* For testing data preparation functions - **Jupyter Notebook**;
* Data cleaning and normalization - **Pandas**;
* Package and dependency management - **Poetry**;
* Containerization and Image storage - **Docker**, **DockerHub**.


## How To Use The Program(FIX!!!!)

### 1. Using Docker

To run the program in a Docker container:
- Download the `docker-compose.yaml` file of this project.
- In the terminal window run `docker compose -f docker-compose.yaml up` command.
- For **presentation purposes**, environment variables are already in the environment of app's Docker Image.

\
For a **Production application:**
- Create and store `.env` file in the same folder as `docker-compose.yaml`.
- The Docker Image should be rebuilt to take into account the `.env` files variables and the Image itself should be stored in a secure Image container.

\
Running the project with Docker will use **PostgreSQL** database image from `https://hub.docker.com/_/postgres/` and the image of **FinTech-Loan-Modelling** app from my publicly available **[Docker Hub](https://hub.docker.com/repository/docker/notexists/kaggle-data-download-app/general)** repository.
The Docker compose YAML file should be on a target machine first.

**Note:**

Every time the program runs, a log file is created in `logs` folder for that day. Information about any subsequent run is appended to the log file of that day. The program logs every data download, data transformation and data upload to the database. Errors are also logged into the same log file for the current day of the run.


When running `docker-compose.yaml` on a target machine, in order to store logs, the `volumes` section for the `project-app` should be adjusted accordingly.

- To restart the program, run `docker compose -f docker-compose.yaml down` and then `docker compose -f docker-compose.yaml up`.


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

To connect to the database, the `Source/db_functions/db_functions.py` file needs to read these values from `.env` file:

|                             |
|-----------------------------|
| PGUSER = db_username        | 
| PGPASSWORD = user_password  | 
| PGHOST = host_name          |
| PGPORT = port               |
| PGDATABASE =  database_name |

\
1.1. **For PostgreSQL Docker image:**

When using Docker, **PostgreSQL** needs POSTGRES_USER and POSTGRES_PASSWORD environment variables to be passed. For this reason the YAML file reads these environment variables from `.env` file.

1.2 **To Connect to a PostgreSQL database from OUTSIDE the Docker container:**

When connecting to a database from **outside** the Docker container, for connection parameters in database connection window use PORT, DATABASE, USER and PASSWORD variables (HOST variable is not needed in most cases. If needed, use `host.docker.internal`).

\
2. **For Kaggle API to work:**

Kaggle API usage is set up using the official Kaggle **[documentation](https://www.kaggle.com/docs/api)** (**[Kaggle GitHub](https://github.com/Kaggle/kaggle-api)**). Kaggle API requires a **kaggle.json** file to be stored in a home directory. For Windows it is `C:\Users\<user_name>\.kaggle`. For Unix systems it is `~/.kaggle`. The file can be generated by signing up to Kaggle and going into your account settings. The code implements a workaround for this JSON file location, but it might not work properly (might be a Kaggle API problem). For this reason, the Dockerfile copies the **kaggle.json** file from the source of the program to `/root/.kaggle/` location in Docker image, so no problems should occur. For redundancy and workaround reasons, `.env` file also needs to contain **kaggle.json** credentials:

|                                   |
|-----------------------------------|
| KAGGLE_USERNAME = kaggle_username | 
| KAGGLE_KEY = kaggle_api_key       |

\
**Note:**

When using the code manually locally, store the `.env` file in the root directory of the project folder to connect to the database and use the Kaggle API with no issues. Also make sure that **kaggle.json** file is stored in a home directory as well as in `Source/.kaggle/`. For Windows the home directory is `C:\Users\<user_name>\.kaggle`. For Unix systems it is `~/.kaggle`.


## Input Dataset Preparation(FIX!!!!)

A successful response to an API call produces a ZIP file that is then stored in `Source/data/` folder. Then the ZIP file contents are extracted in the same location.

There is only one (1) change done to both dataframes of CSV data - the names of the columns are changed to conform to snake case.


## Concurrency method used(FIX!!!!)

The program uses Threading as concurrency method to fetch, transform and upload the data. Threading is suitable when looking to parallelize heavy I/O work, such as HTTP calls, reading from files and processing data. 

Here, Python's own `threading` and `concurrent.futures` modules are used. The `concurrent.futures` module provides a high-level interface for asynchronously executing callables. The asynchronous execution is performed with threads using `threading` module.
The `concurrent.futures` module allows for an easier way to run multiple tasks simultaneously using multi-threading to go around GIL limitations.


Using **ThreadPoolExecutor** subclass uses a pool of threads to execute calls asynchronously. All threads enqueued to **ThreadPoolExecutor** will be joined before the interpreter can exit.






## Project Deliveries Plan

* **Database**:
  * For a database I chose PostgreSQL as it offers more features than some other databases (i.e. MySQL), it is free, easy-to-implement database management system and is better suited for enterprise-level applications. As this project assumes I am a part of an experimental Netflix team, a database suited for enterprise is a logical choice.
  * For testing purposes, I created `db_analyst` and `db_scientist` users and gave them appropriate grants to use `db_users` schema and tables in it.
  * `/misc` folder contains SQL code used to create users, schema and add tables to schema, create relationships between tables.
####
* **Data normalization**:
  * To normalize data I use **Jupyter Notebook** with **Pandas** module. The `data_cleaning.py` file contains functions used to inspect, clean and normalize datasets. 
####
* **Database usage**:
  * The database can be manipulated by using Python code. The code allows for ad hoc functionality (`test`, `create`, `copy`, `check`) to quickly create new tables, populate them with data, check the existing tables in the database. For table creation and data copying I use `.txt` files from `/misc` folder.
  * The program also allows the user to write their own SQL code and pass it to the database to read and write data (read and write privileges depend on the user connected to the database).
####
* **Tables**:
  * Only two tables - `new_raw_titles_2nf` and `raw_credits_2nf` are stored in the database as all other tables are just derived from these two tables, so data duplication in this case is not necessary, as to save space on the database (useful when the database is cloud-based as you usually pay for the storage of a database). These tables are placed under `public` schema that can only be accessed by a 'db_admin' user.
  * Any other helper tables are derived from these tables. All tables that can be accessed by `db_analyst` and `db_scientist` users are placed under `db_users` schema.
####
* **Output data**:
  * Normalized tables are stored in `Source/data/output/` folder. While it may not be the best way to store data, I chose to do this so that if the primary data in a database gets corrupted or lost, the data could be recreated faster.