##parameters=year, month
# $Id$
"""Returns last day of month."""

from DateTime import DateTime

dt = DateTime('%s/%s/1' % (year, month))

if dt.isLeapYear():
    days_in_february = 29
else:
    days_in_february = 28

days_per_month ={'January' : 31,
                 'February': days_in_february,
                 'March' : 31,
                 'April': 30,
                 'May' : 31,
                 'June': 30,
                 'July': 31,
                 'August': 31,
                 'September': 30,
                 'October': 31,
                 'November': 30,
                 'December': 31
                 }

return days_per_month[dt.Month()]
