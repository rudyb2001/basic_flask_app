import requests
from bs4 import BeautifulSoup
import bs4
from datetime import datetime, timedelta
import json
from flask import Flask

app = Flask(__name__)
@app.route("/")
def base():
    message = {"message": "Hello"}
    return json.dumps(message)

def is_within_next_n_days(date: datetime, n: int):
    today = datetime.today()
    print(str(today) + " - " + str(date) + " - " + str(today + timedelta(days=7)))
    return today <= date <= today + timedelta(days=n)

def get_events_within_n_days(elements: bs4.element.ResultSet, n: int):
    hyperlinks = []
    for li in elements:
        day = li.find("div", class_="uw-event-date")
        month_day_text = day.get_text(strip=True, separator=' ')
        date_text = month_day_text + " 2023"
        date = datetime.strptime(date_text, "%B %d %Y")
        if not is_within_next_n_days(date, n):
            continue

        # Find the <a> tag within the <span> element
        link = li.find('a')
        if link:
            href = link.get('href')
            hyperlinks.append(href)

    return hyperlinks

# Print the list of hyperlinks
def get_event_details(link):
    #print(type(link), link)
    cs_event_response = requests.get(link)
    soup = BeautifulSoup(cs_event_response.text, 'html.parser')

    event_details = {}

    title = soup.find("h1", class_="view-event-title").get_text(strip=True)
    print(title)
    event_details["title"] = title

    elements = soup.find_all("div", class_="event-row")
    for element in elements:
        children = element.find_all()
        element_title = children[0].get_text(strip=True, separator=' ')
        element_details = children[1].get_text(strip=True, separator=' ')
        #print("\t" + element_title + ": " + element_details)
        event_details[element_title.lower()] = element_details
    return event_details

@app.route('/cs_events/', defaults={'days': 7})
@app.route('/cs_events/<days>')
def get_cs_events(days):
    cs_events_response = requests.get("https://www.cs.wisc.edu/cs-events/")
    soup = BeautifulSoup(cs_events_response.text, 'html.parser')

    elements = soup.find_all("li", class_="uw-event")
    
    hyperlinks = get_events_within_n_days(elements, int(days))

    events = []
    for link in hyperlinks:
        event = get_event_details(link)
        events.append(event)
    
    response = json.dumps({"message": events})
    print(response)
    return response

if __name__ == "__main__":
    app.run()

"""
if __name__ == "__main__":
    get_cs_events(7)
"""
    
