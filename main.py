import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello from code!"}

if 'VV_DEBUG' in os.environ:
    import debugpy
    debugpy.listen(("0.0.0.0", 5678))
    print("Waiting for debugger attach")
    debugpy.wait_for_client()
    print("Debugger attached")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
