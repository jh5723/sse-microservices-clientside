from flask import Flask, jsonify, request, render_template
import requests
import os

app = Flask(__name__)

BOOK_KEY = os.getenv("BOOK_INFO_URL")

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
    # Build query parameters from request args
    query_params = request.args.to_dict()
    print("Query Parameters:", query_params)

    try:
        if not query_params:
            response = requests.get(BOOK_KEY)
        else:
            # Forward the query parameters to the first service
            response = requests.get(BOOK_KEY, params=query_params)

        if response.status_code == 200:
            response_data = response.json()
            print("Response Data:", response_data)
            return render_template('results.html', results=response_data)
        else:
            return jsonify({'error': 'Failed to retrieve books'}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
