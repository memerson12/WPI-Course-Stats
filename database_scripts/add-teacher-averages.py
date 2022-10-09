import json
import os
import mysql.connector

from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv('PS_HOST'),
    user=os.getenv('PS_USERNAME'),
    password=os.getenv('PS_PASSWORD'),
)
cursor = mydb.cursor()

teacher_total_rating = {}
teacher_number_classes = {}
teacher_number_ratings = {}
professors_ids = {}


def main():
    statement = 'SELECT id, first_name, last_name FROM professors'
    cursor.execute(statement)
    for row in cursor.fetchall():
        professors_ids[f'{row[2]}, {row[1]}'] = row[0]
    report_files = os.listdir('../data')
    for report_name in report_files:
        with open(f'../data/{report_name}', 'r') as file:
            if not file.name.endswith('.json'):
                continue
            reports = json.load(file)
            for report in reports:
                teacher = report['courseInfo']['instructor']
                new_rating = report['overallRatings']['overallQuality']['average']
                number_ratings = int(report['overallRatings']['overallQuality']['surveySize'])
                if new_rating == '':
                    continue
                number_classes = teacher_number_classes.get(teacher, 0)
                current_number_ratings = teacher_number_ratings.get(teacher, 0)
                new_rating = float(new_rating)
                current_rating = teacher_total_rating.get(teacher, 0)
                teacher_total_rating[teacher] = (current_rating + new_rating)
                teacher_number_classes[teacher] = number_classes + 1
                teacher_number_ratings[teacher] = current_number_ratings + number_ratings
    teacher_total_rating_final = {key: (value / teacher_number_classes[key]) for key, value in
                                  teacher_total_rating.items()}

    params = ''
    for professor, average in teacher_total_rating_final.items():
        params += f'({professors_ids[professor]}, {average}), '
    params = params[:-2]
    statement = f"""INSERT into professors (id, average_rating)
        VALUES {params}
        ON DUPLICATE KEY UPDATE average_rating = VALUES(average_rating);"""

    cursor.execute(statement)
    mydb.commit()


if __name__ == '__main__':
    main()
