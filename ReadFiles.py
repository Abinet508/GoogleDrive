from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import flask
from flask import request, jsonify


gAuth=GoogleAuth()
drive=GoogleDrive(gAuth)
file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format('14o8-_gFd1Cslyd1voBojxfctDi9LJEn3')}).GetList()

app = flask.Flask(__name__)

app.config["DEBUG"] = True
def GetallBooks():
    books = []
    temp=""
    for file in file_list:
        dictbooks = {}
        dictbooks['id'] = file['id']
       
        temp = file['originalFilename']
        temp=temp.replace("_@ETHIO_PDF_BOOKS","")
        temp=temp.replace("_@Ethio_Books","")
        temp=temp.replace("_etbookstore_6","")
        temp=temp.replace("_@BOOKALEM","")
        temp=temp.replace("_@OLDBOOKSPDF","")
        temp=temp.replace('_.pdf','').strip()
        temp=temp.replace("@ETHIO_PDF_BOOKS_pdf","")
        temp=temp.replace("@Ethio_Books","")
        temp=temp.replace("@BOOKALEM","")
        temp=temp.replace("@ETHIO_PDF_BOOKS","")
        temp=temp.replace("@OLDBOOKSPDF","")
        temp=temp.replace('.pdf','').strip()
        dictbooks['title'] = temp.strip()
        print(dictbooks['title'])
             #dictbooks['title'] = file['originalFilename'].replace('.pdf','').strip()
            
        dictbooks['link'] = file['embedLink']
        dictbooks['alternateLink'] = file['alternateLink']

        books.append(dictbooks)
    return books
def GetTitle(file_id):
    for file in file_list:
        if file['id'] == file_id:
            return file['originalFilename'].replace('.pdf','').strip()
    return None
def GetEmbedlink(file_id):
    for file in file_list:
        if file['id'] == file_id:
            return file['embedLink']
    return None    

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of fiction novels.</p>'''

@app.route('/all', methods=['GET'])
def Read_all():
    return jsonify(GetallBooks())


@app.route('/<id>', methods=['GET'])
def GetBook(id):
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    GetTitle(id)
    try:
       
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
    except:
         return "Error: No id field provided. Please specify an id."
   

if __name__ == '__main__':
     # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000) 