import logging
import asyncio
import aiohttp
import threading
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
import uvicorn
from logging.handlers import RotatingFileHandler
from typing import List

# Configure logging with rotating files
log_handler = RotatingFileHandler("app.log", maxBytes=10240, backupCount=5)
log_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)
logging.getLogger().addHandler(log_handler)

# List of URLs to hit periodically
URLS = [
    "https://baseboilerflaskadvanceapi.onrender.com",
    "https://sotrueplay.onrender.com"
]

app = FastAPI()
log_messages: List[str] = []  # List to store log messages

# Asynchronous function to hit URLs
async def hit_urls():
    async with aiohttp.ClientSession() as session:
        while True:
            for url in URLS:
                try:
                    async with session.get(url) as response:
                        log_msg = f"Successfully hit URL: {url}, Status Code: {response.status}"
                        if response.status != 200:
                            log_msg = f"Failed to hit URL: {url}, Status Code: {response.status}"
                        logging.info(log_msg)
                        log_messages.append(log_msg)
                except aiohttp.ClientError as e:
                    log_msg = f"Error occurred while hitting {url}: {e}"
                    logging.error(log_msg)
                    log_messages.append(log_msg)
            await asyncio.sleep(60)

# FastAPI route to stream logs using Server-Sent Events (SSE)
@app.get("/stream")
async def stream_logs():
    async def event_generator():
        while True:
            if log_messages:
                log_msg = log_messages.pop(0)
                yield f"data: {log_msg}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# Simple HTML interface to display logs
@app.get("/", response_class=HTMLResponse)
async def get_html():
    html_content = """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Live Logs</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                color: #333;
                padding: 20px;
            }
            h1 {
                color: #444;
            }
            #log-container {
                max-height: 400px;
                overflow-y: scroll;
                background-color: #fff;
                padding: 10px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .log-entry {
                margin: 5px 0;
                padding: 5px;
                background: #e8e8e8;
                border-left: 3px solid #444;
            }
        </style>
    </head>
    <body>
        <h1>Live Logs</h1>
        <div id="log-container"></div>
        <script>
            const eventSource = new EventSource("/stream");
            eventSource.onmessage = function(event) {
                const logContainer = document.getElementById("log-container");
                const newLog = document.createElement("div");
                newLog.className = "log-entry";
                newLog.textContent = event.data;
                logContainer.appendChild(newLog);
                logContainer.scrollTop = logContainer.scrollHeight;  // Auto-scroll to latest log
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

def start_async_loop():
    asyncio.run(hit_urls())

if __name__ == "__main__":
    # Start the async URL hitter in a separate thread
    threading.Thread(target=start_async_loop, daemon=True).start()

    # Run the FastAPI app using uvicorn for production
    uvicorn.run(app, host='0.0.0.0', port=5000, log_level="info")
