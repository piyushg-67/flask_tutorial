from flask import Flask, request, jsonify,json
import mysql.connector

app = Flask(__name__)
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="task_flask"
    )
    print("Connection successful")
except:
    print("some error")

cursor = db.cursor(dictionary=True)

# Home Page
@app.route('/')
def index():
    return 'This is a home page!'

# Getting all the books
@app.route('/books', methods=['GET'])
def get_books():
    cursor.execute("SELECT * FROM new_table")
    books= cursor.fetchall()
    if len(books)>0:
        return jsonify(books)
    else:
        return "No data Found"

# Get details of single book by id 
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    cursor.execute("SELECT * FROM new_table WHERE id=%s", (id,))
    book=cursor.fetchone()
    if book:
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"})
    

# Create a book
@app.route('/books', methods= ['POST'])
def create_book():
    data = request.json
    author = data.get('author')
    title = data.get('title')
    cursor.execute("INSERT INTO new_table(author, title) VALUES (%s, %s)", (author, title))
    db.commit()
    book_id=cursor.lastrowid
    cursor.execute("SELECT * FROM new_table WHERE id= %s", (book_id,))
    new_book=cursor.fetchone()
    return jsonify(new_book),201

# Update a book
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data=request.json
    author=data.get('author')
    title=data.get('title')

    cursor.execute('UPDATE new_table SET author= %s, title= %s WHERE id=%s', (author,title,id))
    db.commit()

    cursor.execute("SELECT * FROM new_table WHERE id=%s", (id,))
    updated_book= cursor.fetchone()
    return jsonify(updated_book),200

# Delete a book
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    cursor.execute("SELECT * FROM new_table WHERE id=%s", (id,))
    book = cursor.fetchone()
    if not book:
        return jsonify({"error": "Book not found"}), 404
    
    cursor.execute("DELETE FROM new_table WHERE id=%s", (id,))
    db.commit()

    return jsonify({"message": "Book deleted successfully"}), 200



# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)