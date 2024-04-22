import uvicorn

from app import init_app

server = init_app()

if __name__ == "__main__":
    uvicorn.run(server, host="0.0.0.0", port=8080)