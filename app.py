from dotenv import load_dotenv
import os
import json
from datetime import datetime
import uuid
from flask import Flask, request, jsonify, render_template
from cassandra.cluster import Cluster
from cassandra.policies import RetryPolicy
from cassandra.query import SimpleStatement
import binascii
from models import reviews as rr
load_dotenv()
global IP
IP = os.getenv('IP_ADDRESS')
global KEYSPACE
KEYSPACE = "movie_keyspace"

from models import sync_tabless


app = Flask(__name__)


cluster = Cluster([IP])

session = cluster.connect()
session.default_timeout = 60
k = "CREATE KEYSPACE IF NOT EXISTS movie_keyspace WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3 };"
session.execute(k)
session.set_keyspace(KEYSPACE)


@app.route('/')
def display_page():

    return render_template('home.html')
@app.route('/display_result', methods=['POST'])
def display_result():
    retry_policy = RetryPolicy()
    page_size = 8
    # page_state = request.form.get('page_state', default=None)
    # print(page_state)
    #
    # x = json.loads(page_state)
    # page_state=x['next_page_state']
    # print(page_state)
    # if(page_state==''):
    #     page_state=None
    movie_name = request.form.get('search_value')
    query = "SELECT review_id, reviewer, rating, movie, review_summary FROM reviews WHERE  movie LIKE  '%{}%' LIMIT 8; ".format(movie_name)

    # stmt = SimpleStatement(
    #     query,
    #     fetch_size=page_size,
    #     retry_policy=retry_policy
    # )
    # result_set = session.execute(stmt,paging_state=page_state)
    # items = result_set.current_rows
    #
    # next_page_state = result_set.paging_state
    items = session.execute(query)
    reviews = []

    for row in items:
        reviews.append({
            "review_id": row.review_id,
            "reviewer": row.reviewer,
            "movie": row.movie,
            "rating": row.rating,
            "review_summary": row.review_summary
        }
        )

    # if next_page_state== None:
    #     next_page_state=''
    # ns =jsonify( {"next_page_state": next_page_state })

    review = [reviews,movie_name,None]
    return render_template('reviewblock.html', data=review)


@app.route('/get_review', methods=['POST'])
def get_review():
    reviewid = request.form.get('reviewid')

    query = "SELECT * FROM movie_keyspace.reviews WHERE  review_id='{}' ;".format(reviewid)
    result = session.execute(query)

    reviews = []
    for row in result:
        reviews.append({
            "review_id": row.review_id,
            "reviewer": row.reviewer,
            "movie": row.movie,
            "rating": row.rating,
            "review_summary": row.review_summary,
            "review_date": row.review_date,
            "spoiler_tag": row.spoiler_tag,
            "review_detail": row.review_detail,
            "helpful": row.helpful,

        }
        )

    return render_template('movie_detailed.html', data=reviews)


@app.route('/add_review', methods=['POST'])
def add_review():
    d1 = dict(request.form)
    data = d1['review']
    data = json.loads(data)

    review_id = str(uuid.uuid4())
    reviewer = data['reviewer']
    movie = data['movie']
    rating = int(data['rating'])
    review_summary = data['review_summary']
    review_date = str(datetime.now())
    spoiler_tag = data['spoiler_tag']
    review_detail = data['review_detail']
    helpful = data['helpful']


    query = "INSERT INTO reviews (review_id,reviewer,movie,rating,review_summary,review_date,spoiler_tag,review_detail,helpful) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s)"
    session.execute(query, (
        review_id, reviewer, movie, rating, review_summary, review_date, spoiler_tag, review_detail, helpful))

    return jsonify({'message': 'Review added successfully'})




@app.route('/delete_review', methods=['DELETE'])
def delete_review():
    data = request.get_json()
    movie_name = data['movie_name']
    user_name = data['reviewer']

    query = "DELETE FROM reviews WHERE movie=%s AND reviewer=%s"
    session.execute(query, (movie_name, user_name))

    return jsonify({'message': 'Review deleted successfully'})


@app.route('/edit_review', methods=['POST'])
def edit_review():
    data = request.get_json()
    movie_name = data['movie']
    user_name = data['reviewer']
    review = data['review']

    query = "UPDATE reviews SET review=%s WHERE movie=%s AND reviewer=%s"
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