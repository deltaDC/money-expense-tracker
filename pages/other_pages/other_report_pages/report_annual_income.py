import sqlite3
from flet import *
import flet as ft
import datetime


BG_COLOR = "#191919"
GREY_COLOR = "#3f3f3f"
PINK = "#eb06ff"
BLUE = "#0077b6"


class Report_During_The_Year_Income(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def fetch_data_from_db(year=datetime.datetime.now().year):
            conn = sqlite3.connect("db/app.db")
            cursor = conn.cursor()
            # Build the SQL query to filter by year and month
            sql_query = (
                "SELECT * FROM financial_transaction WHERE strftime('%Y', date) = ?"
            )
            # Execute the query with the provided month and year
            cursor.execute(sql_query, (f"{year}",))
            records = cursor.fetchall()
            result = [row for row in records]
            conn.close()
            return result

        global current_month, current_year, data
        current_month = datetime.date.today().month
        current_year = datetime.date.today().year
        data = fetch_data_from_db(year=current_year)
        # data = fetch_data_from_db()

        def update_views():
            print("this is baocaotrongnam")
            print(data)
            # chitieu_thunhap_thuchi = create_chitieu_thunhap_thuchi(data)
            bieu_do_cot = create_bieudocot(data)
            thongke1 = create_thongke(data)
            # chitieu_thunhap_thuchi.update()
            # bieu_do_tron.update()
            # thongke1.update()
            # page_3_child_container.content.controls[2] = chitieu_thunhap_thuchi
            baocaotrongnam.content.controls[3] = bieu_do_cot
            baocaotrongnam.content.controls[4] = thongke1
            baocaotrongnam.update()
            self.page.update()

        def create_header():
            # Create a function to change the background color of the buttons.
            def change_button_colors(button_1: TextButton):
                button_1.style.bgcolor = GREY_COLOR
                header.update()

            # Create two text buttons.
            button_1 = Text("Báo cáo trong năm", color="white")

            # Add on_click event listeners to the buttons.
            button_1.on_click = lambda event: change_button_colors(button_1)

            # Add the buttons to the page.
            header = Row(
                alignment="spaceBetween",
                controls=[
                    IconButton(
                        icons.ARROW_BACK,
                        icon_color="white",
                        on_click=lambda e: self.page.go("/other"),
                    ),
                    button_1,
                    IconButton(icons.ACCESS_TIME, icon_color="white"),
                ],
            )
            return header

        def create_date():
            def update_date_display():
                # Định dạng tháng với số 0 trước nếu nhỏ hơn 10
                # formatted_month = str(current_month).zfill(2)
                # Cập nhật ngày tháng trên giao diện
                date_header.controls[0].value = f"{current_year}"
                date_header.update()

            def get_next_year():
                global  current_year, data
                # Tăng tháng
                current_year += 1

                # Nếu tháng là 13, thì tăng năm và đặt lại tháng về 1
                # if current_month > 12:
                #     current_month = 1
                #     current_year += 1
                data = fetch_data_from_db(current_year)
                # print(data)
                update_date_display()
                update_views()

            def get_prev_year():
                global current_year, data
                # Giảm tháng
                current_year -= 1

                # Nếu tháng là 0, thì giảm năm và đặt lại tháng về 12
                # if current_month < 1:
                #     current_month = 12
                #     current_year -= 1
                data = fetch_data_from_db(current_year)
                # print(data)
                update_date_display()
                update_views()

            # Create a row to represent the date header.
            date_header = Row(
                alignment="spaceBetween",
                controls=[
                    # Create a text widget to display the month/year.
                    Text(datetime.date.today().strftime("%Y"), color="white"),
                    # Create a row to contain the arrow buttons.
                    Row(
                        controls=[
                            # Create an icon button for the previous arrow.
                            IconButton(
                                icons.ARROW_LEFT,
                                icon_color="white",
                                on_click=lambda event: get_prev_year(),
                            ),
                            # Create an icon button for the next arrow.
                            IconButton(
                                icons.ARROW_RIGHT,
                                icon_color="white",
                                on_click=lambda event: get_next_year(),
                            ),
                        ]
                    ),
                ],
            )

            return date_header

        def create_bieudo_label():
            def change_button_colors(button_1: TextButton, button_2: TextButton):
                button_1.style.bgcolor = GREY_COLOR
                button_2.style.bgcolor = BG_COLOR
                # button_3.style.bgcolor = BLUE
                bieudo.update()

            button_1 = TextButton(
                text="Chi tiêu",
                style=ButtonStyle(color="white", ),
                on_click=lambda e: (
                    change_button_colors(button_1, button_2),
                    self.page.go("/report_annual_expense"),
                ),
            )
            button_2 = TextButton(
                text="Thu nhập",
                style=ButtonStyle(color="white",bgcolor=GREY_COLOR),
                on_click=lambda e: (
                    change_button_colors(button_2, button_1),
                    self.page.go("/report_annual_income"),
                ),
            )
            # button_3 = TextButton(
            #     text="Tổng", style=ButtonStyle(color="white", bgcolor=GREY_COLOR)
            # )

            bieudo = Column(
                alignment=MainAxisAlignment.START,
                controls=[
                    Row(
                        alignment="spaceAround",
                        controls=[
                            # Text('Chi tiêu'),
                            # Text('Thu nhập'),
                            button_1,
                            button_2,
                        ],
                    ),
                    Container(
                        width=450,
                        height=5,
                        border_radius=5,
                        bgcolor="white12",
                        padding=padding.only(right=170),
                        # content=Container(
                        #     bgcolor=PINK,
                        # ),
                    ),
                ],
            )

            return bieudo

        def create_bieudocot(data):
            total_expense = sum(row[3] for row in data if row[5] == "Tiền chi")
            total_income = sum(row[3] for row in data if row[5] == "Tiền thu")

            def create_money(x, res):
                month = "{:.2f}".format(
                    sum(
                        row[3]
                        for row in data
                        if int(row[1][5:7]) == x and row[5] == "Tiền thu"
                    )
                    / res
                    * 100
                )
                return month

            if total_income != 0:
                thang1_income = str(create_money(1, total_income))
                thang2_income = str(create_money(2, total_income))
                thang3_income = str(create_money(3, total_income))
                thang4_income = str(create_money(4, total_income))
                thang5_income = str(create_money(5, total_income))
                thang6_income = str(create_money(6, total_income))
                thang7_income = str(create_money(7, total_income))
                thang8_income = str(create_money(8, total_income))
                thang9_income = str(create_money(9, total_income))
                thang10_income = str(create_money(10, total_income))
                thang11_income = str(create_money(11, total_income))
                thang12_income = str(create_money(12, total_income))
            else:
                thang1_income = (
                    thang2_income
                ) = (
                    thang3_income
                ) = (
                    thang4_income
                ) = (
                    thang5_income
                ) = (
                    thang6_income
                ) = (
                    thang7_income
                ) = (
                    thang8_income
                ) = (
                    thang9_income
                ) = thang10_income = thang11_income = thang12_income = "0.00"

            chart = ft.BarChart(
                bar_groups=[
                    ft.BarChartGroup(
                        x=0,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=f"{thang1_income}",
                                width=10,
                                color=ft.colors.BLUE,
                                tooltip="Tháng 1",
                                border_radius=0,
                            )
                        ],
                    ),
                    ft.BarChartGroup(
                        x=1,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=f"{thang2_income}",
                                width=10,
                                color=ft.colors.BLUE,
                                tooltip="Tháng 2",
                                border_radius=0,
                            )
                        ],
                    ),
                    ft.BarChartGroup(
                        x=2,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=f"{thang3_income}",
                                width=10,
                                color=ft.colors.BLUE,
                                tooltip="Tháng 3",
                                border_radius=0,
                            )
                        ],
                    ),
                    ft.BarChartGroup(
                        x=3,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=f"{thang4_income}",
                                width=10,
                                color=ft.colors.BLUE,
                                tooltip="Tháng 4",
                                border_radius=0,
                            )
                        ],
                    ),
                    ft.BarChartGroup(
                        x=4,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=f"{thang5_income}",
                                width=10,
                                color=ft.colors.BLUE,
                                tooltip="Tháng 5",
                                border_radius=0,
                            )
                        ],
                    ),
                    ft.BarChartGroup(
                        x=5,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=f"{thang6_income}",
                                width=10,
                                color=ft.colors.BLUE,
                                tooltip="Tháng 6",
                                border_radius=0,
                            )
                        ],
                    ),
                    ft.BarChartGroup(
                        x=6,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=f"{thang7_income}",
                                width=10,
                                color=ft.colors.BLUE,
                                tooltip="Tháng 7",
                                border_radius=0,
                            )
                        ],
                    ),
                    ft.BarChartGroup(
                        x=7,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=f"{thang8_income}",
                                width=10,
                                color=ft.colors.BLUE,
                                tooltip="Tháng 8",
                                border_radius=0,
                            )
                        ],
                    ),
                    ft.BarChartGroup(
                        x=8,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=f"{thang9_income}",
                                width=10,
                                color=ft.colors.BLUE,
                                tooltip="Tháng 9",
                                border_radius=0,
                            )
                        ],
                    ),
                    ft.BarChartGroup(
                        x=9,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=f"{thang10_income}",
                                width=10,
                                color=ft.colors.BLUE,
                                tooltip="Tháng 10",
                                border_radius=0,
                            )
                        ],
                    ),
                    ft.BarChartGroup(
                        x=10,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=f"{thang11_income}",
                                width=10,
                                color=ft.colors.BLUE,
                                tooltip="Tháng 11",
                                border_radius=0,
                            )
                        ],
                    ),
                    ft.BarChartGroup(
                        x=11,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=f"{thang12_income}",
                                width=10,
                                color=ft.colors.BLUE,
                                tooltip="Tháng 12",
                                border_radius=0,
                            )
                        ],
                    ),
                ],
                border=ft.border.all(1, ft.colors.GREY_400),
                bottom_axis=ft.ChartAxis(
                    labels=[
                        ft.ChartAxisLabel(
                            value=0,
                            label=ft.Container(ft.Text("T1"), padding=2),
                        ),
                        ft.ChartAxisLabel(
                            value=1,
                            label=ft.Container(ft.Text("T2"), padding=2),
                        ),
                        ft.ChartAxisLabel(
                            value=2,
                            label=ft.Container(ft.Text("T3"), padding=2),
                        ),
                        ft.ChartAxisLabel(
                            value=3,
                            label=ft.Container(ft.Text("T4"), padding=2),
                        ),
                        ft.ChartAxisLabel(
                            value=4,
                            label=ft.Container(ft.Text("T5"), padding=2),
                        ),
                        ft.ChartAxisLabel(
                            value=5,
                            label=ft.Container(ft.Text("T6"), padding=2),
                        ),
                        ft.ChartAxisLabel(
                            value=6,
                            label=ft.Container(ft.Text("T7"), padding=2),
                        ),
                        ft.ChartAxisLabel(
                            value=7,
                            label=ft.Container(ft.Text("T8"), padding=2),
                        ),
                        ft.ChartAxisLabel(
                            value=8,
                            label=ft.Container(ft.Text("T9"), padding=2),
                        ),
                        ft.ChartAxisLabel(
                            value=9,
                            label=ft.Container(ft.Text("T10"), padding=2),
                        ),
                        ft.ChartAxisLabel(
                            value=10,
                            label=ft.Container(ft.Text("T11"), padding=2),
                        ),
                        ft.ChartAxisLabel(
                            value=11,
                            label=ft.Container(ft.Text("T12"), padding=2),
                        ),
                    ],
                    labels_size=20,
                ),
                left_axis=ft.ChartAxis(
                    labels=[
                    ft.ChartAxisLabel(value=20, label=ft.Text("2")),  
                    ft.ChartAxisLabel(value=40, label=ft.Text("4")),
                    ft.ChartAxisLabel(value=60, label=ft.Text("6")), 
                    ft.ChartAxisLabel(value=80, label=ft.Text("8")),
                    ft.ChartAxisLabel(value=100, label=ft.Text("10"))
                    ],
                ),
                horizontal_grid_lines=ft.ChartGridLines(
                    color=ft.colors.GREY_300, width=1, dash_pattern=[3, 3]
                ),
                tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_300),
                max_y=110,
                interactive=True,
                expand=False,
            )
            return chart

        def create_thongke(data):
            thongke = ListView(
                height=150,
                width=340,
                # scroll='auto',
                spacing=1,
            )

            def create_money(x):
                money = "{:.2f}".format(
                    sum(row[3] for row in data if int(row[1][5:7]) == x and row[5] == "Tiền thu")
                )
                return money

            thang1 = create_money(1)
            thang2 = create_money(2)
            thang3 = create_money(3)
            thang4 = create_money(4)
            thang5 = create_money(5)
            thang6 = create_money(6)
            thang7 = create_money(7)
            thang8 = create_money(8)
            thang9 = create_money(9)
            thang10 = create_money(10)
            thang11 = create_money(11)
            thang12 = create_money(12)

            def create_thongke_row(month, money):
                thongke_row = Container(
                    width=340,
                    height=35,
                    border_radius=5,
                    bgcolor=GREY_COLOR,
                    padding=5,
                    content=Row(
                        alignment="spaceBetween",
                        controls=[
                            Row(
                                alignment="start",
                                controls=[
                                    Text(month, color="white"),
                                ],
                            ),
                            Row(
                                alignment="end",
                                controls=[
                                    Text(f"{money}", color="white"),
                                    Text("đ", color="white"),
                                ],
                            ),
                        ],
                    ),
                )
                return thongke_row

            thongke.controls.extend(
                [
                    create_thongke_row("Tháng 1", thang1),
                    create_thongke_row("Tháng 2", thang2),
                    create_thongke_row("Tháng 3", thang3),
                    create_thongke_row("Tháng 4", thang4),
                    create_thongke_row("Tháng 5", thang5),
                    create_thongke_row("Tháng 6", thang6),
                    create_thongke_row("Tháng 7", thang7),
                    create_thongke_row("Tháng 8", thang8),
                    create_thongke_row("Tháng 9", thang9),
                    create_thongke_row("Tháng 10", thang10),
                    create_thongke_row("Tháng 11", thang11),
                    create_thongke_row("Tháng 12", thang12),
                ]
            )

            return thongke

        header = create_header()
        date_row = create_date()
        bieudo_label = create_bieudo_label()
        bieu_do_cot = create_bieudocot(data)
        statistical = create_thongke(data)

        baocaotrongnam = Container(
            width=400,
            height=712,
            border_radius=35,
            bgcolor=BG_COLOR,
            padding=padding.only(left=30, top=30, right=30),
            content=Column(
                # alignment="spaceBetween",
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[header, date_row, bieudo_label, bieu_do_cot, statistical],
            ),
        )

        return baocaotrongnam
