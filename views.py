from flet import *
from pages.outcome import Outcome
from pages.income import Income
from pages.calendar import Calendar
from pages.report import Report
from pages.other import Other

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
        '/other':View(
            route='/other',
            controls=[
                Other(page)
            ]
        ),
    }