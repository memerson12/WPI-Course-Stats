import json
import re


f = open("prod-data.json", "r")

data = json.load(f)
CLEANR = re.compile(r'<.*?>')

res = {}
for course in data["Report_Entry"]:
    title = course["Course_Title"]
    num = title.split(" - ")[0]
    name = title.split(" - ")[1]
    description = course.get("Course_Description", None)
    # clean up the description
    if description:
        description = CLEANR.sub(" ", description).strip()
        # replace any double or more spaces with single spaces
        description = re.sub(r"Cat\.? III\.?", "_3_ ", description)
        description = re.sub(r"Cat\.? II\.?", "_2_ ", description)
        description = re.sub(r"Cat\.? I\.?", "_1_ ", description)

        description = description.replace("_1_", "Cat. I")
        description = description.replace("_2_", "Cat. II")
        description = description.replace("_3_", "Cat. III")

        description = re.sub(r"\s+", " ", description)

    # format is num: {name: name, description: description, subject: subject, academic_level: academic_level}
    if num not in res:
        res[num] = {"name": name, "description": description,
                    "subject": course["Subject"], "academic_level": course["Academic_Level"], "format": course["Instructional_Format"]}


with open("output.json", "w") as f:
    json.dump(res, f, indent=2)


f.close()
