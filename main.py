from fastapi import FastAPI, Request, Response

app = FastAPI()


@app.get("/")
def read_root(request: Request, response: Response):
    return {"Hello": "World"}
