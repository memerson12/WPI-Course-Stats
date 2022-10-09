# Write a fucntion to merge data from the data folder and the output.json file into one
import json
import os

f = open("output.json", "r")
listings = json.load(f)
f.close()

finalDict = []
for file in os.listdir("data"):
    if file.endswith(".json"):
        with open("data/" + file, "r") as f:
            data = json.load(f)
            for course in data:
                # find the course number
                num = course['courseInfo']['courseNumber']
                # find the course name
                title = course['courseInfo']['courseTitle']
                # find a match in the listings

                ratingsJSON = {
                    'overallRatings': course['overallRatings'],
                    'relativeRating': course['relativeRating'],
                    'frequentlyTrue': course['frequentlyTrue'],
                    'misc': course['misc']}
                # add overallRatings, relativeRating, frequentlyTrue, misc to ratingsJSON

                # add oscar's data to the finalDict
                course_data = {
                    "title": title,
                    "term": course["courseInfo"]['term'].split('_')[1],
                    "number": num,
                    "year": file.split("_")[2].replace('.json', ''),
                    "instructor": course['courseInfo']['instructor'],
                    "subjectAbrev": course['courseInfo']['courseNumber'].split(' ')[0],
                    "subject": "",
                    "description": "",
                    "format": course['courseInfo']['courseType'],
                    "level": "",
                    "ratings": ratingsJSON,
                }
                if num in listings:
                    course_data.update({
                        "subject": listings[num]['subject'],
                        "description": listings[num]['description'],
                        "level": listings[num]['academic_level'],
                        "title": listings[num]['name'],
                    })
                finalDict.append(course_data)
with open("final.json", "w") as f:
    json.dump(finalDict, f, indent=4)
