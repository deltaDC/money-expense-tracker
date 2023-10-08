import sqlite3
from flet import *
import datetime
import calendar
from utils.navbar import create_navbar


BG_COLOR = "#191919"
GREY_COLOR = "#3f3f3f"
PINK = "#eb06ff"


class Calendar(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def fetch_data_from_db(year = datetime.datetime.now().year,month=datetime.datetime.now().month):
            conn = sqlite3.connect("db/app.db")
            cursor = conn.cursor()

            # Extract the year and month from the input month
            

            # Build the SQL query to filter by year and month
            sql_query = (
                "SELECT * FROM financial_transaction WHERE strftime('%Y-%m', date) = ?"
            )

            # Execute the query with the provided month and year
            cursor.execute(sql_query, (f"{year:04}-{month:02}",))

            records = cursor.fetchall()
            result = [row for row in records]
            conn.close()
            return result

        global current_month, current_year, data
        current_month = datetime.date.today().month
        current_year = datetime.date.today().year
        data = fetch_data_from_db(year=current_year,month=current_month)

        def update_views():
            print(data)
            calendar_new_UI = creat_calendar(data)
            month_new_report = create_month_report(data)
            calendar_page_child_container.content.controls[2] = calendar_new_UI
            # calendar_page_child_container.content.controls[3] = month_new_report
            calendar_page.content.controls[1] = month_new_report
            calendar_page_child_container.update()
            calendar_page.update()
            self.page.update()

        def create_header():
            # Create a function to change the background color of the buttons.
            def change_button_colors(button_1: TextButton):
                button_1.style.bgcolor = GREY_COLOR
                header.update()

            # Create two text buttons.
            button_1 = Text(
                "Lịch", color="white"
            )

            # Add on_click event listeners to the buttons.
            button_1.on_click = lambda event: change_button_colors(button_1)

            # Add the buttons to the page.
            header = Row(
                alignment="spaceBetween",
                controls=[
                    Row(
                        controls=[
                            button_1,
                            # button_2,
                        ]
                    ),
                    # Icon(icons.SEARCH),
                    IconButton(icons.SEARCH, icon_color="white"),
                ],
            )
            return header

        def create_date():
            def update_date_display():
                # Định dạng tháng với số 0 trước nếu nhỏ hơn 10
                formatted_month = str(current_month).zfill(2)
                formatted_year = str(current_year).zfill(4)
                # Cập nhật ngày tháng trên giao diện
                date_header.controls[0].value = f"{formatted_month}/{formatted_year}"
                date_header.update()

            def get_next_month():
                global current_month, current_year, data
                # Tăng tháng
                current_month += 1

                # Nếu tháng là 13, thì tăng năm và đặt lại tháng về 1
                if current_month > 12:
                    current_month = 1
                    current_year += 1
                data = fetch_data_from_db(current_year,current_month)
                # print(data)
                update_date_display()
                update_views()

            def get_prev_month():
                global current_month, current_year, data
                # Giảm tháng
                current_month -= 1

                # Nếu tháng là 0, thì giảm năm và đặt lại tháng về 12
                if current_month < 1:
                    current_month = 12
                    current_year -= 1
                data = fetch_data_from_db(current_year,current_month)
                # print(data)
                update_date_display()
                update_views()

            # Create a row to represent the date header.
            date_header = Row(
                alignment="spaceBetween",
                controls=[
                    # Create a text widget to display the month/year.
                    Text(datetime.date.today().strftime("%m/%Y"), color="white"),
                    # Create a row to contain the arrow buttons.
                    Row(
                        controls=[
                            # Create an icon button for the previous arrow.
                            IconButton(
                                icons.ARROW_LEFT,
                                icon_color="white",
                                on_click=lambda event: get_prev_month(),
                            ),
                            # Create an icon button for the next arrow.
                            IconButton(
                                icons.ARROW_RIGHT,
                                icon_color="white",
                                on_click=lambda event: get_next_month(),
                            ),
                        ]
                    ),
                ],
            )

            return date_header

        def creat_calendar(data):
            num_days = calendar.monthrange(current_year, current_month)[1]

            # Create a GridView widget with 7 rows and 7 columns.
            calendar_UI = GridView(
                runs_count=5, 
                max_extent=60, 
                child_aspect_ratio=0.8, 
                spacing=0, 
                run_spacing=0,
            )

            def on_day_widget_click(day):
                day_income_report_list = []
                day_outcome_report_list = []
                for record in data:
                    if int(record[1][-2:]) == day:
                        if record[5] == "Tiền chi":
                            day_outcome_report_list.append(f"{record[4]} {record[3]} `{record[2]}`")
                        elif record[5] == "Tiền thu":
                            day_income_report_list.append(f"{record[4]} {record[3]} `{record[2]}`")

                day_income_report_text = "\n ".join(day_income_report_list)
                day_outcome_report_text = "\n ".join(day_outcome_report_list)

                report_text = f"TIỀN THU:\n {day_income_report_text}\nTIỀN CHI:\n {day_outcome_report_text}"

                dlg = AlertDialog(
                    title=Text(f"Báo cáo ngày {day}/{current_month}/{current_year}"), 
                    content=Text(report_text),
                    on_dismiss=lambda e: print("Dialog dismissed!")
                )
                def open_dlg():
                    self.page.dialog = dlg
                    dlg.open = True
                    self.page.update()
                open_dlg()

            # Create a child widget for each day of the calendar_UI.
            for day in range(1, num_days + 1):
                day_widget = Container(
                    border=border.all(0.5, "white24"),
                    alignment=alignment.top_left,
                    padding=2,
                    content=Column(
                        controls=[
                            Text(str(day), size=12),
                        ]
                    ),
                    on_click= lambda e, day=day: on_day_widget_click(day)
                )
                one_day_income_money = 0
                one_day_outcome_money = 0

                for record in data:
                    if int(record[1][-2:]) == day:
                        if record[5] == "Tiền chi":
                            one_day_outcome_money += record[3]
                        elif record[5] == "Tiền thu":
                            one_day_income_money += record[3]


                if one_day_income_money > 0:
                    day_widget.content.controls.append(
                        Text(f"{'{:,}'.format(int(one_day_income_money))}", size=9, color="#50b4d1")
                    )
                if one_day_outcome_money > 0:
                    day_widget.content.controls.append(
                        Text(f"{'{:,}'.format(int(one_day_outcome_money))}", size=9, color="red")
                    )
                
                calendar_UI.controls.append(day_widget)

            return calendar_UI

        def create_month_report(data):
            month_income = 0
            month_outcome = 0
            for record in data:
                if record[5] == "Tiền chi":
                    month_outcome += record[3]
                elif record[5] == "Tiền thu":
                    month_income += record[3]
            
            month_total = month_income - month_outcome


            income_container = Container(
                padding=padding.only(left=20, right=20),
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Text("Tiền thu", weight="bold"),
                        Text(value=f"{month_income}", color="#50b4d1")
                    ]
                )
            )

            outcome_container = Container(
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Text("Tiền chi", weight="bold"),
                        Text(value=f"{'{:,}'.format(int(month_outcome))}", color="red")
                    ]
                )
            )

            total_container = Container(
                padding=padding.only(left=20, right=20),
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Text("Tổng", weight="bold"),
                        Text(value=f"{'{:,}'.format(int(month_total))}")
                    ]
                )
            )

            if month_total > 0:
                total_container.content.controls[1].color = "#50b4d1"
            else:
                total_container.content.controls[1].color = "red"


            month_report = Row(
                alignment="spaceBetween",
                controls=[
                    income_container, 
                    outcome_container, 
                    total_container
                ]
            )

            return month_report

        header = create_header()
        date_row = create_date()
        calendar_row = creat_calendar(data)
        month_report_row = create_month_report(data)
        navbar = create_navbar(self.page, 1)

        calendar_page_child_container = Container(
            padding=padding.only(left=30, top=30, right=30),
            content=Column(
                controls=[
                    header,
                    date_row,
                    calendar_row,
                ]
            ),
        )

        calendar_page = Container(
            width=400,
            height=712,
            border_radius=35,
            bgcolor=BG_COLOR,
            content=Column(
                alignment="spaceBetween",
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    calendar_page_child_container,
                    month_report_row,
                    navbar,
                ],
            ),
        )

        return calendar_page

