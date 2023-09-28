import sqlite3
from flet import *
import flet as ft
import datetime
from utils.navbar import create_navbar


BG_COLOR = "#191919"
GREY_COLOR = "#3f3f3f"
PINK = "#eb06ff"


class Report(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def create_header():
            # Create a function to change the background color of the buttons.
            def change_button_colors(button_1: TextButton):
                button_1.style.bgcolor = GREY_COLOR
                header.update()

            # Create two text buttons.
            button_1 = TextButton(
                text="Báo cáo", style=ButtonStyle(color="White", bgcolor=GREY_COLOR)
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
                    IconButton(
                        icons.SEARCH,
                    ),
                ],
            )
            return header

        def create_date():
            today = datetime.date.today()
            current_month = today.month
            current_year = today.year

            def update_date_display():
        # Định dạng tháng với số 0 trước nếu nhỏ hơn 10
                formatted_month = str(current_month).zfill(2)
        # Cập nhật ngày tháng trên giao diện
                date_header.controls[0].value = f"{formatted_month}/{current_year}"
                date_header.update()

            def get_next_month():
                nonlocal current_month, current_year
                # Tăng tháng
                current_month += 1
                # Nếu tháng là 13, thì tăng năm và đặt lại tháng về 1
                if current_month > 12:
                    current_month = 1
                    current_year += 1
                update_date_display()

            def get_prev_month():
                nonlocal current_month, current_year
                # Giảm tháng
                current_month -= 1
                # Nếu tháng là 0, thì giảm năm và đặt lại tháng về 12
                if current_month < 1:
                    current_month = 12
                    current_year -= 1
                update_date_display()

            def get_prev_month():
                nonlocal current_month, current_year
                # Giảm tháng
                current_month -= 1
                # Nếu tháng là 0, thì giảm năm và đặt lại tháng về 12
                if current_month < 1:
                    current_month = 12
                    current_year -= 1
                update_date_display()

            # Create a row to represent the date header.
            date_header = Row(
                alignment="spaceBetween",
                controls=[
                    # Create a text widget to display the month/year.
                    Text(datetime.date.today().strftime("%m/%Y")),
                    # Create a row to contain the arrow buttons.
                    Row(
                        controls=[
                            # Create an icon button for the previous arrow.
                            IconButton(
                                icons.ARROW_LEFT,
                                on_click=lambda event: get_prev_month(),
                            ),
                            # Create an icon button for the next arrow.
                            IconButton(
                                icons.ARROW_RIGHT,
                                on_click=lambda event: get_next_month(),
                            ),
                        ]
                    ),
                ],
            )

            return date_header

        def fetch_data_from_db():
            conn = sqlite3.connect('db/app.db')
            cursor = conn.cursor()

           # Thực hiện truy vấn SQL
            cursor.execute("SELECT * FROM financial_transaction")
            records = cursor.fetchall()
            result = [row for row in records]
            conn.close()
            return result


        def create_chitieu_thunhap_thuchi():
            # Lấy dữ liệu từ cơ sở dữ liệu
            data = fetch_data_from_db()

            def change_button_colors(button_1: TextButton, button_2: TextButton):
                button_1.style.bgcolor = GREY_COLOR
                button_2.style.bgcolor = BG_COLOR
                chitieu_thunhap1.update()

            # Create two text buttons.
            button_1 = TextButton(
                text="Chi tiêu", style=ButtonStyle(color="White", bgcolor=GREY_COLOR)
            )
            button_2 = TextButton(
                text="Thu nhập", style=ButtonStyle(color="White", bgcolor=GREY_COLOR)
            )

            # Calculate and format the total expense and income from the data
            total_expense = sum(row[3] for row in data if row[5] == "Tiền chi")
            total_income = sum(row[3] for row in data if row[5] == "Tiền thu")

            # Add on_click event listeners to the buttons.
            button_1.on_click = lambda event: change_button_colors(button_1, button_2)
            button_2.on_click = lambda event: change_button_colors(button_2, button_1)

            # Update the text on the buttons with the calculated totals
            # button_1.text = f"Chi tiêu: {total_expense}đ"
            # button_2.text = f"Thu nhập: {total_income}đ"

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
                            controls=[button_1, Text(f"{total_expense} đ")],
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
                            controls=[button_2, Text(f"{total_income} đ")],
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
                            controls=[button_3, Text(f"{total_income-total_expense} đ")],
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
        def create_bieudo():
            def change_button_colors(button_1: TextButton, button_2: TextButton):
                button_1.style.bgcolor = PINK
                button_2.style.bgcolor = GREY_COLOR
                bieudo1.update()

            # Create two text buttons.
            button_1 = TextButton(
                text="Chi tiêu", style=ButtonStyle(color="white", bgcolor=GREY_COLOR)
            )
            button_2 = TextButton(
                text="Thu nhập", style=ButtonStyle(color="White", bgcolor=GREY_COLOR)
            )

            # Add on_click event listeners to the buttons.
            button_1.on_click = lambda event: change_button_colors(button_1, button_2)
            button_2.on_click = lambda event: change_button_colors(button_2, button_1)
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

        def create_bieudotron():
            data = fetch_data_from_db()
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
            total_expense = sum(row[3] for row in data if row[5] == "Tiền chi")
            anuong="{:.2f}".format(sum(row[3] for row in data if row[4]=='Ăn uống')/total_expense*100)
            quanao="{:.2f}".format(sum(row[3] for row in data if row[4]=='Quần áo')/total_expense*100)
            tiennha="{:.2f}".format(sum(row[3] for row in data if row[4]=='Tiền nhà')/total_expense*100)
            tiendien="{:.2f}".format(sum(row[3] for row in data if row[4]=='Tiền điện')/total_expense*100)
            giadung="{:.2f}".format(sum(row[3] for row in data if row[4]=='Gia dụng')/total_expense*100)
            yte="{:.2f}".format(sum(row[3] for row in data if row[4]=='Y tế')/total_expense*100)
            giaoduc="{:.2f}".format(sum(row[3] for row in data if row[4]=='Giáo dục')/total_expense*100)
            dilai="{:.2f}".format(sum(row[3] for row in data if row[4]=='Đi lại')/total_expense*100)
            tiennuoc="{:.2f}".format(sum(row[3] for row in data if row[4]=='Tiền nước')/total_expense*100)
            khac="{:.2f}".format(sum(row[3] for row in data if row[4]=='Khác')/total_expense*100)
            
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
                        title="Quần áo"+str(f"{quanao}")+"%",
                        title_style=normal_title_style2,
                        color=ft.colors.BLUE,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        tiennha,
                        title="Tiền nhà"+str(f"{tiennha}")+"%",
                        title_style=normal_title_style2,
                        color=ft.colors.YELLOW,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        tiendien,
                        title="Tiền điện"+str(f"{tiendien}")+"%",
                        title_style=normal_title_style2,
                        color=ft.colors.PURPLE,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        anuong,
                        title="Ăn uống"+str(f"{anuong}")+"%",
                        title_style=normal_title_style2,
                        color=ft.colors.GREEN,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        giadung,
                        title="Gia dụng"+str(f"{giadung}")+"%",
                        title_style=normal_title_style2,
                        color=ft.colors.RED,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        yte,
                        title="Y tế"+str(f"{yte}")+"%",
                        title_style=normal_title_style2,
                        color=ft.colors.ORANGE,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        giaoduc,
                        title="Giáo dục"+str(f"{giaoduc}")+"%",
                        title_style=normal_title_style2,
                        color=ft.colors.PINK,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        tiennuoc,
                        title="Tiền nước"+str(f"{tiennuoc}")+"%",
                        title_style=normal_title_style2,
                        color=ft.colors.BROWN,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        dilai,
                        title="Đi lại"+str(f"{dilai}")+"%",
                        title_style=normal_title_style2,
                        color=ft.colors.GREY,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        khac,
                        title="Khác"+str(f"{khac}")+"%",
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
        # def create_navbar():
        #     nav_bar = NavigationBar(
        #         destinations=[
        #             NavigationDestination(icon=icons.EDIT, label="Nhập vào"),
        #             NavigationDestination(icon=icons.CALENDAR_MONTH, label="Lịch"),
        #             NavigationDestination(icon=icons.PIE_CHART, label="Báo cáo"),
        #             NavigationDestination(icon=icons.MORE_HORIZ, label="Khác"),
        #         ],
        #         bgcolor=BG_COLOR,
        #     )

        #     return nav_bar
        def create_thongke():
            data = fetch_data_from_db()
            thongke = ListView(
                height=65,
                width=340,
                # scroll='auto',
                spacing=1,
            )
            anuong=sum(row[3] for row in data if row[4]=='Ăn uống')
            quanao=sum(row[3] for row in data if row[4]=='Quần áo')
            tiennha=sum(row[3] for row in data if row[4]=='Tiền nhà')
            tiendien=sum(row[3] for row in data if row[4]=='Tiền điện')
            giadung=sum(row[3] for row in data if row[4]=='Gia dụng')
            yte=sum(row[3] for row in data if row[4]=='Y tế')
            giaoduc=sum(row[3] for row in data if row[4]=='Giáo dục')
            dilai=sum(row[3] for row in data if row[4]=='Đi lại')
            tiennuoc=sum(row[3] for row in data if row[4]=='Tiền nước')
            khac=sum(row[3] for row in data if row[4]=='Khác')
            thongke.controls.append(
                Container(
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
                                    Icon(name=icons.HOUSE, color="yellow"),
                                    Text("Tiền nhà:"),
                                ],
                            ),
                            Row(
                                alignment="end",
                                controls=[
                                    Text(f"{tiennha}"),
                                    Text("đ"),
                                ],
                            ),
                        ],
                    ),
                ),
            )

            thongke.controls.append(
                Container(
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
                                    Icon(icons.ELECTRIC_BOLT, color="PURPLE"),
                                    Text("Tiền điện:"),
                                ],
                            ),
                            Row(
                                alignment="end",
                                controls=[
                                    Text(f"{tiendien}"),
                                    Text("đ"),
                                ],
                            ),
                        ],
                    ),
                )
            )

            thongke.controls.append(
                Container(
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
                                    Icon(icons.CHECKROOM, color="blue"),
                                    Text("Quần áo:"),
                                ],
                            ),
                            Row(
                                alignment="end",
                                controls=[
                                    Text(f"{quanao}"),
                                    Text("đ"),
                                ],
                            ),
                        ],
                    ),
                )
            )

            thongke.controls.append(
                Container(
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
                                    Icon(icons.LOCAL_DINING, color="green"),
                                    Text("Ăn uống:"),
                                ],
                            ),
                            Row(
                                alignment="end",
                                controls=[
                                    Text(f"{anuong}"),
                                    Text("đ"),
                                ],
                            ),
                        ],
                    ),
                ),
            )
            thongke.controls.append(
                Container(
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
                                    Icon(icons.HOME_REPAIR_SERVICE, color="RED"),
                                    Text("Gia dụng:"),
                                ],
                            ),
                            Row(
                                alignment="end",
                                controls=[
                                    Text(f"{giadung}"),
                                    Text("đ"),
                                ],
                            ),
                        ],
                    ),
                )
            )

            thongke.controls.append(
                Container(
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
                                    Icon(icons.EMERGENCY, color="ORANGE"),
                                    Text("Y tế:"),
                                ],
                            ),
                            Row(
                                alignment="end",
                                controls=[
                                    Text(f"{yte}"),
                                    Text("đ"),
                                ],
                            ),
                        ],
                    ),
                )
            )
            thongke.controls.append(
                Container(
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
                                    Icon(icons.SCHOOL, color="PINK"),
                                    Text("Giáo dục:"),
                                ],
                            ),
                            Row(
                                alignment="end",
                                controls=[
                                    Text(f"{giaoduc}"),
                                    Text("đ"),
                                ],
                            ),
                        ],
                    ),
                )
            )
            thongke.controls.append(
                Container(
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
                                    Icon(icons.QUESTION_MARK, color="BLACK"),
                                    Text("Khác:"),
                                ],
                            ),
                            Row(
                                alignment="end",
                                controls=[
                                    Text(f"{khac}"),
                                    Text("đ"),
                                ],
                            ),
                        ],
                    ),
                )
            )
            thongke.controls.append(
                Container(
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
                                    Icon(icons.DIRECTIONS_BUS, color="GREY"),
                                    Text("Đi lại:"),
                                ],
                            ),
                            Row(
                                alignment="end",
                                controls=[
                                    Text(f"{dilai}"),
                                    Text("đ"),
                                ],
                            ),
                        ],
                    ),
                )
            )
            thongke.controls.append(
                Container(
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
                                    Icon(icons.WATER_DROP, color="BROWN"),
                                    Text("Tiền nước:"),
                                ],
                            ),
                            Row(
                                alignment="end",
                                controls=[
                                    Text(f"{tiennuoc}"),
                                    Text("đ"),
                                ],
                            ),
                        ],
                    ),
                )
            )
            return thongke
                

        header = create_header()
        date_row = create_date()
        chitieu_thunhap_thuchi = create_chitieu_thunhap_thuchi()
        bieu_do = create_bieudo()
        bieu_do_tron = create_bieudotron()
        navbar = create_navbar(self.page, 2)
        thongke1 = create_thongke()

        page_3_child_container = Container(
            padding=padding.only(left=30, top=30, right=30),
            content=Column(
                controls=[
                    header,
                    date_row,
                    chitieu_thunhap_thuchi,
                    bieu_do,
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
                    navbar,
                ],
            ),
        )

        return page_3
