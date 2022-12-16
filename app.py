# import uuid
# from flask import Flask
# from flask_cqlalchemy import CQLAlchemy
# from  model import Review
# app = Flask(__name__)
# app.config['CASSANDRA_HOSTS'] = ['172.18.0.2']
# app.config['CASSANDRA_KEYSPACE'] = "cqlengine"
# db = CQLAlchemy(app)
#
#
#
# # @app.route('/')
# # def hello_world():  # put application's code here
# #     return 'Hello World!'
#
#
# # if __name__ == '__main__':
# #     app.run()
import json
from datetime import datetime
import uuid
from flask import Flask, request, jsonify, render_template
from cassandra.cluster import Cluster

global IP
IP = '52.188.66.157'
global KEYSPACE
KEYSPACE = "movie_keyspace"

from models import sync_tabless


app = Flask(__name__)


cluster = Cluster([IP])

session = cluster.connect()
k = "CREATE KEYSPACE IF NOT EXISTS movie_keyspace WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };"
session.execute(k)
session.set_keyspace(KEYSPACE)


@app.route('/')
def display_page():
    query = "SELECT * FROM reviews"
    result = session.execute(query)

    reviews = []
    for row in result:
        reviews.append({
            "user_name": row.user_name,
            "review_id": row.review_id,
            "reviewer": row.reviewer,
            "movie": row.movie,
            "rating": row.rating,
            "review_summary": row.review_summary,
            "review_date": row.review_date,
            "review_detail": row.review_detail,
            "helpful": row.helpful,
            "created_at": row.created_at
        }
        )
    return render_template('homepage.html', data=reviews)


@app.route('/add_review', methods=['POST'])
def add_review():
    d1 = dict(request.form)
    data = d1['review']
    data = json.loads(data)

    user_name = data['user_name']
    review_id = uuid.uuid4()
    reviewer = data['reviewer']
    movie = data['movie']
    rating = int(data['rating'])
    review_summary = data['review_summary']
    review_date = datetime.now()
    review_detail = data['review_detail']
    helpful = data['helpful']
    created_at = datetime.now()

    query = "INSERT INTO reviews (user_name,review_id,reviewer,movie,rating,review_summary,review_date,review_detail,helpful,created_at) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)"
    session.execute(query, (
        user_name, review_id, reviewer, movie, rating, review_summary, review_date, review_detail, helpful, created_at))

    return jsonify({'message': 'Review added successfully'})


@app.route('/search_review', methods=['GET'])
def search_review():
    movie_name = request.args.get('movie_name')

    query = "SELECT * FROM reviews WHERE movie_name=%s"
    result = session.execute(query, (movie_name,))

    reviews = []
    for row in result:
        reviews.append({
            "user_name": row.user_name,
            "review_id": row.review_id,
            "reviewer": row.reviewer,
            "movie": row.movie,
            "rating": row.rating,
            "review_summary": row.review_summary,
            "review_date": row.review_date,
            "review_detail": row.review_detail,
            "helpful": row.helpful,
            "created_at": row.created_at
        }
        )

    return jsonify({'reviews': reviews})


@app.route('/delete_review', methods=['DELETE'])
def delete_review():
    data = request.get_json()
    movie_name = data['movie_name']
    user_name = data['user_name']

    query = "DELETE FROM reviews WHERE movie_name=%s AND user_name=%s"
    session.execute(query, (movie_name, user_name))

    return jsonify({'message': 'Review deleted successfully'})


@app.route('/edit_review', methods=['POST'])
def edit_review():
    data = request.get_json()
    movie_name = data['movie_name']
    user_name = data['user_name']
    review = data['review']

    query = "UPDATE reviews SET review=%s WHERE movie_name=%s AND user_name=%s"
    session.execute(query, (review, movie_name, user_name))

    return jsonify({'message': 'Review updated successfully'})


@app.route('/sr')
def abc():
    sync_tabless()
    return "Synced with DB"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="8080")

# 
# /app
#     - app_runner.py
#     /services
#         - app.py 
#     /templates
#         - mainpage.html
#     /static
#         /styles
#             - mainpage.css