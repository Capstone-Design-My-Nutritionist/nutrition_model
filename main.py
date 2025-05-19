from fastapi import FastAPI

app = FastAPI(docs_url='/recommend/docs', openapi_url='/recommend/openapi.json')