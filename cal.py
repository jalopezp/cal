import argparse
import sys
import datetime
import calendar

from calendar import formatstring


class TrimesterTextCalendar(calendar.TextCalendar):
    """
    Subclass of TextCalendar, which aims to output a
    text calendar similar to the unix program cal,
    whcih contains a feature to display three months
    at a single time.
    """

    def prtrimester(self, theyear, themonth, w=0, l=0, c=6):
        """
        Print three months of a calendar, including
        the two months surrounding the month passed
        as an argument.
        """
        print self.formattrimester(theyear, themonth, w, l, c)

    def formattrimester(self, theyear, themonth, w, l, c):
        """
        Formats a calendar trimester as a multi line string.
        """
        w=max(2,w)
        l=max(1,l)
        c=max(2,c)
        colwidth = (w + 1) * 7 - 1

        v = []
        a = v.append

        header = self.formatweekheader(w)
        prevmonth = (themonth-2)%12+1
        nextmonth = themonth%12+1
        if themonth==12:
            nextyear=theyear+1
            prevyear=theyear
        elif themonth==1:
            nextyear=theyear
            prevyear=theyear-1
        else :
            nextyear=theyear
            prevyear=theyear

        monthnames = formatstring(
                         [ self.formatmonthname(prevyear, prevmonth, colwidth, True)
                         , self.formatmonthname(theyear, themonth, colwidth, True)
                         , self.formatmonthname(nextyear, nextmonth, colwidth, True)
                         ]
                    , colwidth, c)
        headers = calendar.formatstring((header for i in range(3)), colwidth, c)

        a(monthnames)
        a('\n'*l)
        a(headers)
        a('\n'*l)

        row =   [ self.monthdays2calendar(prevyear, prevmonth)
                , self.monthdays2calendar(theyear, themonth)
                , self.monthdays2calendar(nextyear, nextmonth)
                ]
        height = max(len(cal) for cal in row)
        for j in range(height):
            weeks = []
            for cal in row:
                if j >= len(cal):
                    weeks.append('')
                else:
                    weeks.append(self.formatweek(cal[j], w))
            a(formatstring(weeks, colwidth, c).rstrip())
            a('\n' * l)
        return ''.join(v)

class TrueAndVal(argparse.Action):
    def __call__(self, parser, args, values, option_string=None):
        setattr(args, self.dest, True)
        setattr(args, self.dest+'val', values)
today =  datetime.date.today()


parser = argparse.ArgumentParser(description='cal - display a calendar')

parser.add_argument('month', nargs='?', default=today.month, type=int, choices=range(1,13), help='The month to display, must be a number between 1 and 12. Defaults to the current month.', metavar='month')
parser.add_argument('year', nargs='?', default=today.year, type=int, choices=range(1,9999), help='The year to display, must be a number between 1 and 9999. Defaults to the current year.', metavar='year')
parser.add_argument('--three', '-3', action='store_true', help='Displays the calendar for three months, including the two surrounding the specified month.')
parser.add_argument('-y', nargs='?', action=TrueAndVal, type=int, help='Displays the calendar for a whole year.')

arg=parser.parse_args()


cal = TrimesterTextCalendar()
if arg.three :
    cal.prtrimester(arg.year, arg.month)
elif arg.y :
    if arg.yval==None :
        cal.pryear(arg.year)
    else :
        cal.pryear(arg.yval)
else :
    cal.prmonth(arg.year, arg.month)
# cal.prtrimester(arg.year, arg.month)
