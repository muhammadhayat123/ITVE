from dotenv import load_dotenv
from fastapi import FastAPI
from routes.user_route import user_route


load_dotenv()

app = FastAPI()



# routes
app.include_router(user_route, prefix="", tags=["User"])


