from fastapi import FastAPI
from python_fastapi.app.api.v1.users import router as user_router
import uvicorn
app = FastAPI()
app.include_router(user_router)

if __name__ == "__main__":
  uvicorn.run("addison_example:app", reload=True, host="0.0.0.0", port=8000)