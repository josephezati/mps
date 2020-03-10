from calendar import HTMLCalendar
import datetime
from .models import*
from datetime import datetime, timedelta

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events, bds):
        events_per_day = events.filter(date__day=day)
        bds_per_day = bds.filter(date_of_birth__day=day)
        d = ''
        for event in events_per_day:
            d += f'<li id="event"> {event.topic} {event.date.hour}:{event.date.minute} </li>'

        for bd in bds_per_day:
            d += f'<li id="bd"> {bd.name}`s BD </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    # formats a week as a tr 
    def formatweek(self, theweek, events, bds):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events, bds)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = Meeting.objects.filter(date__year=self.year, date__month=self.month)
        bds = Student.objects.filter(date_of_birth__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events, bds)}\n'
        return cal