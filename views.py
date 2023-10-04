from flet import *
from pages.outcome import Outcome
from pages.income import Income
from pages.calendar import Calendar
from pages.reports.report_outcome import Report
from pages.reports.report_income import Report1
from pages.other import Other
from pages.reports.report_year_outcome import Report2
from pages.reports.report_year_income import Report3

def views_handler(page):
    return {
        '/':View(
            route='/',
            controls=[
                Outcome(page)
            ]
        ),
        '/page_2':View(
            route='/page_2',
            controls=[
                Income(page)
            ]
        ),
        '/calendar':View(
            route='/calendar',
            controls=[
                Calendar(page)
            ]
        ),
        '/report':View(
            route='/report',
            controls=[
                Report(page)
            ]
        ),
        '/report_1':View(
            route='/report_1',
            controls=[
                Report1(page)
            ]
        ),
        '/other':View(
            route='/other',
            controls=[
                Other(page)
            ]
        ),
        '/report_2':View(
            route='/report_2',
            controls=[
                Report2(page)
            ]
        ),
        '/report_3':View(
            route='/report_3',
            controls=[
                Report3(page)
            ]
        ),
    }