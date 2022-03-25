import os
import json
import csv

teacher_average_rating = {}
teacher_number_classes = {}


def main():
    report_files = os.listdir('./data')
    for report_name in report_files:
        with open(f'./data/{report_name}', 'r') as file:
            reports = json.load(file)
            for report in reports:
                teacher = report['courseInfo']['instructor']
                new_rating = report['overallRatings']['overallQuality']['average']
                if new_rating == '': continue
                number_classes = teacher_number_classes.get(teacher, 0)
                new_rating = float(new_rating)
                current_rating = teacher_average_rating.get(teacher, new_rating)
                teacher_average_rating[teacher] = (current_rating + new_rating) / 2
                teacher_number_classes[teacher] = number_classes + 1
    print(teacher_average_rating)
    with open('./results/Teacher_Raking_All_Years.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Professor', 'Average Rating', 'Number of Courses'])
        for key, value in teacher_average_rating.items():
            writer.writerow([key, value, teacher_number_classes[key]])


if __name__ == '__main__':
    main()
