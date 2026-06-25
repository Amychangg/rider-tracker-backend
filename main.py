from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from features.users import router as users_router
from features.trips import router as trips_router
import uvicorn


app = FastAPI()

app.include_router(users_router.router)
app.include_router(trips_router.router)







app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.get("/")
def root() -> str:
    return "ha server running"











if __name__ == "__main__":
    uvicorn.run("main:app", host="172.16.16.77", port=5678, reload=True)
