import datetime
import csv
from re import match
import sys
from requests import get
from bs4 import BeautifulSoup

today = datetime.datetime.now()
months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}


def main():
    humans = read_human("./Data/birthdays.csv")
    add_human('a', 'b', '2004-07-22', humans)
    print('-----------------Bdays:')
    for human in humans:
        #print(human)
        print(human.get_next_time())

    print('-----------------Holidays:')
    hol = get_holidays()
    for h in hol:
        print(h.get_next_time())

class Human():
    def __init__(self, first, last, birthday):
        self.first = first
        self.last = last
        try:
            self.birthday = datetime.datetime.fromisoformat(birthday)
        except ValueError:
            sys.exit("Incorrect date")

    def __repr__(self):
        return f"{self.first} {self.last}, {self.birthday}"

    def get_born(self):
        return self.birthdate

    def get_next_time(self):
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
    def __init__(self, name, date):
        self.name = name
        (m , d) = date.split(",")[0].split(" ")
        if(m in months.keys() and d.isdigit()):
            self.date = datetime.datetime(today.year, months[m], int(d))
    
    def get_next_time(self):
        time = self.date - today
        if(time.days<0):
            time = self.date.replace(year = today.year+1) - today
        return time
    
    def __str__(self):
        return f"{self.name} {self.date}"

def get_holidays():
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

if __name__ == "__main__":
    main()
