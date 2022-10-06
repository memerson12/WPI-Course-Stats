import json
import os

f = open("final.json", "r")

finalDict = json.load(f)

f.close()


overviewDict = []
profDict = []
for course in finalDict:
    if course['instructor'] not in profDict:
        profDict.append(id, course['instructor'])
        # insert into profTable
        id = insertIntoProfTable(course['instructor'], course['ratings'])
    else:
        id = profDict.index(course['instructor'])
        # update profTable with new ratings
        updateProfTable(id, course['ratings'])

    if course['course'] not in overviewDict:
        # insert into overviewTable
        overviewDict.append(course['course'])
        insertIntoOverviewTable(course)

    # add course to courseTable
    insertIntoCourseTable(course)
