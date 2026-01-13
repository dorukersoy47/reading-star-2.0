
uvicorn sample:app --host 127.0.0.1 --port 8000

'sample': the name of the file
'app': the name of the FastAPI instance

to test the backend is working you can use Postman to send requests

main.py registers routers
api.py creates routers and handles paths, calls services methods and uses models
models/... holds pydantic classes (like DTOs)
services/... is where the business logic is

Pydantic automatically handles JSON parsing