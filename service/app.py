import json
import logging
import os
from colormap import rgb2hex
from flask import Flask, abort, jsonify, render_template, request
from service import image, kuimono, db

app = Flask(__name__)
logger = logging.getLogger()


@app.route('/start', methods=['POST', 'GET'])
def start():
    if request.method == 'POST':
        html = render_template('index.html', data={})
    html = render_template('start.html', data={})
    return html


@app.route('/', methods=['POST', 'GET'])
def root():
    if request.method == 'POST':
        html = render_template('index.html', data={})
    html = render_template('index.html', data={})
    return html


@app.route('/search', methods=['GET'])
def search():
    """
    ex: /search?color=e520f2&n=20
    """
    code = request.args.get('color', "FF0000", type=str).strip()

    n = request.args.get('n', 90, type=int)
    print(f"query Code is {code}")

    img_urls = image.search_by_hex(code, image.represent_colors, n_result=n)
    ids = [int(u.split(os.path.sep)[4]) for u in img_urls]

    recipes = [{"id" : _id, "url" : url} for _id, url in zip(ids, img_urls)]
    print(f"recipes data: {len(recipes)}")

    data = {
        "color" : code,
        "recipes" : recipes
    }
    return render_template('results.html', data=data)


@app.route('/search/photo', methods=['GET'])
def get_photo():
    data = {}
    return render_template('photo.html', data=data)


@app.route('/search/photo', methods=['POST'])
def search_photo():
    data = request.files['camera'].read()
    print("posted binary data")
    mat = image.binary_to_array(data)
    print(f"Extracting color feature from data")
    print("image matrix shape", mat.shape)
    rgb = image.get_rgb_kmeans(mat, K=3)
    print(f"Extracterd RGB is {rgb}")
    code = rgb2hex(*rgb).replace("#", "")
    print(f"Searching...")
    searched_urls = image.search(rgb, image.represent_colors)
    ids = [int(u.split(os.path.sep)[4]) for u in searched_urls]
    recipes = [{"id" : _id, "url" : url} for _id, url in zip(ids, searched_urls)]

    print(f"recipes data: {len(recipes)}")

    data = {
        "color" : code,
        "recipes" : recipes
    }
    return render_template('results.html', data=data)


@app.route("/recipes", methods=['GET'])
def recipes():
    _id = request.args.get('id', 30, type=int)
    user_id = request.args.get('user_id', "atsuyakoba", type=str)
    data = kuimono.get_recipe_data_by_id(_id)
    data["status"] = "liked" if _id in db.getlikes(user_id) else "nonliked"

    return render_template('recipe.html', data=data)


@app.route("/likes", methods=['GET'])
def likes():
    # hard coded username!!! (for demo)
    user_id = request.args.get('user_id', "atsuyakoba", type=str)
    ids = db.getlikes(user_id)
    if len(ids) == 0:
        print(f"No liked recipes!")
        return render_template('likes.html', data={"recipes" : ""})

    data = kuimono.get_recipes_data_by_ids(ids)
    print(f"Liked recipes: {len(data)}")
    print(data)
    return render_template('likes.html', data=data)


@app.route("/likes/do", methods=['GET'])
def toglelikes() -> str:
    userid = request.args.get('userid')
    recipeid = int(request.args.get('recipeid'))
    print("/likes/do param data:")
    print(f"/likes/do userid : {userid}")
    print(f"/likes/do recipeid : {recipeid}")

    if recipeid is None: print("data is none")

    res = {
        "userid" : userid,
        "recipeid" : recipeid}

    likes = db.getlikes(userid)
    print(f"{recipeid}: {type(recipeid)} in {likes}: {type(likes[0])}")

    if recipeid in likes:
        print(f"Like removed: {recipeid}")
        db.rmlike(userid, recipeid)
        res["status"] = "removed"
    else:
        print(f"Liked: {recipeid}")
        db.like(userid, recipeid)
        res["status"] = "liked"

    print(f"Response: {res}")

    return jsonify(res)


@app.route('/image/color', methods=['GET'])
def extract_color():
    img_url = request.args.get('img_url')
    colors = image.get_rgb_kmeans_by_url(img_url)
    print(f"got colors from image: {colors}")
    res = {
        "colors" : colors
    }
    return jsonify(res)

if __name__ == "__main__":
    app.run()
