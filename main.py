# ################################################
#               IMPORTS & SETUP
# ################################################

import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from routes import PageRoutes, UserRoutes, AuthRoutes
from lib import AuthUtility, LayoutUtility
from starlette.routing import WebSocketRoute
import uvicorn


# Load environment variables from .env file
load_dotenv()
FASTAPI_PORT = int(os.getenv("FASTAPI_PORT", 5001))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"


# ################################################
#             UTILITY CLASS INSTANTIATION
# ################################################
auth = AuthUtility()
layout = LayoutUtility()



# ################################################
#             FASTAPI APP INITIALIZATION
# ################################################
# Create FastAPI application
app = FastAPI(lifespan=layout.arel.lifespan)  # Attach the lifespan handler to FastAPI


# ################################################
#             MIDDLEWARE CONFIGURATION
# ################################################
# middleware
app.add_middleware(GZipMiddleware)

# Authorization middleware
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    response = await auth.authorize_user(request, call_next)
    return response

@app.middleware("http")
async def no_cache_middleware(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    return response



# ################################################
#            STATIC FILES MOUNTING
# ################################################
app.mount("/public", StaticFiles(directory="public"), name="public")



# ################################################
#              ROUTE DEFINITIONS
# ################################################
auth_routes = AuthRoutes()
app.include_router(auth_routes.setup_routes())

pages_routes = PageRoutes()
app.include_router(pages_routes.setup_routes())

users_routes = UserRoutes()
app.include_router(users_routes.setup_routes())



# ################################################
#         HOT RELOAD WEBSOCKET ROUTE
# ################################################
app.router.routes.append(WebSocketRoute("/hot-reload", layout.arel.hotreload, name="hot-reload"))


# ################################################
#             DATABASE INITIALIZATION
# ################################################

# init_db()


# ################################################
#           STARTING THE FASTAPI SERVER
# ################################################
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=FASTAPI_PORT, reload=DEBUG)
