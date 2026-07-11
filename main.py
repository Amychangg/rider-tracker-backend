from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from features.users import router as users_router
from features.trips import router as trips_router
from features.road_map import router as road_map_router
from features.auth import router as auth_router


import uvicorn
from core.config import HOST


app = FastAPI()

app.include_router(users_router.router)
app.include_router(trips_router.router)
app.include_router(road_map_router.router)
app.include_router(auth_router.router)









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
    uvicorn.run("main:app", host=HOST, port=5678, reload=True)
