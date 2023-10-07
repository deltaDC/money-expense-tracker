from flet import *
from pages.outcome import Outcome
from pages.income import Income
from pages.calendar import Calendar
from pages.reports.report_outcome import Report
from pages.reports.report_income import Report1
from pages.other import Other
from pages.reports.report_year_outcome import Report2
from pages.reports.report_year_income import Report3
from pages.reports.report_toanki import Report4
from pages.reports.report_danhmuctoanki1 import Report5
from pages.reports.report_danhmuctoanki2 import Report6
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
        '/report_4':View(
            route='/report_4',
            controls=[
                Report4(page)
            ]
        ),
        '/report_5':View(
            route='/report_5',
            controls=[
                Report5(page)
            ]
        ),
        '/report_6':View(
            route='/report_6',
            controls=[
                Report6(page)
            ]
        ),
    }