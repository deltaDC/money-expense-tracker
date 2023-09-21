from flet import *
from pages.input import Input
from pages.input_1 import Input_1

def views_handler(page):
    return {
        '/':View(
            route='/',
            controls=[
                Input(page)
            ]
        ),
        '/page_2':View(
            route='/page_2',
            controls=[
                Input_1(page)
            ]
        ),
    }