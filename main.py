import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from app.routes import AuthRoutes, PageRoutes, UserRoutes
from app.lib import AuthUtility
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.database.db import init_db


# ###########################################################################
#                               APP CREATION 
# ###########################################################################

# Load Environment Variables 
load_dotenv()
FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", 5001))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Instantiate Auth Utility
auth = AuthUtility()

# Create FastAPI App
app = FastAPI()  


# ###########################################################################
#                                MIDDLEWARE 
# ###########################################################################

# GZip
app.add_middleware(GZipMiddleware)


# CORS Middleware - Allow All
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],             # Allows all origins
    allow_credentials=True,          # Allows credentials such as cookies or authorization headers
    allow_methods=["*"],             # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"]              # Allows all headers
)


# No Response Caching Middleware
@app.middleware("http")
async def no_cache_middleware(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    return response


# Authorization Middleware
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    response = await auth.authorize_user(request, call_next)
    return response


# ###########################################################################
#                                  ROUTES
# ###########################################################################

# Auth API
auth_routes = AuthRoutes()
app.include_router(auth_routes.setup_routes())

# Page API
page_routes = PageRoutes()
app.include_router(page_routes.setup_routes())

# User API
users_routes = UserRoutes()
app.include_router(users_routes.setup_routes())


# ###########################################################################
#                               START SERVER
# ###########################################################################
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=FASTAPI_PORT, reload=DEBUG)
