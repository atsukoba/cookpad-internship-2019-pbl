import io
import json
import logging
import cv2
import requests
from matplotlib import pyplot as plt

logger = logging.getLogger(__name__)

with open("config.json", "r") as cf:
    conf = json.load(cf)

CLIENT_ID = conf["kuimono"]["uid"]
CLIENT_SECRET = conf["kuimono"]["secret key"]
USER_ID = conf["id"]


def get_recipe_data_by_id(_id: int) -> dict:
    """
    responce = {
        "id" : hoge,
        "title" : hoge,
        "media" : hoge
    }
    """
    res = requests.get(url.format(_id),
        auth=(CLIENT_ID, CLIENT_SECRET),
        headers={"content-type": "application/json",
            "Resource-Owner-Id" : USER_ID})

    if not res.ok:
        print(f"responce not ok: {res}")
        return demo_data
    
    if len(res.json()) == 0 or conf["demo"] == "true":
        print(f"responce json length is 0: {res.json()}")
        # demo data
        return demo_data

    return res.json()[0]


def get_recipes_data_by_ids(ids: list) -> list:
    if ids == []: return
    ids = list(map(str, ids))
    res = requests.get(url.format(",".join(ids)),
        auth=(CLIENT_ID, CLIENT_SECRET),
        headers={
            "content-type": "application/json",
            "Resource-Owner-Id" : USER_ID})

    if not res.ok:
        print(f"responce not ok")
        return {}

    return res.json()
