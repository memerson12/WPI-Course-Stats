import os
import json
import csv

teacher_total_rating = {}
teacher_number_classes = {}
teacher_number_ratings = {}


def main():
    report_files = os.listdir('./data')
    for report_name in report_files:
        with open(f'./data/{report_name}', 'r') as file:
            reports = json.load(file)
            for report in reports:
                teacher = report['courseInfo']['instructor']
                new_rating = report['overallRatings']['overallQuality']['average']
                number_ratings = int(report['overallRatings']['overallQuality']['surveySize'])
                if new_rating == '': continue
                number_classes = teacher_number_classes.get(teacher, 0)
                current_number_ratings = teacher_number_ratings.get(teacher, 0)
                new_rating = float(new_rating)
                current_rating = teacher_total_rating.get(teacher, 0)
                teacher_total_rating[teacher] = (current_rating + new_rating)
                teacher_number_classes[teacher] = number_classes + 1
                teacher_number_ratings[teacher] = current_number_ratings + number_ratings
    print(teacher_total_rating)
    with open('./results/Teacher_Raking_All_Years.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Professor', 'Average Rating', 'Number of Courses', 'Total Number of Ratings'])
        for key, value in teacher_total_rating.items():
            writer.writerow([key, value/teacher_number_classes[key], teacher_number_classes[key], teacher_number_ratings[key]])


if __name__ == '__main__':
    main()
