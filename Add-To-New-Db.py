import json
import os
import mysql.connector

from dotenv import load_dotenv

f = open("final.json", "r")

finalDict = json.load(f)

f.close()

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv('PS_HOST'),
    user=os.getenv('PS_USERNAME'),
    password=os.getenv('PS_PASSWORD'),
)
cursor = mydb.cursor()

overviewDict = {}
profDict = {}
for course in finalDict:
    print('Inserting', course['title'])
    if course['instructor'] not in profDict:
        names = course['instructor'].split(',')
        statement = "INSERT professors (first_name, last_name) VALUES (%s, %s)"
        values = (names[1], names[0])
        cursor.execute(statement, values)
        profDict[course['instructor']] = cursor.lastrowid

    if course['number'] not in overviewDict or 'HU 3900' == course['number'] or course['number'] == 'HU 3910':
        statement = """INSERT course_overviews 
                              (course_title, course_number, course_type, subject, subject_abbreviation, description, level) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (course['title'], course['number'], course['format'], course['subject'], course['subjectAbrev'],
                  course['description'],
                  course['level'])
        cursor.execute(statement, values)
        overviewDict[course['number']] = cursor.lastrowid

    statement = "INSERT courses (professor_id, overview_id, term, year, course_report_data) VALUES (%s, %s, %s , %s, %s)"
    values = (profDict[course['instructor']], overviewDict[course['number']], course['term'], course['year'],
              json.dumps(course['ratings']))
    cursor.execute(statement, values)
mydb.commit()
