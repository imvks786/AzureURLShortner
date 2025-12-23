from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
import uuid
from datetime import datetime

app = FastAPI(title="URL Analytics Platform")

# TEMP storage (we'll replace with Azure SQL)
url_store = {}

@app.get("/")
def root():
    return {"message": "URL Analytics Backend is running"}

# Create Short URL
@app.post("/shorten")
def create_short_url(original_url: str):
    short_id = str(uuid.uuid4())[:6]
    url_store[short_id] = {
        "original_url": original_url,
        "created_at": datetime.utcnow()
    }

    return {
        "short_url": f"http://localhost:8000/{short_id}"
    }

# Redirect + Track Click
@app.get("/{short_id}")
async def redirect_url(short_id: str, request: Request):
    if short_id not in url_store:
        raise HTTPException(status_code=404, detail="URL not found")

    click_data = {
        "short_id": short_id,
        "timestamp": datetime.utcnow().isoformat(),
        "ip": request.client.host,
        "user_agent": request.headers.get("user-agent")
    }

    # For now, just print (later → ADLS)
    print("CLICK EVENT:", click_data)

    original_url = url_store[short_id]["original_url"]
    return RedirectResponse(original_url)
