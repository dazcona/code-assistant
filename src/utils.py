#!/usr/bin/python

import os
import sys
from pymongo import MongoClient
from time import time
from datetime import datetime


def get_db():
    """
    Set up MongoDB
    """
    db_uri = os.environ["DATABASE_URI"]
    db_name = os.environ["DATABASE_NAME"]
    username = os.environ["MONGO_INITDB_ROOT_USERNAME"]
    password = os.environ["MONGO_INITDB_ROOT_PASSWORD"]

    uri = 'mongodb://%s:%s@mongo:27017' % (username, password)
    conn = MongoClient(uri)
    return conn[db_name]


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def update_status(db, username, status):
    """ Update Status """

    result = db.students.update_one(
        { 'username': username },
        {
            '$set': { 
                'status': status,
            }
        }
    )
    # print(result)
    return result.matched_count == 1


def get_student_by_phone(db, phone):
    """ Get Student """

    return db.students.find_one(
        { 
            'phone': phone, 
            'status': { "$gt": 2 },
        },
        { 'name': 1, 'surname': 1, 'email': 1, 'username': 1, 'status': 1, 'phone': 1, 'code': 1 },
    )


def get_signups(db):
    """ Get Students that signed up """

    return db.students.find(
        { 'status': 2 }, # Code shown
        { 'name': 1, 'surname': 1, 'email': 1, 'username': 1, 'status': 1, 'phone': 1, 'code': 1 },
    )


def store_message(db, sender, recipient, text):
    """ Add text to DB """

    timestamp = datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
    result = db.messages.insert_one({
        'timestamp': timestamp,
        'sender': sender,
        'recipient': recipient,
        'message': text,
    })
    # print(result)
    return result.inserted_id


def get_prediction(db, username):
    """ Get prediction """

    return db.predictions.find_one(
        { 'student': username, 'week': 9 }, 
        { 'prediction': 1 },
    )


def get_recommendation(db, username):
    """ Get prediction """

    return db.recommendations.find_one(
        { 'student': username, 'week': 9 }, 
        { 'task': 1, 'labsheet': 1, 'resources': 1 },
    )


def get_work(db, username):
    """ Get prediction """

    return db.features.find_one(
        { 'student': username, 'week': 9 }, 
        { 'cum_programs_W9': 1, 'coverage_W9': 1 },
    )