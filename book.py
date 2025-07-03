from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
import requests
from app.models.book import Book
from app import db

book_bp = Blueprint('book', __name__)

@book_bp.route('/books')
@login_required
def books():
    return render_template('book/search.html')

@book_bp.route('/books/search', methods=['GET', 'POST'])
@login_required
def search_books():
    if request.method == 'POST':
        search_query = request.form.get('search')
        sort_by = request.form.get('sort_by', 'title')
        show_date = 'show_date' in request.form
        show_rating = 'show_rating' in request.form
        
        # Google Books API
        url = f"https://www.googleapis.com/books/v1/volumes?q={search_query}&maxResults=10"
        response = requests.get(url)
        
        books = []
        if response.status_code == 200:
            data = response.json()
            
            for item in data.get('items', []):
                volume_info = item.get('volumeInfo', {})
                
                book = {
                    'id': item.get('id'),
                    'title': volume_info.get('title', 'N/A'),
                    'authors': volume_info.get('authors', ['Unknown']),
                    'publisher': volume_info.get('publisher', 'N/A'),
                    'published_date': volume_info.get('publishedDate', 'N/A') if show_date else None,
                    'rating': volume_info.get('averageRating', 'N/A') if show_rating else None,
                    'image': volume_info.get('imageLinks', {}).get('thumbnail', None)
                }
                
                books.append(book)
                
            # Sort books based on user preference
            if sort_by == 'title':
                books = sorted(books, key=lambda x: x['title'])
            elif sort_by == 'date' and show_date:
                books = sorted(books, key=lambda x: x['published_date'] if x['published_date'] else 'N/A')
            elif sort_by == 'rating' and show_rating:
                books = sorted(books, key=lambda x: x['rating'] if x['rating'] else 0, reverse=True)
                
        return render_template('book/results.html', books=books, search_query=search_query)
    
    return redirect(url_for('book.books'))

@book_bp.route('/books/save/<book_id>', methods=['POST'])
@login_required
def save_book(book_id):
    # Fetch book details from Google Books API
    url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        volume_info = data.get('volumeInfo', {})
        
        # Check if book already exists for this user
        existing_book = Book.query.filter_by(book_id=book_id, user_id=current_user.id).first()
        
        if not existing_book:
            new_book = Book(
                title=volume_info.get('title', 'Unknown'),
                author=', '.join(volume_info.get('authors', ['Unknown'])),
                published_date=volume_info.get('publishedDate', 'N/A'),
                image_url=volume_info.get('imageLinks', {}).get('thumbnail', None),
                book_id=book_id,
                rating=volume_info.get('averageRating', 0),
                user_id=current_user.id
            )
            
            db.session.add(new_book)
            db.session.commit()
            flash('Book saved to your favorites!', 'success')
        else:
            flash('This book is already in your favorites!', 'info')
    else:
        flash('Failed to save the book. Please try again later.', 'danger')
    
    return redirect(request.referrer or url_for('book.books'))

@book_bp.route('/books/remove/<int:book_id>', methods=['POST'])
@login_required
def remove_favorite(book_id):
    book = Book.query.filter_by(id=book_id, user_id=current_user.id).first()
    
    if book:
        db.session.delete(book)
        db.session.commit()
        flash('Book removed from your favorites!', 'success')
    else:
        flash('Book not found in your favorites.', 'warning')
    
    return redirect(url_for('book.favorites'))

@book_bp.route('/books/favorites')
@login_required
def favorites():
    user_books = Book.query.filter_by(user_id=current_user.id).all()
    return render_template('book/favorites.html', books=user_books) 