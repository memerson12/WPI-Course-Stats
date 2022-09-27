import requests
from bs4 import BeautifulSoup
import CourseReports as Courses
import json

cookie = '24e97d4bbe9b1e58c6bbf6a5a9cdc912'
base_url = 'https://oscar.wpi.edu/'


def main():
    home_page_html = requests.get(base_url, cookies={'MOD_AUTH_CAS_S': cookie}).text
    soup = BeautifulSoup(home_page_html, 'html.parser')
    links = soup.find_all('a')
    links.reverse()
    for link in links:
        link_address = link.get('href')
        if 'oscar/' in link_address:
            year = link_address.split('/')[1].split('.')[0]
            print(f'Fetching reports from {year}')
            reports = get_reports_by_year(link_address, year)
            with open(f'./data/Course_Reports_{year}.json', 'w') as file:
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
    previous_course_id = ''
    for class_option in classes:
        print(f'Getting class {curr_class}/{number_of_classes}')
        course_id = class_option.get('value')
        if previous_course_id == course_id:
            curr_class += 1
            continue
        reports = Courses.get_past_reports(course_id, year)
        for report in reports:
            rating = Courses.get_rating(report)
            course_ratings.append(rating)
        curr_class += 1
        previous_course_id = course_id
    return course_ratings


if __name__ == '__main__':
    main()
