import re
import requests

cookie = '4f42869efc8f1593d3b414e452127a5d'


def getPastReports(course_id: str, year='2020-2021'):
    course_id_letters = re.search('[a-zA-Z]+', course_id).group()
    course_id_numbers = re.search('\d+', course_id).group()
    url = f'https://oscar.wpi.edu/cgi-bin/oscar/1.3/byC.cgi?courseNumber={course_id_letters} {course_id_numbers}&year={year}'
    reports = requests.get(url, cookies={'MOD_AUTH_CAS_S': cookie}).text.split('\n')
    for i in range(len(reports)):
        reports[i] = reports[i].split(';')
    reports.pop(len(reports) - 1)
    return reports


def getRating(report):
    return _getRating(report[3], report[0], report[5])


def _getRating(course_id, pidm_id, term):
    course_id_letters = re.search('[a-zA-Z]+', course_id).group()
    course_id_numbers = re.search('\d+', course_id).group()
    url = f'https://oscar.wpi.edu/cgi-bin/oscar/1.3/byPandC.cgi?pidm_id={pidm_id}&courseNumber={course_id_letters} {course_id_numbers}&term={term}'
    raw_rating = requests.get(url, cookies={'MOD_AUTH_CAS_S': cookie}).text
    return _extractReport(raw_rating.split(';'))


def _extractReport(fields):
    report_data = {
        "courseInfo": {
            "instructor": "",
            "courseTitle": "",
            "courseNumber": "",
            "numStudents": "",
            "courseType": "",
            "term": "",
            "subject": ""
        },
        "overallRatings": {
            "overallQuality": {
                "average": "5.0",
                "surveySize": "6",
                "scoreBreakdown": {
                    "oneStar": "0",
                    "twoStar": "0",
                    "threeStar": "0",
                    "fourStar": "0",
                    "fiveStar": "6"
                }
            },
            "overallInstructor": {
                "average": "5.0",
                "surveySize": "6",
                "scoreBreakdown": {
                    "oneStar": "0",
                    "twoStar": "0",
                    "threeStar": "0",
                    "fourStar": "0",
                    "fiveStar": "6"
                }
            },
            "educationalValue": {
                "average": "5.0",
                "surveySize": "6",
                "scoreBreakdown": {
                    "oneStar": "0",
                    "twoStar": "0",
                    "threeStar": "0",
                    "fourStar": "0",
                    "fiveStar": "6"
                }
            },
            "organization": {
                "average": "4.7",
                "surveySize": "6",
                "scoreBreakdown": {
                    "oneStar": "0",
                    "twoStar": "0",
                    "threeStar": "0",
                    "fourStar": "2",
                    "fiveStar": "4"
                }
            },
            "clarity": {
                "average": "4.8",
                "surveySize": "6",
                "scoreBreakdown": {
                    "oneStar": "0",
                    "twoStar": "0",
                    "threeStar": "0",
                    "fourStar": "1",
                    "fiveStar": "5"
                }
            },
            "instructorExplanationSkill": {
                "average": "4.8",
                "surveySize": "6",
                "scoreBreakdown": {
                    "oneStar": "0",
                    "twoStar": "0",
                    "threeStar": "0",
                    "fourStar": "1",
                    "fiveStar": "5"
                }
            },
            "amountLearned": {
                "average": "4.0",
                "surveySize": "6",
                "scoreBreakdown": {
                    "oneStar": "0",
                    "twoStar": "0",
                    "threeStar": "2",
                    "fourStar": "2",
                    "fiveStar": "2"
                }
            }
        },
        "relativeRating": {
            "amountLearned": {
                "average": "4.2",
                "surveySize": "6",
                "scoreBreakdown": {
                    "oneStar": "0",
                    "twoStar": "0",
                    "threeStar": "1",
                    "fourStar": "3",
                    "fiveStar": "2"
                }
            },
            "intellectualChallenge": {
                "average": "5.0",
                "surveySize": "6",
                "scoreBreakdown": {
                    "oneStar": "0",
                    "twoStar": "0",
                    "threeStar": "0",
                    "fourStar": "0",
                    "fiveStar": "6"
                }
            },
            "instructorInterest": {
                "average": "4.7",
                "surveySize": "6",
                "scoreBreakdown": {
                    "oneStar": "0",
                    "twoStar": "0",
                    "threeStar": "0",
                    "fourStar": "2",
                    "fiveStar": "4"
                }
            },
            "interestStimulated": {
                "average": "3.7",
                "surveySize": "6",
                "scoreBreakdown": {
                    "oneStar": "0",
                    "twoStar": "0",
                    "threeStar": "3",
                    "fourStar": "2",
                    "fiveStar": "1"
                }
            },
            "workload": {
                "average": 0,
                "surveySize": 0,
                "scoreBreakdown": {
                    "oneStar": 0,
                    "twoStar": 0,
                    "threeStar": 0,
                    "fourStar": 0,
                    "fiveStar": 0
                }
            }
        },
        "frequentlyTrue": {
            "instructorWellPrepared": {
                "average": "5.0",
                "surveySize": "6",
                "scoreBreakdown": {
                    "oneStar": "0",
                    "twoStar": "0",
                    "threeStar": "0",
                    "fourStar": "0",
                    "fiveStar": "6"
                }
            },
            "encouragedToQuestion": {
                "average": "5.0",
                "surveySize": "6",
                "scoreBreakdown": {
                    "oneStar": "0",
                    "twoStar": "0",
                    "threeStar": "0",
                    "fourStar": "0",
                    "fiveStar": "6"
                }
            },
            "instructorRespectful": {
                "average": "5.0",
                "surveySize": "6",
                "scoreBreakdown": {
                    "oneStar": "0",
                    "twoStar": "0",
                    "threeStar": "0",
                    "fourStar": "0",
                    "fiveStar": "6"
                }
            },
            "helpfulFeedback": {
                "average": "4.8",
                "surveySize": "6",
                "scoreBreakdown": {
                    "oneStar": "0",
                    "twoStar": "0",
                    "threeStar": "0",
                    "fourStar": "1",
                    "fiveStar": "5"
                }
            },
            "goodExams": {
                "average": "5.0",
                "surveySize": "6",
                "scoreBreakdown": {
                    "oneStar": "0",
                    "twoStar": "0",
                    "threeStar": "0",
                    "fourStar": "0",
                    "fiveStar": "6"
                }
            },
            "gradesFair": {
                "average": "4.8",
                "surveySize": "5",
                "scoreBreakdown": {
                    "oneStar": "0",
                    "twoStar": "0",
                    "threeStar": "0",
                    "fourStar": "1",
                    "fiveStar": "4"
                }
            }
        },
        "misc": {
            "expectedGrade": {
                "average": "1.8",
                "surveySize": "6",
                "scoreBreakdown": {
                    "oneStar": "4",
                    "twoStar": "1",
                    "threeStar": "0",
                    "fourStar": "0",
                    "fiveStar": "1"
                }
            },
            "outsideClassTime": {
                "average": "0",
                "surveySize": "0",
                "hourBreakdown": {
                    "zero": "0",
                    "oneToFive": "0",
                    "sixToTen": "0",
                    "elevenToFifteen": "0",
                    "sixteenToTwenty": "0",
                    "twentyOnePlus": "0"
                }
            }
        }
    }
    report_data['courseInfo']['instructor'] = fields[1]
    report_data['courseInfo']['courseTitle'] = fields[2]
    report_data['courseInfo']['courseNumber'] = fields[3]
    report_data['courseInfo']['numStudents'] = fields[4]
    report_data['courseInfo']['courseType'] = fields[5]
    report_data['courseInfo']['term'] = fields[6]
    all_entries = _processDone(fields[7])

    n0 = -1
    for j in range(19):
        n1 = _nthIndex(all_entries, ",", 9, n0)
        token = all_entries[n0 + 1: n1]
        lots = token.split(',')
        if j < 7:
            keys = [*report_data['overallRatings']]
            _lotsToObject(report_data, lots, 'overallRatings', keys[j])
        elif j < 11:
            keys = [*report_data['relativeRating']]
            _lotsToObject(report_data, lots, 'relativeRating', keys[j - 7])
        elif j < 17:
            keys = [*report_data['frequentlyTrue']]
            _lotsToObject(report_data, lots, 'frequentlyTrue', keys[j - 11])
        elif j == 17:
            _lotsToObject(report_data, lots, 'misc', 'expectedGrade')
        else:
            report_data['misc']['outsideClassTime']['average'] = lots[8]
            report_data['misc']['outsideClassTime']['surveySize'] = lots[7]
            report_data['misc']['outsideClassTime']['hourBreakdown']['zero'] = lots[1]
            report_data['misc']['outsideClassTime']['hourBreakdown']['oneToFive'] = lots[2]
            report_data['misc']['outsideClassTime']['hourBreakdown']['sixToTen'] = lots[3]
            report_data['misc']['outsideClassTime']['hourBreakdown']['elevenToFifteen'] = lots[4]
            report_data['misc']['outsideClassTime']['hourBreakdown']['sixteenToTwenty'] = lots[5]
            report_data['misc']['outsideClassTime']['hourBreakdown']['twentyOnePlus'] = lots[6]
        n0 = n1
    return report_data


def _lotsToObject(report_data, lots, section, key):
    report_data[section][key]['average'] = lots[8]
    report_data[section][key]['surveySize'] = lots[7]
    report_data[section][key]['scoreBreakdown']['oneStar'] = lots[1]
    report_data[section][key]['scoreBreakdown']['twoStar'] = lots[2]
    report_data[section][key]['scoreBreakdown']['threeStar'] = lots[3]
    report_data[section][key]['scoreBreakdown']['fourStar'] = lots[4]
    report_data[section][key]['scoreBreakdown']['fiveStar'] = lots[5]


def _processDone(data: str):
    data = data.replace('w', '0')
    data = data.replace('b', '.')
    data = re.sub('[rstvxzcdfghjklmnpq]', '', data)
    data = re.sub('[aeiouy]', ',', data)
    return data


def _nthIndex(string: str, pat, n, i):
    L = len(string)
    while n != 0 and i < L:
        n -= 1
        i += 1
        i = string.find(pat, i)
        if i < 0:
            break
    return i
