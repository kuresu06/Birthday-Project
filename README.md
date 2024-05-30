# Birthday reminder

### Description:
Program for reminding you of upcoming birthdays and national (Lithuanian) holidays.
Made for practicing python and trying webscraping + GUI creation.

### Details:
- The birthdays are stored in a dictionary which is created by reading a .csv file.
- Dates of national holidays are gotten by webscraping (using BeautifulSoup and requests) the following website - https://www.wincalendar.com/Calendar-Lithuania/{insert year}.
- Both birthdays and holidays are stored as their respective objects that hold relevant info and provide methods used for getting, setting and storing data.
- A list is created and stored by the amount of time left until the date.
- Very simple GUI is implemented that lets the user input how many dates do they want to see, then that many are displayed after clicking "Display."

### Libraries used:
- from python:
    - datetime
    - csv
    - re
    - sys
    - random
    - tkinter
- external:
    - requests
    - bs4

### TODO:
- Create add date functionality in GUI.
- Display the dates in table format.
- Create functionality that shows the date of a selected birthday/holiday.