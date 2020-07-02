""" main module to run server """
import uvicorn

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", reload=True)
