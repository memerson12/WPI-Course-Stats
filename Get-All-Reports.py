import requests
from bs4 import BeautifulSoup
import CourseReports as Courses
import json

cookie = '4f42869efc8f1593d3b414e452127a5d'
base_url = 'https://oscar.wpi.edu/'


def main():
    home_page_html = requests.get(base_url, cookies={'MOD_AUTH_CAS_S': cookie}).text
    soup = BeautifulSoup(home_page_html, 'html.parser')
    for link in soup.find_all('a'):
        link_address = link.get('href')
        if 'oscar/' in link_address:
            year = link_address.split('/')[1].split('.')[0]
            print(f'Fetching reports from {year}')
            reports = get_reports_by_year(link_address, year)
            with open(f'./results/Course_Reports_{year}.json', 'w') as file:
                file.write(json.dumps(reports))


def get_reports_by_year(link_address: str, year):
    reports_html = requests.get(base_url + link_address, cookies={'MOD_AUTH_CAS_S': cookie}).text
    soup = BeautifulSoup(reports_html, 'html.parser')
    [teachers, class_obj] = soup.find_all('select')
    course_ratings = []
    classes = class_obj.find_all('option')
    classes.pop(0)
    number_of_classes = len(classes)
    curr_class = 1
    for class_option in classes:
        print(f'Getting class {curr_class}/{number_of_classes}')
        course_id = class_option.get('value')
        reports = Courses.getPastReports(course_id, year)
        for report in reports:
            rating = Courses.getRating(report)
            course_ratings.append(rating)
        curr_class += 1
    return course_ratings


if __name__ == '__main__':
    main()
