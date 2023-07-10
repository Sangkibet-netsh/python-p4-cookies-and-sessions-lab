#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    # Retrieve all articles (replace this with your own logic)
    articles = Article.query.all()
    
    # Create a list of dictionaries representing each article
    article_data = []
    for article in articles:
        article_data.append({
            'id': article.id,
            'title': article.title,
            'content': article.content,
            # Add more attributes as needed
        })
    
    # Render a JSON response with the article data
    return jsonify(article_data)


@app.route('/articles/<int:id>')
def show_article(id):
    session.setdefault('page_views', 0)  # Set initial value of page_views to 0 if it doesn't exist
    
    session['page_views'] += 1  # Increment page_views for every request
    
    if session['page_views'] <= 3:
        # Retrieve the article data (replace this with your own logic)
        article = Article.query.get(id)
        
        if article:
            # Create a dictionary representation of the article
            article_data = {
                'id': article.id,
                'title': article.title,
                'content': article.content,
                # Add more attributes as needed
            }
            
            # Render a JSON response with the article data
            return jsonify(article_data)
        else:
            # Handle the case when the article is not found
            return jsonify({'message': 'Article not found'}), 404
    else:
        # Return an error message and status code 401 unauthorized
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

if __name__ == '__main__':
    app.run(port=5555)
