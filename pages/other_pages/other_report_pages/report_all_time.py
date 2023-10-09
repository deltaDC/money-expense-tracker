import sqlite3
from flet import *
import flet as ft
import datetime
from utils.navbar import create_navbar


BG_COLOR = "#191919"
GREY_COLOR = "#3f3f3f"
PINK = "#eb06ff"


class Report_All_Time(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def fetch_data_from_db():
            conn = sqlite3.connect("db/app.db")
            cursor = conn.cursor()
            data = cursor.execute("""SELECT * FROM financial_transaction""")
            result = [row for row in data]
            conn.close()
            return result

        
        def create_header():
            def change_button_colors(button_1: TextButton):
                button_1.style.bgcolor = GREY_COLOR
                header.update()

            button_1 = Text(
                "Báo cáo toàn kì", color="white"
            )
            button_1.on_click = lambda event: change_button_colors(button_1)
            header = Row(
                spacing=10,
                alignment="spaceBetween",
                controls=[
                    IconButton(icons.ARROW_BACK, 
                               icon_color="white",
                               on_click=lambda e:self.page.go('/other')
                               ),
                    button_1,
                    IconButton(icons.SEARCH, icon_color="white"),
                ],
            )
            return header

        
        def create_chitieu_thunhap_thuchi():
            data = fetch_data_from_db()
            # Create two text buttons.
            button_1 = Text(
                "Chi tiêu", color="White"
            )
            button_2 = Text(
                "Thu nhập", color="White"
            )
            button_3 = Text(
                "Tổng", color="White"
            )

            # Calculate and format the total expense and income from the data
            total_expense = sum(row[3] for row in data if row[5] == "Tiền chi")
            total_income = sum(row[3] for row in data if row[5] == "Tiền thu")

            chitieu_thunhap_tong1 = Column(
                
                alignment="spaceBetween",
                controls=[
                    Container(
                        padding=padding.only(30,10,30,10),
                        border=border.only(bottom=border.BorderSide(0.5, "#3c3c3c"), top=border.BorderSide(0.5, "#3c3c3c")),
                        content=Row(
                            alignment="spaceBetween",
                            controls=[
                                button_1,
                                Text(f"{total_expense} đ", color="white"),
                            ],
                        ),
                    ),
                    Container(
                        padding=padding.only(30,10,30,10),
                        border=border.only(bottom=border.BorderSide(0.5, "#3c3c3c"), top=border.BorderSide(0.5, "#3c3c3c")),
                        content=Row(
                            alignment="spaceBetween",
                            controls=[
                                button_2,
                                Text(f"{total_income} đ", color="white"),
                            ],
                        ),
                    ),
                    Container(
                        padding=padding.only(30,10,30,10),
                        border=border.only(bottom=border.BorderSide(0.5, "#3c3c3c"), top=border.BorderSide(0.5, "#3c3c3c")),
                        content=Row(
                            alignment="spaceBetween",
                            controls=[
                                button_3,
                                Text(f"{total_income-total_expense} đ", color="white"),
                            ],
                        ),
                    )
                ]
            )

            return  chitieu_thunhap_tong1

        

        header = create_header()
        chitieu_thunhap_thuchi = create_chitieu_thunhap_thuchi()

        
        page_3_child_container = Container(
            padding=padding.only(left=10, top=30, right=30),
            content=Column(
                controls=[
                    header,
                ]
            ),
        )
        page_3 = Container(
            width=400,
            height=712,
            border_radius=35,
            bgcolor=BG_COLOR,
            content=Column(
                controls=[
                    page_3_child_container,
                    chitieu_thunhap_thuchi 
                ],
            ),
        )

        return page_3
