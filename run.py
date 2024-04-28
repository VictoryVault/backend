import uvicorn
import os
from app.main import init_app


server = init_app()

if 'VV_DEBUG' in os.environ:
    import debugpy
    debugpy.listen(("0.0.0.0", 5678))
    print("Waiting for debugger attach")
    debugpy.wait_for_client()
    print("Debugger attached")

if __name__ == "__main__":
    uvicorn.run(server, host="0.0.0.0", port=80)