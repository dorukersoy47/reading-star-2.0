
uvicorn sample:app --host 127.0.0.1 --port 8000

'sample': the name of the file
'app': the name of the FastAPI instance

to test the backend is working you can use Postman to send requests

main.py registers routers
api/... creates routers and handles paths, calls services methods and uses models
models/... holds pydantic classes (like DTOs)
services/... is where the business logic is


frontend needs:
create instrumental (POST) (/instrumentals)
create lyrics within instrumental (POST) (/instrumentals/{id}/lyrics)
get all songs (GET) (/instrumentals)
get instrumental (GET) (/instrumentals/{id})
get lyrics (GET) (/instrumentals/{id}/lyrics/{id})

eventually:
edit instrumental (volume levels)? (PUT)
delete instrumental (DELETE)
delete lyrics within instrumental (DELETE)


get all tracks (instrumentals + their lyrics), multiple requests?

Pydantic automatically handles JSON parsing