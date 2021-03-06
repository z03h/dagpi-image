import os

import uvicorn

host = os.getenv("HOST", "127.0.0.1")
port = os.getenv("PORT", 5000)

if __name__ == "__main__":
    print("Ready to run app")
    uvicorn.run("app:app", host=host, port=port, log_level="info")
