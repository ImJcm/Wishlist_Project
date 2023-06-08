from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient

client = MongoClient('mongodb+srv://wjsckdals108:ckdals108@cluster0.oxx6bv6.mongodb.net/?retryWrites=true&w=majority')
db = client.TeamProject

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html')

# @app.route('/wishlistDetail', methods=['GET','POST'])
# def wishlistDetailPage():
#     if request.method == 'POST':
#         id = request.form['id']
#         print(id)
#         return render_template('wishlistDetail.html')
#     return render_template('wishlistDetail.html')

@app.route('/item', methods=['GET'])
def getItems():
    all_list = list(db.project_1.find({},{'_id':False}))
    return jsonify({'result':all_list})

@app.route('/item', methods=['POST'])
def addItems():
    id_receive = request.form['id_give']
    title_receive = request.form['title_give']
    image_receive = request.form['image_give']
    day_receive = request.form['day_give']
    price_receive = request.form['price_give']
    reason_receive = request.form['reason_give']
    description_receive = request.form['description_give']
    password_receive = request.form['password_give']
    
    doc = {
        'id' : id_receive,
        'title' : title_receive,
        'image' : image_receive,
        'day' : day_receive,
        'price' : price_receive,
        'reason' : reason_receive,
        'description' : description_receive,
        'password' : password_receive,
        'recommandCount' : 0
    }
    
    db.project_1.insert_one(doc)
    
    return jsonify({'result': '등록 성공!'})

@app.route('/modify', methods=['PUT'])
def update():
    id_receive = request.form['id_give']
    title_receive = request.form['title_give']
    image_receive = request.form['image_give']
    day_receive = request.form['day_give']
    price_receive = request.form['price_give']
    reason_receive = request.form['reason_give']
    description_receive = request.form['description_give']
    
    db.project_1.update_one(
        {'id' : id_receive}, {"$set" : {
            'title':title_receive,
            'image':image_receive,
            'day':day_receive,
            'price':price_receive,
            'reason':reason_receive,
            'description':description_receive
            }
        }
    )
    
    return jsonify({'result': '수정 성공!'})

@app.route('/remove', methods=['DELETE'])
def delete():
    id_receive = request.form['id_give']
    
    db.project_1.delete_one(
        {'id':id_receive}
    )
    return jsonify({'result': '삭제 성공!'})
 

@app.route("/wishlistDetail", methods=["GET"])
def wishlistDetailPage():
    idx = request.args.get('id')
    #wishlist Detail info
    all_list = list(db.project_1.find({},{'_id':False}))
    
    for lt in all_list:
        if lt['id'] == idx:
            # title = list['title']
            # image = list['image']
            # day = list['day']
            # price = list['price']
            # reason = list['reason']
            # description = list['description']
            # password = list['password']
            # recommandCount = list['recommmandCount']
            return render_template('wishlistDetail.html', data=lt)

@app.route("/wishlistDetail/upRecommand",methods=['GET'])
def upRecommandCount():
    idx = request.args.get('id')
    
    upC = list(db.project_1.find({'id':idx},{'_id':False}))
    
    #print(upC[0]['recommandCount'])
    
    db.project_1.update_one({'id':idx}, 
        {"$set": {
            'recommandCount': int(upC[0]['recommandCount']) + 1
            }
        })
    
    return jsonify({'result':'추천 수 상승'})

@app.route('/wishlistDetail/addComments', methods=['POST'])
def addItemComments():
    id_receive = request.form['id_give']
    cid_receive = request.form['cid_give']
    text_receive = request.form['text_give']
    passwrod_receive = request.form['password_give']
    
    doc = {
        'id': id_receive,
        'cid': cid_receive,
        'text' : text_receive,
        'password' : passwrod_receive
    }
    
    db.project_1_comments.insert_one(doc)
    
    return jsonify({'result':'댓글 등록 성공!'})
    

@app.route('/wishlistDetail/getComments', methods=['GET'])
def getItemComments():
    id_receive = request.args.get('id')
    ct = list(db.project_1_comments.find({'id':id_receive}, {'_id':False}))
    
    return jsonify({'result':ct})

@app.route('/wishlistDetail/getCommentPwd', methods=['GET'])
def getItemCommentsPwd():
    id_receive = request.args.get('id')
    cid_receive = request.args.get('cid')
    
    ct = list(db.project_1_comments.find({'id':id_receive, 'cid':cid_receive}, {'_id':False}))
    
    return jsonify({'result':ct})

@app.route('/wishlistDetail/deleteComments',methods=['DELETE'])
def delItemComments():
    id_receive = request.args.get('id')
    cid_receive = request.args.get('cid')
    
    db.project_1_comments.delete_one(
        {'id':id_receive, 'cid':cid_receive}
    )
    return jsonify({'result': '댓글 삭제 성공!'})

@app.route('/wishlistDetail/updateComments',methods=['PUT'])
def upItemComments():
    id_receive = request.args.get('id')
    cid_receive = request.args.get('cid')
    
    text_receive = request.form['text_give']
    
    db.project_1_comments.update_one(
        {'id':id_receive, 'cid':cid_receive}, 
            {'$set': {
                'text' : text_receive
            }   
        }
    )
    
    return jsonify({'result':'댓글 수정 성공'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)