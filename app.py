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

from flask import Flask, request, jsonify, render_template
from cassandra.cluster import Cluster

app = Flask(__name__)

cluster = Cluster(['172.18.0.2'])

session = cluster.connect()
k = "CREATE KEYSPACE IF NOT EXISTS movie_keyspace WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };"
session.execute(k)
session.set_keyspace('movie_keyspace')

@app.route('/')
def display_page():
    return render_template('homepage.html')

@app.route('/add_review', methods=['POST'])
def add_review():
    data = request.get_json()
    user_name = data['user_name']
    review_id = data['review_id']
    reviewer = data['reviewer']
    movie = data['movie']
    rating = data['rating']
    review_summary = data['review_summary']
    review_date = data['review_date']
    review_detail = data['review_detail']
    helpful = data['helpful']
    created_at = data['created_at']

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


if __name__ == '__main__':
    app.run()
