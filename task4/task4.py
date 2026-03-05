from datetime import datetime


from fastapi import FastAPI, Query
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from playwright.sync_api import sync_playwright


import uvicorn


# ===== БД =====
DATABASE_URL = "postgresql://postgres:MrLogan555@localhost:5432/parser_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class NetworkRequest(Base):
    __tablename__ = "network_requests"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    method = Column(String)
    resource_type = Column(String)
    headers = Column(JSON)
    source_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)
app = FastAPI()


# ===== Парсинг + сохранение =====
@app.get("/parse")
def parse_endpoint(url: str = Query(...)):
    requests_data = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("request", lambda result: requests_data.append({
            "url": result.url, 
            "method": result.method,
            "resource_type": result.resource_type, 
            "headers": dict(result.headers)
        }))
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        browser.close()

    db = SessionLocal()
    for req in requests_data:
        db.add(NetworkRequest(**req, source_url=url))
    db.commit()
    db.close()
    return {"status": "ok", "url": url, "total": len(requests_data)}


# ===== Получение данных из БД =====
@app.get("/data")
def get_data(limit: int = Query(50), source: str = Query(None)):
    db = SessionLocal()
    query = db.query(NetworkRequest)
    if source:
        query = query.filter(NetworkRequest.source_url == source)
    results = query.order_by(NetworkRequest.created_at.desc()).limit(limit).all()
    db.close()
    return {
        "count": len(results),
        "data": [
            {   "id": result.id,
                "url": result.url,
                "method": result.method,
                "resource_type": result.resource_type,
                "source_url": result.source_url,
                "created_at": result.created_at.isoformat()
             }
        for result in results
    ]}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


# curl "http://127.0.0.1:8000/parse?url=https://market.yandex.ru"
# curl http://127.0.0.1:8000/data
# curl "http://127.0.0.1:8000/data?source=https://market.yandex.ru"
