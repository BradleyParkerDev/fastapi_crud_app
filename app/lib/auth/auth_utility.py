from fastapi import Request, Response

class AuthUtility():

    async def authorize_user(self, request:Request, call_next):
        print("Authorization Middleware!!!")
        response = await call_next(request)
        response.set_cookie(key="session_cookie", value="This is a session cookie!", httponly=True)
        return response 
