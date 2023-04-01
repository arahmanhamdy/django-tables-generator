## Tables Generator

Tables Generator written in Python using Django to dynamically create tables and add rows into the database. 

- [Quick Start](#Quick-Start)
    - [Installation](#installation)
    - [Running](#running)
- [OpenAPI](#openapi)

### Quick Start
- #### Installation
    ```bash
  git clone https://github.com/arahmanhamdy/django-tables-generator.git
  cd django-tables-generator
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt 
    ```

  - #### Running
    - Export environment variables for secrets
        ```bash 
        export SECRET_KEY="<SECRET_KEY>"
        export DATABASE_HOST="<DB_HOST>"
        export DATABASE_PORT="<DB_PORT>"
        export DATABASE_USER="<DB_USER>"
        export DATABASE_PASS="<DB_PASS>"
        export DATABASE_NAME="<DB_NAME>"
        ```
    - Apply migrations and run
      ```bash 
        python manage.py migrate
        python manage.py runserver
      ```
### OpenApi

The api is documented using OpanAPI Specs in [`openapi.yaml`](./openapi.yaml) and an online version of it can be viewed [here](https://tinyurl.com/table-generator-swagger)
