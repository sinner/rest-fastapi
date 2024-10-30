# FastAPI & SQLAlchemy

1. You should have already installed python 3.11.1+ in your OS
2. Install poetry

```bash
pip install poetry
pip3 install poetry
```

1. Once you have installed poetry you could start your project with a virtual environment. Take into account that the 

```bash
# It will start a new project with the OS python version
poetry init

# It will start a new project with the specified python version
poetry init --python 3.11.9
```

1. Open the poetry shell, it will allow you to get into the virtual environment created by poetry:

```bash
poetry shell
```

1. Install the dependencies (FastAPI & Uvicorn)

```bash
poetry fastapi uvicorn
```

1. Let’s create an `app` python package
2. Let’s create a `main.py` file into the `app` python package with the following code

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

1. Let’s create a `controllers`  python package with a controller file.

```python
# app/controllers/health_check.py
from fastapi import APIRouter

from app.config.database import db_connection

router = APIRouter(
    prefix="/health-check",
    tags=["Health Check"]
)

@router.get("/api")
async def api_health_check():
    return {"status": "ok"}

```

1. Modify the `app/main.py` file to include the new controller into the app:

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.health_check import router as health_check_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_check_router)
```

1. SQLAlchemy integration. Let’s install sqlalchemy ORM as a dependency and psycopg2 as the database connection library due to my RDMS is Postgresql. I will install alembic library to manage the sqlalchemy migrations.

```bash
poetry add sqlalchemy psycopg2-binary alembic
```

1. Let’s create the database configuration with SQLAlchemy ORM. It will be into the `app/config/database.py`

```python
# app/config/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@postgresqlserverhost:port/db_name"

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def db_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

```

The DATABASE_URL variable contains the connection string to your database. The database should be already created and you should have a connection to it.

1. Let’s integrate SQLAlchemy with FastAPI

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.health_check import router as health_check_router
from app.config.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_check_router)

```

1. Integrate alembic with sqlalchemy:

```bash
alembic init migrations
```

`migrations` is the name of the directory that will hold the migration code and it will be created by alembic.

![Screen Shot 2024-07-22 at 4.39.38 PM.png](FastAPI%20&%20SQLAlchemy%20562a667999154116b2004d19285340b0/Screen_Shot_2024-07-22_at_4.39.38_PM.png)

Let’s setup the alembic configuration.

13.1. Modify the `file_template` variable into the `alembic.ini` file that should be into the root of the project. This change will allow us to modify the migration files name to me displayed chronologically. For doing we will find for the `file_template` variable and we will add the following line:

```bash
file_template = %%(epoch)s_%%(rev)s_%%(slug)s
```

13.2. Let’s configure the `sqlalchemy.url` variable and set the proper DB connection string

```bash
sqlalchemy.url = postgresql+psycopg2://user:password@localhost:5432/db_name
```

13.2 Let’s modify the `migrations/env.py` file to add the DB metadata:

```python
from app.config.database import Base

target_metadata = Base.metadata
```

13.3 Let’s add the proper value to the `url` variable that you will find into the `run_migrations_offline`  function and set the following value:

```python
import os

url = config.get_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
```

13.4 The most important thing is that you should import all your models ensuring that they are imported to register their metadata.

```python
from app.models import User, Task
```

Execute the following command to generate the migrations based on the models

```bash
alembic revision --autogenerate -m "My Slug Message"
```

Then, review the generated migration file into your `migrations/versions` directory and if everything is ok and as it is expected you can apply the changes to your databases executing the following command 

```bash
alembic upgreade head
```