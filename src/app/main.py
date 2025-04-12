from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()

"""
Define the allowed origins for CORS.
"""
origins = [
    "[http://127.0.0.1](http://127.0.0.1):8033",
    "http://localhost:8033",
]

"""
Add CORS middleware to the app.
"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
Import and include routers for the app.
"""
from app.routes import auth, contacts, user 
app.include_router(contacts.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")


def main():
    """
    Run the app using uvicorn.
    """
    try:
        uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True, workers=2)
        logging.info("App started")
    except Exception as e:
        logging.error(f"Error starting app: {e}")

if __name__ == "__main__":
    main()