import os
import sqlite3
import json
from itertools import chain


# for like function

def initialize():
    conn = sqlite3.connect('data/likes.sqlite3')
    c = conn.cursor()
    c.execute('drop table likes')
    c.execute('create table likes(userid text, recipeid integer)')
    conn.commit()
    conn.close()
    return


def like(userid, recipeid):
    conn = sqlite3.connect('data/likes.sqlite3')
    c = conn.cursor()
    c.execute(f"insert into likes values ('{userid}', {recipeid})")
    conn.commit()
    conn.close()
    return


def rmlike(userid, recipeid):
    conn = sqlite3.connect('data/likes.sqlite3')
    c = conn.cursor()
    c.execute(f"delete from likes where userid = '{userid}' and recipeid = {recipeid}")
    conn.commit()
    conn.close()
    return


def getlikes(userid) -> list:
    # select id, name from user;
    conn = sqlite3.connect('data/likes.sqlite3')
    c = conn.cursor()
    print("db get likes...")
    c.execute(f"select recipeid from likes where userid = '{userid}'")
    data = list(chain.from_iterable(c.fetchall()))
    print(data)
    if type(data) != list: return [data]
    return data


if __name__ == "__main__":
    initialize()
