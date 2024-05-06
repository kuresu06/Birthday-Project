from datetime import datetime
import csv
import re
import sys
import requests

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
    
# class Holiday():
#     def __init__(self, name, date):
#         self.name = name
#         self.date = date
        

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


if __name__ == "__main__":
    main()
