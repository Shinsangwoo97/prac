from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.gbr1o.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta
# 이거 몽고데이터베이스 본인껄로 바꿔주세요!

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/star", methods=["POST"])
def star_post():
    star_name_receive = request.form['star_name_give']
    image_url_receive = request.form['image_url_give']
    video_link_receive = request.form['video_link_give']
    comment_receive = request.form['comment_give']

    star_list = list(db.stars.find({}, {'_id': False}))
    count = len(star_list) + 1


    doc = {
        'name': star_name_receive,
        'image': image_url_receive,
        'video': video_link_receive,
        'comment': comment_receive,
        'num': count,
        'vote': 0
    }
    db.stars.insert_one(doc)

    return jsonify({'msg':'추가 완료!'})

@app.route("/star", methods=["GET"])
def star_get():
    star_list = list(db.stars.find({}, {'_id':False}))
    return jsonify({'mystars':star_list})

@app.route("/star/vote", methods=["POST"])
def vote_star():
    num_receive = request.form['num_give']

    db.stars.update_one({'num': int(num_receive)}, {'$inc': {'vote': 1}})

    return jsonify({'msg': '완료!'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)