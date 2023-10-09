import sqlite3
from flet import *
import flet as ft
import datetime



BG_COLOR = "#191919"
GREY_COLOR = "#3f3f3f"
PINK = "#eb06ff"


class Report_Year_Outcome(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def fetch_data_from_db(year=datetime.datetime.now().year):
            conn = sqlite3.connect("db/app.db")
            cursor = conn.cursor()

            # Extract the year and month from the input month
            # year = datetime.datetime.now().year

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
        # print(f"data is: {data}")

        def update_views():
            print("this is rp2")
            print(data)
           
            bieu_do_tron = create_bieudotron(data)
            thongke1 = create_thongke(data)
            
            page_3_child_container.content.controls[3] = bieu_do_tron
            page_3.content.controls[1] = thongke1
            page_3_child_container.update()
            page_3.update()
            self.page.update()

        def create_header():
            # Create a function to change the background color of the buttons.
            def change_button_colors(button_1: TextButton):
                button_1.style.bgcolor = GREY_COLOR
                header.update()

            # Create two text buttons.
            button_1 = Text(
                "Báo cáo danh mục trong năm", color="white"
            )

            # Add on_click event listeners to the buttons.
            button_1.on_click = lambda event: change_button_colors(button_1)

            # Add the buttons to the page.
            header = Row(
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
                button_1.style.bgcolor = PINK
                button_2.style.bgcolor = GREY_COLOR
                bieudo1.update()

            # Create two text buttons.
            button_1 = TextButton(
                text="Chi tiêu", 
                style=ButtonStyle(color="white",bgcolor=PINK),
                on_click= lambda e: (change_button_colors(button_1, button_2), self.page.go("/report_year_outcome")),
            )
            button_2 = TextButton(
                text="Thu nhập", 
                style=ButtonStyle(color="White"),
                on_click= lambda e: (change_button_colors(button_2, button_1), self.page.go("/report_year_income")),
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
            normal_title_style = ft.TextStyle(
                size=10, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
            )
            normal_title_style2 = ft.TextStyle(
                size=9, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
            )
            hover_title_style = ft.TextStyle(
                size=10,
                color=ft.colors.WHITE,
                weight=ft.FontWeight.BOLD,
                shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
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
                    sum(row[3] for row in month_data if row[4] == "Khác" and  row[5] == "Tiền chi")
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

            def on_chart_event(e: ft.PieChartEvent):
                for idx, section in enumerate(chart.sections):
                    if idx == e.section_index:
                        section.radius = hover_radius
                        section.title_style = hover_title_style
                    else:
                        section.radius = normal_radius
                        section.title_style = normal_title_style
                chart.update()

            chart = ft.PieChart(
                sections=[
                    ft.PieChartSection(
                        quanao,
                        title="Quần áo" + str(f"{quanao}") + "%",
                        title_style=normal_title_style2,
                        color=ft.colors.BLUE,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        tiennha,
                        title="Tiền nhà" + str(f"{tiennha}") + "%",
                        title_style=normal_title_style2,
                        color=ft.colors.YELLOW,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        tiendien,
                        title="Tiền điện" + str(f"{tiendien}") + "%",
                        title_style=normal_title_style2,
                        color=ft.colors.PURPLE,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        anuong,
                        title="Ăn uống" + str(f"{anuong}") + "%",
                        title_style=normal_title_style2,
                        color=ft.colors.GREEN,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        giadung,
                        title="Gia dụng" + str(f"{giadung}") + "%",
                        title_style=normal_title_style2,
                        color=ft.colors.RED,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        yte,
                        title="Y tế" + str(f"{yte}") + "%",
                        title_style=normal_title_style2,
                        color=ft.colors.ORANGE,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        giaoduc,
                        title="Giáo dục" + str(f"{giaoduc}") + "%",
                        title_style=normal_title_style2,
                        color=ft.colors.PINK,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        tiennuoc,
                        title="Tiền nước" + str(f"{tiennuoc}") + "%",
                        title_style=normal_title_style2,
                        color=ft.colors.BROWN,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        dilai,
                        title="Đi lại" + str(f"{dilai}") + "%",
                        title_style=normal_title_style2,
                        color=ft.colors.GREY,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        khac,
                        title="Khác" + str(f"{khac}") + "%",
                        title_style=normal_title_style2,
                        color=ft.colors.BLACK,
                        radius=normal_radius,
                    ),
                ],
                sections_space=0,
                center_space_radius=70,
                # size=ft.size(150, 150),
                on_chart_event=on_chart_event,
                expand=False,
            )
            return chart

        def create_thongke(year_data):
            thongke = ListView(
                height=150,
                width=340,
                # scroll='auto',
                spacing=1,
            )
            anuong = sum(row[3] for row in year_data if row[4] == "Ăn uống")
            quanao = sum(row[3] for row in year_data if row[4] == "Quần áo")
            tiennha = sum(row[3] for row in year_data if row[4] == "Tiền nhà")
            tiendien = sum(row[3] for row in year_data if row[4] == "Tiền điện")
            giadung = sum(row[3] for row in year_data if row[4] == "Gia dụng")
            yte = sum(row[3] for row in year_data if row[4] == "Y tế")
            giaoduc = sum(row[3] for row in year_data if row[4] == "Giáo dục")
            dilai = sum(row[3] for row in year_data if row[4] == "Đi lại")
            tiennuoc = sum(row[3] for row in year_data if row[4] == "Tiền nước")
            khac = sum(row[3] for row in year_data if row[4] == "Khác"and  row[5] == "Tiền chi")

            def create_thongke_row(category, icon, text, icon_color):
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

            thongke.controls.extend([
                    create_thongke_row(tiennha, icons.HOUSE, "Tiền nhà", "yellow"),
                    create_thongke_row(tiendien, icons.ELECTRIC_BOLT, "Tiền điện", "purple"),
                    create_thongke_row(quanao, icons.CHECKROOM, "Quần áo", "blue"),
                    create_thongke_row(anuong, icons.LOCAL_DINING, "Ăn uống", "green"),
                    create_thongke_row(giadung, icons.HOME_REPAIR_SERVICE, "Gia dụng", "red"),
                    create_thongke_row(yte, icons.EMERGENCY, "Y tế", "orange"),
                    create_thongke_row(giaoduc, icons.SCHOOL, "Giáo dục", "pink"),
                    create_thongke_row(dilai, icons.DIRECTIONS_BUS, "Đi lại", "grey"),
                    create_thongke_row(tiennuoc, icons.WATER_DROP, "Tiền nước", "brown"),
                    create_thongke_row(khac, icons.QUESTION_MARK, "Khác", "black"),
                ]
            )

            return thongke

        header = create_header()
        date_row = create_date()
        # chitieu_thunhap_thuchi = create_chitieu_thunhap_thuchi(data)
        bieu_do_label = create_bieudo_label()
        bieu_do_tron = create_bieudotron(data)
        thongke1 = create_thongke(data)
       

        page_3_child_container = Container(
            padding=padding.only(left=10, top=30, right=30),
            content=Column(
                controls=[
                    header,
                    date_row,
                    # chitieu_thunhap_thuchi,
                    bieu_do_label,
                    bieu_do_tron,
                ]
            ),
        )

        page_3 = Container(
            width=400,
            height=712,
            border_radius=35,
            bgcolor=BG_COLOR,
            content=Column(
                alignment="spaceBetween",
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    page_3_child_container,
                    thongke1,
                   
                ],
            ),
        )

        return page_3
