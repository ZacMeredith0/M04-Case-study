from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80), nullable=False)
    publisher = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"
    
@app.route("/")
def index():
    return "Welcome to the Book API!"

@app.route("/books", methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(book_name=data['book_name'], author=data['author'], publisher=data['publisher'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book created"}), 201

@app.route("/books", methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([str(book) for book in books])

@app.route("/books/<int:id>", methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    if book:
        return jsonify(str(book))
    else:
        return jsonify({"message": "Book not found"}), 404

@app.route("/books/<int:id>", methods=['PUT'])
def update_book(id):
    data = request.get_json()
    book = Book.query.get(id)
    if book:
        book.book_name = data['book_name']
        book.author = data['author']
        book.publisher = data['publisher']
        db.session.commit()
        return jsonify({"message": "Book updated"})
    else:
        return jsonify({"message": "Book not found"}), 404

@app.route("/books/<int:id>", methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted"})
    else:
        return jsonify({"message": "Book not found"}), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)