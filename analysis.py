import json
import csv

file = open('ratings_with_subject.json', 'r')
ratings: dict = json.load(file)
file.close()

ratings_by_type = {}
ratings_by_department_and_type = {}
teacher_ratings = {}
teacher_number_of_ratings = {}
ratings_by_subject = {}

departments = [*ratings]
for department in departments:
    course_types = [*ratings[department]]
    print(department)
    ratings_by_department_and_type[department] = {}
    for course_type in course_types:
        num_courses = 0
        total_ratings = 0
        for course in ratings[department][course_type]:
            if course['overallRatings']['overallQuality']['average'] == '':
                continue
            total_ratings += float(course['overallRatings']['overallQuality']['average'])
            num_courses += 1
            instructor = course['courseInfo']['instructor']
            subject = course['courseInfo']['subject']
            course_rating = float(course['overallRatings']['overallQuality']['average'])
            teacher_number_of_ratings[instructor] = teacher_number_of_ratings.get(instructor, 1) + 1
            teacher_ratings[instructor] = (teacher_ratings.get(instructor, course_rating) + course_rating) / 2
            ratings_by_subject[subject] = (ratings_by_subject.get(subject, course_rating) + course_rating) / 2
        average = total_ratings / num_courses
        ratings_by_type[course_type] = (ratings_by_type.get(course_type, average) + average) / 2
        ratings_by_department_and_type[department][course_type] = (ratings_by_department_and_type[department].get(
            course_type, average) + average) / 2
        print(f'{course_type}s: {round(total_ratings / num_courses, 2)}/5 average rating')
    print('\n---------------------------\n')

print(ratings_by_subject)
with open('./results/Ratings_by_Course_Type.csv', 'w') as csv_file:
    types_list = list(ratings_by_type.keys())
    writer = csv.DictWriter(csv_file, fieldnames=types_list)
    writer.writeheader()
    writer.writerow(ratings_by_type)

with open('./results/Ratings_by_Department.csv', 'w') as csv_file:
    departments_list = [*ratings_by_department_and_type]
    values_list = [sum(list(x.values())) / len(x.values()) for x in ratings_by_department_and_type.values()]
    writer = csv.writer(csv_file)
    writer.writerow(departments_list)
    writer.writerow(values_list)

with open('./results/Ratings_by_Department_and_Type.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    departments_list = [*ratings_by_department_and_type]
    types_list = [*ratings_by_type]
    writer.writerow([''] + types_list)
    for department in departments_list:
        writer.writerow([department] + [ratings_by_department_and_type[department].get(x, '') for x in types_list])

with open('./results/Ratings_by_Professor.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Professor', 'Average Rating', 'Number of Courses'])
    for key, value in teacher_ratings.items():
        writer.writerow([key, value, teacher_number_of_ratings[key]])

with open('./results/Ratings_by_Subject.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Subject', 'Average Rating'])
    for key, value in ratings_by_subject.items():
        writer.writerow([key, value])

