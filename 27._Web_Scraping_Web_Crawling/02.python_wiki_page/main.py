import requests
from bs4 import BeautifulSoup

html = requests.get("wiki side").text
parsed_html = BeautifulSoup(html, "lxml")


tags = parsed_html.find("div", {"class": "mw-parsed-output"})

projects = {
    "Initial_Category":
}

current_category = None

for tag in tags:
    if tag.name == "h2":
        current_category = tag.text.replace("[edit]", "")
        projects[current_category] = []
    elif tag.name == "ul":
        for li in tag.find_all("li"):
            projects[current_category].append(li.text)


print(projects)
