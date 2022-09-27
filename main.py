import requests
import json
import CourseReports as Courses

ratings = {}


def main():
    courses = requests.get('https://courselistings.wpi.edu/assets/prod-data.json').json()
    total_courses = len(courses['Report_Entry'])
    current_course = 0
    last_course_id = ''
    for course in courses['Report_Entry']:
        current_course += 1
        course_id = course['Course_Title'].split('-')[0]
        if course_id == last_course_id: continue
        print(f'{current_course}/{total_courses}: {course["Course_Title"]}')
        last_course_id = course_id
        reports = Courses.get_past_reports(course_id)
        for report in reports:
            report_info = Courses.get_rating(report)
            department = course['Course_Section_Owner']
            course_type = report_info['courseInfo']['courseType']
            report_info['courseInfo']['subject'] = course['Subject']
            if department not in ratings:
                ratings[department] = {}
            if course_type not in ratings[department]:
                ratings[department][course_type] = []
            ratings[department][course_type].append(report_info)
    with open('ratings_with_subject.json', 'w') as file:
        file.write(json.dumps(ratings, indent=2))


if __name__ == '__main__':
    main()
