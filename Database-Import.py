import json
import os
import re

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv('PS_HOST'),
    user=os.getenv('PS_USERNAME'),
    password=os.getenv('PS_PASSWORD'),
)
cursor = mydb.cursor()


def main():
    report_files = sorted(os.listdir('./data'))
    print(report_files)
    for report_name in report_files:
        if report_name == '.DS_Store':
            continue
        inserts = []
        year = report_name.split("_")[2].replace('.json', '')
        with open(f'./data/{report_name}', 'r') as file:
            reports = json.load(file)
            print(f'Creating Inserts for {year}')
            for report in reports:
                if len(inserts) >= 1000:
                    sql = f"""
                           INSERT INTO courses (course_title, course_number, course_type,
                                            instructor, response_count, subject, term,
                                            year, report_data)
                           VALUES {", ".join(inserts)}
                           """
                    print(f'\tAttempting to insert {len(inserts)} courses')
                    cursor.execute(sql)
                    print('\t\tStatement Executed')
                    mydb.commit()
                    print('\t\tDatabase Committed')
                    inserts = []
                info = report['courseInfo']
                title = parse_titles(info['courseTitle'])
                course_number = info['courseNumber'].strip()
                subject = course_number.split(' ')[0]
                term = info['term'].split('_')[1]
                if info['courseType'] not in ['Lecture', 'Web', 'Seminar', 'Practicum', 'Lab', 'ADLN', 'Corporate Ed',
                                              'GPS', 'Conference', 'Blended', 'Other']:
                    print('Course Type not in Schema')
                    print(info)
                    exit()
                course_rating = {"overallRatings": report['overallRatings'], "frequentlyTrue": report['frequentlyTrue'],
                                 "relativeRating": report['relativeRating'], "misc": report['misc']}

                inserts.append(
                    f"('{title}', '{course_number}', '{info['courseType']}', '{parse_titles(info['instructor'])}', "
                    f"{info['numStudents']}, '{subject}', '{term}', '{year}', '{json.dumps(course_rating)}')")
        if inserts:
            sql = f"""
            INSERT INTO courses (course_title, course_number, course_type,
                             instructor, response_count, subject, term,
                             year, report_data)
            VALUES {", ".join(inserts)}
            """
            print(f'\tAttempting to insert {len(inserts)} courses')
            cursor.execute(sql)
            print('\t\tStatement Executed')
            mydb.commit()
            print('\t\tDatabase Committed')
        print()


def parse_titles(text: str):
    title = text.replace('  ', '').replace("'", "\\'").replace('"', '\\"').title().strip()
    title = fix_roman_numeral(title)
    return title


def fix_roman_numeral(text: str):
    possible_numerals = text.split(' ')
    search = re.search('(I{2,}|\bIV)', possible_numerals[-1], re.IGNORECASE)
    if search:
        return " ".join(possible_numerals[:-1]) + " " + possible_numerals[-1].upper()
    else:
        return " ".join(possible_numerals)


if __name__ == '__main__':
    main()
