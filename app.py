from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

BOOK_INFO_URL = "http://book-api-server-avd123.hue0hefkamekfha3.uksouth.azurecontainer.io:5000/books"

# Function to filter books by criteria <author, genre, id, publication,title>
def filter_books(books, criteria):
    filtered_books = []
    for book in books:
        match = True
        for key, value in criteria.items():
            if str(book.get(key, '')).lower() != value.lower():
                match = False
                break
        if match:
            filtered_books.append(book)
    return filtered_books

# Render search page

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to return book information filtered by specified criteria
@app.route('/books', methods=['GET'])
def get_books_by_criteria():
    # Initialise query parameters
    genre = request.args.get('genre', '')
    author = request.args.get('author', '')
    book_id = request.args.get('id', '')
    publication_year = request.args.get('publication_year')
    title = request.args.get('title', '')

    # Build dictionary of book classifiers
    criteria = {k: v for k, v in [('genre', genre), ('author', author), ('id', book_id), ('publication_year', publication_year),('title', title)] if v}

    # Try to request all book data and filter according to criteria args
    try:
        response = requests.get(BOOK_INFO_URL)
        # Successfully downloaded list
        if response.status_code == 200:
            all_books = response.json()
            filtered_books = filter_books(all_books, criteria)
            return jsonify(filtered_books)
        # Could not access book data
        else:
            return jsonify({'error': 'Failed to retrieve books'}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
