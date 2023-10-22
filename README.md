# FastAPI project
Contain User API
- Login
- Signup
- Get login user detail

## Setup
### Server
 ```bash
    # create virtual env
    python -m venv .
    # install dependencies
    pip install -r requirements.txt
```
### Database
- Run Query in db_query.sql
- Configure postgres credentails and host in .env file

##
## To run Project
 ```bash
uvicorn main:app --reload
 ```
## Swagger Url
127.0.0.1:8000/docs

