import sqlite3
from flet import *
import flet as ft


BG_COLOR = "#191919"
GREY_COLOR = "#3f3f3f"
PINK = "#eb06ff"
BLUE = "#0077b6"


class Search(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def fetch_data_from_db():
            conn = sqlite3.connect("db/app.db")
            cursor = conn.cursor()
            # Build the SQL query to filter by year and month
            sql_query = "SELECT * FROM financial_transaction"
            # Execute the query with the provided month and year
            cursor.execute(sql_query)
            records = cursor.fetchall()
            result = [row for row in records]
            conn.close()
            return result

        global data, user_input
        user_input = "!"
        data = fetch_data_from_db()

        def update_views():
            search_report_row_new = create_search_report(user_input, data)
            search_page.content.controls[2] = search_report_row_new
            search_page.update()
            self.page.update()

        def create_header():
            # Create two text buttons.
            header_text = Text("Tìm kiếm (toàn thời gian)", color="white")

            header = Container(
                # bgcolor="black",
                padding=padding.only(bottom=10),
                content=Row(
                    # alignment="spaceBetween",
                    controls=[
                        IconButton(
                            icons.ARROW_BACK,
                            icon_color="white",
                            on_click=lambda e: self.page.go("/calendar"),
                        ),
                        header_text,
                        # IconButton(icons.SEARCH, icon_color="white"),
                    ],
                ),
            )
            return header

        def create_search_textfield():
            def on_submit_search():
                global user_input
                user_input = text_field.controls[0].value
                update_views()

            text_field = Row(
                controls=[
                    TextField(
                        label="Nhập từ khóa",
                        on_blur=lambda e: on_submit_search(),
                    ),
                    IconButton(
                        icons.SEARCH,
                        icon_color="white",
                        on_click=lambda e: on_submit_search(),
                    ),
                ],
            )

            return text_field

        def create_search_report(user_input, data):
            result = []
            for item in data:
                for field in item:
                    if str(user_input).lower() in str(field).lower():
                        result.append(item)
                        break  # Once a match is found, move to the next item
            # print(result)
            money_expense = 0
            money_income = 0

            for item in result:
                if item[5] == "Tiền thu":
                    money_income += item[3]
                elif item[5] == "Tiền chi":
                    money_expense += item[3]

            money_total = money_income - money_expense

            income_container = Container(
                # padding=padding.only(left=20, right=20),
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Text("Tiền thu", weight="bold"),
                        Text(value=f"{money_income}", color="#50b4d1"),
                    ],
                ),
            )

            outcome_container = Container(
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Text("Tiền chi", weight="bold"),
                        Text(value=f"{'{:,}'.format(int(money_expense))}", color="red"),
                    ],
                )
            )

            total_container = Container(
                # padding=padding.only(left=20, right=20),
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Text("Tổng", weight="bold"),
                        Text(value=f"{'{:,}'.format(int(money_total))}"),
                    ],
                ),
            )

            if money_total > 0:
                total_container.content.controls[1].color = "#50b4d1"
            else:
                total_container.content.controls[1].color = "red"

            def create_report_row(date, category, note, amount):
                report_row = Column(
                    spacing=0,
                    controls=[
                        Divider(height=20, opacity=0),
                        Container(
                            padding=padding.only(top=2, bottom=2),
                            bgcolor="#313131",
                            content=Row(controls=[Text(date, color="white")]),
                        ),
                        Row(
                            alignment="spaceBetween",
                            controls=[
                                Text(category, color="white"),
                                Text(note, color="white"),
                                Text(amount, color="white"),
                            ],
                        ),
                    ],
                )
                return report_row

            def create_report_list(result):
                date_rows = {}
                for item in result:
                    date = item[1]
                    category = item[4]
                    note = item[2]
                    if item[5] == "Tiền chi":
                        amount = -item[3]
                    else:
                        amount = item[3]

                    if date not in date_rows:
                        date_rows[date] = create_report_row(
                            date, category, note, amount
                        )
                    else:
                        # Add the category, note, and amount to the existing date row.
                        date_rows[date].controls.append(
                            Row(
                                alignment="spaceBetween",
                                controls=[
                                    Text(category, color="white"),
                                    Text(note, color="white"),
                                    Text(amount, color="white"),
                                ],
                            )
                        )
                return list(date_rows.values())

            search_report_list_view = ListView(
                height=300,
                # width=340,
                # scroll='auto',
                spacing=1,
            )

            if len(result) > 0:
                result.sort(key=lambda x: x[1])
                search_report_list_view.controls.extend(create_report_list(result))

            search_report = Column(
                controls=[
                    Row(
                        alignment="spaceBetween",
                        controls=[
                            income_container,
                            outcome_container,
                            total_container,
                        ],
                    ),
                    search_report_list_view,
                ]
            )

            return search_report

        header = create_header()
        text_field_row = create_search_textfield()
        search_report_row = create_search_report(user_input, data)

        search_page = Container(
            width=400,
            height=712,
            border_radius=35,
            bgcolor=BG_COLOR,
            padding=padding.only(left=30, top=30, right=30),
            content=Column(
                # alignment="spaceBetween",
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[header, text_field_row, search_report_row],
            ),
        )

        return search_page
