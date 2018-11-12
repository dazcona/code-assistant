#!/usr/bin/python

# IMPORTS
import sys
import os
import csv
import json
import uuid
from utils import get_db, query_yes_no
from time import time


# MongoDB
db = get_db()

# DIR
main_dir = os.path.join(os.path.dirname(__file__), '..')

def store_students(filename):

	print('Storing students:')

	# MongoDB Drop Collection
	if query_yes_no("Drop the students collection?", "no"):
		db.students.drop()

	with open(os.path.join(main_dir, filename)) as f:
		reader = csv.DictReader(f)
		students = [ 
			{ 
				'name': row['Name'], 
				'surname': row['Surname'], 
				'email': row['Email'],
				'username': row['Username'],
				'token': str(uuid.uuid4()),
				'status': 0, # Status: "Created"
			} for row in reader ]

	# MongoDB Insert in Bulk
	# print("Inserting students in bulk")
	# result = db.students.insert_many(students)
	# print(result)

	# MongoDB Insert one by one
	for student in students:
		candidate = db.students.find(
			{ 'username': student['username'] },
			{ 'username': 1 },
		)
		if len(candidate) > 0:
			print('Student %s is already in the database' % (student['username']))
		else:
			print('Inserting %s in the database' % (student['username']))
			result = db.students.insert_one(student)
			print('Inserted: %s' % (result.inserted_id))

	# How many students?
	# $ mongo
	# > show databases
	# > use coding_bot
	# > show tables
	# students
	# > db.students.find().count()
	# ...
	# > db.students.distinct("name").length
	# ...
	# > db.students.find()
	# ...
	# > db.students.findOne()
	# ...


def store_predictions(filename):

	print('Storing predictions:')

	if query_yes_no("Drop the predictions collection?", "no"):
		db.predictions.drop()

	with open(filename) as f:
    	predictions = json.load(f)

	print("Inserting predictions in bulk")
	result = db.predictions.insert_many(predictions)
	print(result)

		
def store_recommendations(filename):

	print('Storing recommendations:')

	if query_yes_no("Drop the recommendations collection?", "no"):
		db.recommendations.drop()

	with open(filename) as f:
    	recommendations = json.load(f)

	print("Inserting recommendations in bulk")
	result = db.recommendations.insert_many(recommendations)
	print(result)


def store_features(filename):

	print('Storing features:')

	if query_yes_no("Drop the features collection?", "no"):
		db.features.drop()

	with open(filename) as f:
    	features = json.load(f)

	print("Inserting features in bulk")
	result = db.features.insert_many(features)
	print(result)


def main(args):

	tic = time()

	filename = args[0]

	if filename.startswith('emails'):

		store_students(filename)

	elif filename.startswith('predictions'):

		store_predictions(filename)

	elif filename.startswith('recommendations'):

		store_recommendations(filename)

	elif filename.startswith('features'):

		store_features(filename)


	else:

		print('File format not found')
		exit(2)

	toc = time()

	print('%d seconds took to run' % (toc - tic))


if __name__ == "__main__":

	if len(sys.argv) > 1:
		main(sys.argv[1:])
	else:
		print('USAGE: $ python %s <filename>' % (sys.argv[0]))
		print('Example: $ python %s data/emails.csv' % (sys.argv[0]))
		exit(1)

