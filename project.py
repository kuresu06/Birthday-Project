from datetime import datetime
import csv
import re
import sys
import requests
from bs4 import BeautifulSoup

def main():
    humans = read_human("./Data/birthdays.csv")
    add_human('a', 'b', '2004-07-22', humans)
    for human in humans:
        #print(human)
        print(human.get_next_birthday())

class Human():
    def __init__(self, first, last, birthday):
        self.first = first
        self.last = last
        try:
            self.birthday = datetime.fromisoformat(birthday)
        except ValueError:
            sys.exit("Incorrect date")

    def __repr__(self):
        return f"{self.first} {self.last}, {self.birthday}"

    def get_born(self):
        return self.birthdate

    def get_next_birthday(self):
        today = datetime.today()
        b = self.birthday.replace(year = today.year)
        time = b - today
        if(time.days<0):
            time = self.birthday.replace(year = today.year+1) - today

        return str(time)

def read_human(file_name):
    humans=[]
    with open(file_name) as file:
        reader = csv.DictReader(file)
        for row in reader:
            humans.append(Human(row['first'], row['last'], row['birthdate']))
    return humans

def add_human(first, last, birthday, L):
    L.append(Human(first, last, birthday))

def write_human(file):
    return

class Holiday():
    def __init__(self, date, en_name, lt_name, remarks):
        self.date = date
        self.en_name = en_name
        self.lt_name = lt_name
        self.remarks = remarks

def read_holidays():
    url = 'https://en.wikipedia.org/wiki/Public_holidays_in_Lithuania'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('table', class_="wikitable")

    headers = table.find_all('th')
    header = []
    for h in headers:
        if t:= h.get_text(strip=True):
            header.append(t)

    data=[]
    trs = table.find_all('tr')
    for field in trs:
        new = []
        tds = field.find_all('td')
        for t in tds:
            if t.get_text(strip=True):
                new.append(t.get_text(strip=True))
        if(len(new)!=0):
            d = {}
            for i in range(len(new)):
                d.update({header[i]:new[i]})
            data.append(d)


if __name__ == "__main__":
    main()
