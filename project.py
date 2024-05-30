import datetime
import csv
from re import match
import sys
from requests import get
from bs4 import BeautifulSoup
import random
from tkinter import *

today = datetime.date.today()
months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}

def main():
    # Storing data
    bdays = read_humans("./Data/birthdays.csv")
    add_human('vardas', 'pavarde', '2004-07-22', bdays)

    hdays = read_holidays()

    # Making GUI
    root = Tk()
    root.title("Date reminder")
    root.geometry("800x800")
    head_Label = Label(root, text="Date reminder", font=("Helvetica", 24))
    head_Label.pack()

    entry_label = Label(root, text="How many upcoming dates to display?", font=("Helvetica", 12))
    entry_label.pack(pady=20)

    entry = Entry(root)
    entry.pack(pady=10)

    display_button = Button(root, text="Display",
                             command= lambda: create_dates_display(root, entry.get(), sort_by_time(bdays+hdays)))
    display_button.pack(pady=20)
    


    root.mainloop()

def create_dates_display(root, amount, dates):
    try:
        amount = int(amount.strip())
    except:
        if hasattr(root, 'lbl'):
            root.lbl.destroy()
        root.lbl = Label(root, text="invalid")
        root.lbl.pack()
        return

    if hasattr(root, 'lbl'):
        root.lbl.destroy()
    root.lbl = Label(root, text=get_dates_txt(dates, amount), font=("Helvetica", 12))
    root.lbl.pack()

def get_all_times(h, b):
    all = []
    for x in [h, b]:
        for y in x:
            all.append(y.get_next_time())
    return all

def get_dates(all, amount):
    for i in all[:amount]:
        if type(i).__name__ == 'Human':
            if (i.get_next_time().days == 0):
                print(f'Birthday of {i.first} {i.last} is today!')
            else:
                print(f'Birthday of {i.first} {i.last} in {i.get_next_time().days} days')
        if type(i).__name__ == 'Holiday':
            if (i.get_next_time().days == 0):
                print(f'{i.name} is today!')
            else:
                print(f'Holiday - {i.name} in {i.get_next_time().days} days')

def get_dates_txt(all, amount):
    txt = ""
    for i in all[:amount]:
        if type(i).__name__ == 'Human':
            if (i.get_next_time().days == 0):
                txt+=f'Birthday of {i.first} {i.last} is today!\n'
            else:
                txt+=f'Birthday of {i.first} {i.last} in {i.get_next_time().days} days\n'
        if type(i).__name__ == 'Holiday':
            if (i.get_next_time().days == 0):
                txt+=f'{i.name} is today!\n'
            else:
                txt+=f'Holiday - {i.name} in {i.get_next_time().days} days\n'
    return txt


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
        return time
    
    def __gt__(self, other):
        return self.date > other.date 

def read_humans(file_name):
    humans=[]
    with open(file_name) as file:
        reader = csv.DictReader(file)
        for row in reader:
            humans.append(Human(row['first'], row['last'], row['birthdate']))

    return humans

def add_human(first, last, birthday, L):
    L.append(Human(first, last, birthday))

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
        return time
    
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

def sort_by_time(times):
    swap = True
    while(swap):
        swap = False
        for i in range(len(times)):
            if i+1<len(times) and (times[i].get_next_time()>times[i+1].get_next_time()):
                temp = times[i]
                times[i] = times[i+1]
                times[i+1] = temp
                swap = True
    return times

if __name__ == "__main__":
    main()