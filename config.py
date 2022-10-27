from sqlite3 import version
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')



class Settings:
    title="GKM_IT Project"
    description="""
This API helps you do awesome stuff. 🚀

## Flats

You can **read,create, update and delete Flat details**.

## Users

You will be able to:

* **Create users** .
* **Read users** .
"""
    version="0.0.1"
    terms_of_service="http://example.com/terms/"
    contact={
        "name": "Sheersh Jain",
        "email": "sheersh@gkmit.co",
    }
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
    DATABASE_URL= os.getenv("POSTGRES_URL")
    tags_metadata = [
        {
            "name": "Users",
            "description": "Operations with users. The **login** logic is also here.",
        },
        {
            "name": "Flats",
            "description": "Manage items. So _fancy_ they have their own docs.",
            "externalDocs": {
                "description": "Items external docs",
                "url": "https://fastapi.tiangolo.com/",
            },
        }
    ]
    SECRET_KEY= os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    TEST_EMAIL="sheersh@gkmit.co"
    TEST_PASS = "SHEERSH"
    

    

setting=Settings()