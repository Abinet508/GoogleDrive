from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from fastapi import FastAPI
from pydantic import BaseModel


from flask import request, jsonify


gAuth=GoogleAuth()
drive=GoogleDrive(gAuth)
file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format('14o8-_gFd1Cslyd1voBojxfctDi9LJEn3')}).GetList()
app = FastAPI()


async  def GetallBooks():
    books = []
    for file in file_list:
        books.append(file)
    return books
async def GetTitle(file_id):
    for file in file_list:
        if file['id'] == file_id:
            return file['title']
    return None
async def GetEmbedlink(file_id):
    for file in file_list:
        if file['id'] == file_id:
            return file['embedLink']
    return None    

@app.get('/')
async def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of fiction novels.</p>'''


@app.get('/api/v1/resources/books/all', response_model=BaseModel)
async def api_all():
    return jsonify(GetallBooks())


@app.get('/api/v1/resources/books')
async def GetBook():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for book in GetallBooks():
        if book['id'] == id:
            results.append(book)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

  