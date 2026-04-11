from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, SessionLocal, engine
from app.routers.web import router as web_router
from app.services.seed_data import seed_database

app = FastAPI(title='Customer AI Agent MVP', version='0.1.0')
app.mount('/static', StaticFiles(directory='app/static'), name='static')
app.include_router(web_router)


@app.on_event('startup')
def startup_event():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


@app.get('/health')
def health():
    return {'status': 'ok'}
