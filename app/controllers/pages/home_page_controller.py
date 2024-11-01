from fastapi import Request, Response

async def home_page_controller(request:Request, response:Response):
    return 'This is a FastAPI CRUD app!'