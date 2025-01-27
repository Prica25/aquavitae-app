<h1 align="center">
<br>
    <img src="./src/static/images/thumbnail_AquaeVitae_Logo.png" width="350">
<br>
    Aquavitae App
<br>
</h1>

<h4 align="center">
    Software to track patients who are on nutritional diets and allow the patient and nutritionist to see the progress.
<br>
<br>
<div align="center">
    <img src="https://img.shields.io/badge/python-%23007ACC.svg?&style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="Postgres">
</div>
</h4>

## How to execute
To build the project run the following commands in terminal, step by step:

### Manually
1. Creating a virtual environment with pipenv
    ```
    $ cd /path/to/project
    $ pip install pipenv
    $ pipenv install
    ```
  
    1. Make sure pip is using python version **3.9**
    2. If you have problems installing the ***psycopg2*** package run the following commands:
       ```
       $ sudo apt install libpq-dev python3.9-dev
       $ pipenv install
       ```

2. Creating the Postgres database using docker
    ```
    $ sudo apt install docker docker-compose
    $ docker pull postgres
    $ docker run --name <CONTAINER_NAME> -e POSTGRES_USER=<DATABASE_USER> -e POSTGRES_PASSWORD=<DATABASE_PASSWORD> -p 5432:5432 -d postgres
    ```
  
3. Create or update the database with **alembic**
    ```
    $ alembic upgrade head
    ```
  
4. Execute the project
    ```
    $ python src/main.py
    ```
   
5. Fill the database with initial data
    ```
    $ python src/core/scripts/initial_data/main.py
    ```
   
### With Docker
1. Have Docker and Docker Compose installed
    ```
    $ sudo apt install docker docker-compose
    ```
   
2. Run the following command in the project *root* directory
    ```
    $ docker-compose up
    ```
   
3. Open the application docker terminal to create the tables in the database and fill them with the necessary initial 
data 
    ```
    $ docker exec -it <CONTAINER_NAME> bash
    $ alembic upgrade head
    $ python src/core/scripts/initial_data/main.py
    ```

  
## How to execute the tests
1. In the **.env** file put your  ```APP_ENV=test ```
2. Execute the following commands in terminal:
    - Create or update the test database with **alembic**
      ```
      $ cd /path/to/project
      $ alembic upgrade head
      ```
      
    - Execute all the tests
      ```
      $ python -m pytest
      ```

       * *Note*: You can also run in terminal just ```$ pytest```
       * *Note*: To get the code coverage you can add the following parameters ```--cov=. --cov-report=html```
       * *Note*: To get performance reports you can add the following parameter ```--report-log reportlog.jsonl```
         * To view the generated report run ```$ pytest-duration-insights explore reportlog.jsonl```

## License
[MIT License](/LICENSE.md)
