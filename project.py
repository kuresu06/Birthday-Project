import datetime
import csv
from re import match
import sys
from requests import get
from bs4 import BeautifulSoup
import random

today = datetime.date.today()
months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

def main():
    bdays = read_humans("./Data/birthdays.csv")
    add_human('a', 'b', '2004-07-22', bdays)

    hdays = read_holidays()
    hdays = random.sample(hdays, len(hdays))
    hdays = sort_by_date(hdays)

    bdays = random.sample(bdays, len(bdays))
    bdays = sort_by_date(bdays)

def get_all_times(h, b):
    all = []
    for x in [h, b]:
        for y in x:
            all.append(y.get_next_time())
    return all

def get_next_five():
    return


class Human():
    def __init__(self, first, last, date):
        self.first = first
        self.last = last
        try:
            self.date = datetime.date.fromisoformat(date).replace(year = today.year)
        except ValueError:
            sys.exit("Incorrect date")

    def __repr__(self):
        return f"{self.first} {self.last}, {self.date}"

    def get_born(self):
        return self.birthdate

    def get_next_time(self):
        time = self.date - today
        if(time.days<0):
            time = self.date.replace(year = today.year+1) - today

        return time.days

def read_humans(file_name):
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

#--------------------------------------------------------
class Holiday():
    def __init__(self, name, date):
        self.name = name
        (m , d) = date.split(",")[0].split(" ")
        if(m in months.keys() and d.isdigit()):
            self.date = datetime.date(today.year, months[m], int(d))
    
    def get_next_time(self):
        time = self.date - today
        if(time.days<0):
            time = self.date.replace(year = today.year+1) - today
        return time.days
    
    def __str__(self):
        return f"{self.name} {self.date}"
    
    def __gt__(self, other):
        return self.date > other.date

def read_holidays():
    url = f'https://www.wincalendar.com/Calendar-Lithuania/{today.year}'
    r = get(url) # sends get request
    soup = BeautifulSoup(r.content, 'html.parser') #parses gotten html
    table = soup.find('table', class_="thlinks") #finds the table where the data is stored

    trs = table.find_all('tr')

    holidays = []
    for tr in trs:
        tds = tr.find_all('td')
        a = tr.find('a').get_text()
        if(t:=match(r".*Date (.*) in a Calendar.*", tds[3].a['title']).group(1)):
            holidays.append(Holiday(a, t))
    return holidays

def sort_by_date(dates):
    swap = True
    while(swap):
        swap = False
        for i in range(len(dates)):
            if i+1<len(dates) and (dates[i].date>dates[i+1].date):
                temp = dates[i]
                dates[i] = dates[i+1]
                dates[i+1] = temp
                swap = True
    return dates
if __name__ == "__main__":
    main()
