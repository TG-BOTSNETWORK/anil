# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.migrations import run_auto_migration
from app.api.routes import news, favorites, broadcast, auth

app = FastAPI()

# CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    run_auto_migration()

# ROUTES
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(news.router, prefix="/api/v1/news", tags=["News"])
app.include_router(favorites.router, prefix="/api/v1/favorites", tags=["Favorites"])
app.include_router(broadcast.router, prefix="/api/v1/broadcast", tags=["Broadcast"])

@app.get("/")
def root():
    return {"msg": "API is running 🚀"}