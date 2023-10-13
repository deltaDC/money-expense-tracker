import sqlite3
from flet import *
import datetime
from utils.navbar import create_navbar
from const import *


BG_COLOR = "#191919"
GREY_COLOR = "#3f3f3f"
PINK = "#eb06ff"


class Report_Outcome(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def fetch_data_from_db(
            year=datetime.datetime.now().year, month=datetime.datetime.now().month
        ):
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
        data = fetch_data_from_db(year=current_year, month=current_month)
        # print(f"data is: {data}")

        def update_views():
            # print(data)
            chitieu_thunhap_thuchi = create_chitieu_thunhap_thuchi(data)
            bieu_do_tron = create_bieudotron(data)
            thongke1 = create_thongke(data)
            # chitieu_thunhap_thuchi.update()
            # bieu_do_tron.update()
            # thongke1.update()
            page_3_child_container.content.controls[2] = chitieu_thunhap_thuchi
            page_3_child_container.content.controls[4] = bieu_do_tron
            page_3.content.controls[1] = thongke1
            page_3_child_container.update()
            page_3.update()
            self.page.update()

        def create_header():
            # Create two text buttons.
            header = Text("Báo cáo", color="white")

            # Add the buttons to the page.
            header = Row(
                alignment="spaceBetween",
                controls=[
                    Row(
                        controls=[
                            header,
                        ]
                    ),
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
                data = fetch_data_from_db(current_year, current_month)
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
                data = fetch_data_from_db(current_year, current_month)
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

        def create_chitieu_thunhap_thuchi(month_data):
            # Create two text buttons.
            button_1 = TextButton(
                text="Chi tiêu", style=ButtonStyle(color="White", bgcolor=GREY_COLOR)
            )
            button_2 = TextButton(
                text="Thu nhập", style=ButtonStyle(color="White", bgcolor=GREY_COLOR)
            )

            # Calculate and format the total expense and income from the data
            total_expense = sum(row[3] for row in month_data if row[5] == "Tiền chi")
            total_income = sum(row[3] for row in month_data if row[5] == "Tiền thu")

            chitieu_thunhap1 = Row(
                alignment="spaceBetween",
                controls=[
                    Container(
                        width=168,
                        height=30,
                        border_radius=5,
                        bgcolor=GREY_COLOR,
                        padding=1,
                        content=Row(
                            alignment="spaceBetween",
                            controls=[
                                button_1,
                                Text(f"{total_expense} đ", color="white"),
                            ],
                        ),
                    ),
                    Container(
                        width=168,
                        height=30,
                        border_radius=5,
                        bgcolor=GREY_COLOR,
                        padding=1,
                        content=Row(
                            alignment="spaceBetween",
                            controls=[
                                button_2,
                                Text(f"{total_income} đ", color="white"),
                            ],
                        ),
                    ),
                ],
            )

            def change_button_colors1(button_3: TextButton):
                button_3.style.bgcolor = GREY_COLOR
                thu_chi1.update()

            # Create two text buttons.
            button_3 = TextButton(
                text="Thu chi", style=ButtonStyle(color="White", bgcolor=GREY_COLOR)
            )

            # Add on_click event listeners to the buttons.
            button_3.on_click = lambda event: change_button_colors1(button_3)

            thu_chi1 = Row(
                controls=[
                    Container(
                        width=340,
                        height=30,
                        border_radius=5,
                        bgcolor=GREY_COLOR,
                        padding=1,
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
            chitieuthunhapthuchi = Column(
                controls=[
                    chitieu_thunhap1,
                    thu_chi1,
                ]
            )
            return chitieuthunhapthuchi

        def create_bieudo_label():
            def change_button_colors(button_1: TextButton, button_2: TextButton):
                button_1.style.bgcolor = PINK
                button_2.style.bgcolor = GREY_COLOR
                bieudo1.update()

            # Create two text buttons.
            button_1 = TextButton(
                text="Chi tiêu",
                style=ButtonStyle(color="white", bgcolor=PINK),
                on_click=lambda e: (
                    change_button_colors(button_1, button_2),
                    self.page.go("/report_outcome"),
                ),
            )
            button_2 = TextButton(
                text="Thu nhập",
                style=ButtonStyle(color="White"),
                on_click=lambda e: (
                    change_button_colors(button_2, button_1),
                    self.page.go("/report_income"),
                ),
            )

            # Add on_click event listeners to the buttons.
            # button_1.on_click = lambda event: change_button_colors(button_1, button_2)
            # button_2.on_click = lambda event: change_button_colors(button_2, button_1)
            bieudo1 = Column(
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
                        content=Container(
                            bgcolor=PINK,
                        ),
                    ),
                ]
            )

            return bieudo1

        def create_bieudotron(month_data):
            normal_radius = 50
            hover_radius = 60
            normal_title_style = TextStyle(
                size=10, color=colors.WHITE, weight=FontWeight.BOLD
            )
            normal_title_style2 = TextStyle(
                size=9, color=colors.WHITE, weight=FontWeight.BOLD
            )
            hover_title_style = TextStyle(
                size=10,
                color=colors.WHITE,
                weight=FontWeight.BOLD,
                shadow=BoxShadow(blur_radius=2, color=colors.BLACK54),
            )
            total_expense = sum(row[3] for row in month_data if row[5] == "Tiền chi")
            if total_expense != 0:
                anuong = "{:.2f}".format(
                    sum(row[3] for row in month_data if row[4] == "Ăn uống")
                    / total_expense
                    * 100
                )
                quanao = "{:.2f}".format(
                    sum(row[3] for row in month_data if row[4] == "Quần áo")
                    / total_expense
                    * 100
                )
                tiennha = "{:.2f}".format(
                    sum(row[3] for row in month_data if row[4] == "Tiền nhà")
                    / total_expense
                    * 100
                )
                tiendien = "{:.2f}".format(
                    sum(row[3] for row in month_data if row[4] == "Tiền điện")
                    / total_expense
                    * 100
                )
                giadung = "{:.2f}".format(
                    sum(row[3] for row in month_data if row[4] == "Gia dụng")
                    / total_expense
                    * 100
                )
                yte = "{:.2f}".format(
                    sum(row[3] for row in month_data if row[4] == "Y tế")
                    / total_expense
                    * 100
                )
                giaoduc = "{:.2f}".format(
                    sum(row[3] for row in month_data if row[4] == "Giáo dục")
                    / total_expense
                    * 100
                )
                dilai = "{:.2f}".format(
                    sum(row[3] for row in month_data if row[4] == "Đi lại")
                    / total_expense
                    * 100
                )
                tiennuoc = "{:.2f}".format(
                    sum(row[3] for row in month_data if row[4] == "Tiền nước")
                    / total_expense
                    * 100
                )
                khac = "{:.2f}".format(
                    sum(
                        row[3]
                        for row in month_data
                        if row[4] == "Khác" and row[5] == "Tiền chi"
                    )
                    / total_expense
                    * 100
                )
            else:
                anuong = (
                    quanao
                ) = (
                    tiennha
                ) = (
                    tiendien
                ) = giadung = yte = giaoduc = dilai = tiennuoc = khac = "0.00"

            def on_chart_event(e: PieChartEvent):
                for idx, section in enumerate(chart.sections):
                    if idx == e.section_index:
                        section.radius = hover_radius
                        section.title_style = hover_title_style
                    else:
                        section.radius = normal_radius
                        section.title_style = normal_title_style
                chart.update()

            chart = PieChart(
                sections=[
                    PieChartSection(
                        quanao,
                        title="Quần áo" + str(f"{quanao}") + "%",
                        title_style=normal_title_style2,
                        color=colors.BLUE,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        tiennha,
                        title="Tiền nhà" + str(f"{tiennha}") + "%",
                        title_style=normal_title_style2,
                        color=colors.YELLOW,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        tiendien,
                        title="Tiền điện" + str(f"{tiendien}") + "%",
                        title_style=normal_title_style2,
                        color=colors.PURPLE,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        anuong,
                        title="Ăn uống" + str(f"{anuong}") + "%",
                        title_style=normal_title_style2,
                        color=colors.GREEN,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        giadung,
                        title="Gia dụng" + str(f"{giadung}") + "%",
                        title_style=normal_title_style2,
                        color=colors.RED,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        yte,
                        title="Y tế" + str(f"{yte}") + "%",
                        title_style=normal_title_style2,
                        color=colors.ORANGE,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        giaoduc,
                        title="Giáo dục" + str(f"{giaoduc}") + "%",
                        title_style=normal_title_style2,
                        color=colors.PINK,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        tiennuoc,
                        title="Tiền nước" + str(f"{tiennuoc}") + "%",
                        title_style=normal_title_style2,
                        color=colors.BROWN,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        dilai,
                        title="Đi lại" + str(f"{dilai}") + "%",
                        title_style=normal_title_style2,
                        color=colors.GREY,
                        radius=normal_radius,
                    ),
                    PieChartSection(
                        khac,
                        title="Khác" + str(f"{khac}") + "%",
                        title_style=normal_title_style2,
                        color=colors.BLACK,
                        radius=normal_radius,
                    ),
                ],
                sections_space=0,
                center_space_radius=70,
                # size=size(150, 150),
                on_chart_event=on_chart_event,
                expand=False,
            )
            return chart

        def create_thongke(month_data):
            thongke = ListView(
                height=65,
                width=340,
                # scroll='auto',
                spacing=1,
            )
            anuong = sum(row[3] for row in month_data if row[4] == "Ăn uống")
            quanao = sum(row[3] for row in month_data if row[4] == "Quần áo")
            tiennha = sum(row[3] for row in month_data if row[4] == "Tiền nhà")
            tiendien = sum(row[3] for row in month_data if row[4] == "Tiền điện")
            giadung = sum(row[3] for row in month_data if row[4] == "Gia dụng")
            yte = sum(row[3] for row in month_data if row[4] == "Y tế")
            giaoduc = sum(row[3] for row in month_data if row[4] == "Giáo dục")
            dilai = sum(row[3] for row in month_data if row[4] == "Đi lại")
            tiennuoc = sum(row[3] for row in month_data if row[4] == "Tiền nước")
            khac = sum(
                row[3]
                for row in month_data
                if row[4] == "Khác" and row[5] == "Tiền chi"
            )

            def create_thongke_row(category, icon, text, icon_color):
                thongke_row = Container(
                    width=340,
                    height=21,
                    border_radius=5,
                    bgcolor=GREY_COLOR,
                    padding=1,
                    content=Row(
                        alignment="spaceBetween",
                        controls=[
                            Row(
                                alignment="start",
                                controls=[
                                    Icon(name=icon, color=icon_color),
                                    Text(text, color="white"),
                                ],
                            ),
                            Row(
                                alignment="end",
                                controls=[
                                    Text(f"{category}", color="white"),
                                    Text("đ", color="white"),
                                ],
                            ),
                        ],
                    ),
                )
                return thongke_row

            thongke.controls.extend(
                [
                    create_thongke_row(tiennha, icons.HOUSE, "Tiền nhà", "yellow"),
                    create_thongke_row(
                        tiendien, icons.ELECTRIC_BOLT, "Tiền điện", "purple"
                    ),
                    create_thongke_row(quanao, icons.CHECKROOM, "Quần áo", "blue"),
                    create_thongke_row(anuong, icons.LOCAL_DINING, "Ăn uống", "green"),
                    create_thongke_row(
                        giadung, icons.HOME_REPAIR_SERVICE, "Gia dụng", "red"
                    ),
                    create_thongke_row(yte, icons.EMERGENCY, "Y tế", "orange"),
                    create_thongke_row(giaoduc, icons.SCHOOL, "Giáo dục", "pink"),
                    create_thongke_row(dilai, icons.DIRECTIONS_BUS, "Đi lại", "grey"),
                    create_thongke_row(
                        tiennuoc, icons.WATER_DROP, "Tiền nước", "brown"
                    ),
                    create_thongke_row(khac, icons.QUESTION_MARK, "Khác", "black"),
                ]
            )

            return thongke

        header = create_header()
        date_row = create_date()
        chitieu_thunhap_thuchi = create_chitieu_thunhap_thuchi(data)
        bieu_do_label = create_bieudo_label()
        bieu_do_tron = create_bieudotron(data)
        thongke1 = create_thongke(data)
        navbar = create_navbar(self.page, 2)

        page_3_child_container = Container(
            padding=padding.only(left=30, top=30, right=30),
            content=Column(
                controls=[
                    header,
                    date_row,
                    chitieu_thunhap_thuchi,
                    bieu_do_label,
                    bieu_do_tron,
                ]
            ),
        )

        page_3 = Container(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            border_radius=35,
            bgcolor=BG_COLOR,
            content=Column(
                alignment="spaceBetween",
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    page_3_child_container,
                    thongke1,
                    navbar,
                ],
            ),
        )

        return page_3
