#!/usr/bin/python

# IMPORTS
import sys
import os
import csv
import uuid
from utils import get_db, query_yes_no
from time import time


# MongoDB
db = get_db()

# DIR
main_dir = os.path.join(os.path.dirname(__file__), '..')

def store_students(filename):

	# MongoDB Drop Collection
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
	print("Inserting students in bulk")
	result = db.students.insert_many(students)
	print(result)

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


def main(args):

	print
	print("STORING")

	# EMAILS
	filename = args[0]

	tic = time()

	if query_yes_no("Store students from %s?" % (filename), "no"):
		store_students(filename)

	toc = time()

	print('%d seconds took to run' % (toc - tic))


if __name__ == "__main__":

	if len(sys.argv) > 1:
		main(sys.argv[1:])
	else:
		print('USAGE: $ python %s <filename>' % (sys.argv[0]))
		print('Example: $ python %s data/emails.csv' % (sys.argv[0]))

