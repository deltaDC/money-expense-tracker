from flet import *
import flet as ft
import datetime

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
            def get_next_date(curr_date):
                next_date = curr_date + datetime.timedelta(days=1)
                date_header.controls[0].value = next_date
                date_header.update()

            def get_prev_date(curr_date):
                prev_date = curr_date - datetime.timedelta(days=1)
                date_header.controls[0].value = prev_date
                date_header.update()

            # Create a row to represent the date header.
            date_header = Row(
                alignment="spaceBetween",
                controls=[
                    # Create a text widget to display the datetime.datetime.
                    Text(datetime.date.today()),
                    # Create a row to contain the arrow buttons.
                    Row(
                        controls=[
                            # Create an icon button for the previous arrow.
                            IconButton(
                                icons.ARROW_LEFT,
                                on_click=lambda event: get_prev_date(
                                    date_header.controls[0].value
                                ),
                            ),
                            # Create an icon button for the next arrow.
                            IconButton(
                                icons.ARROW_RIGHT,
                                on_click=lambda event: get_next_date(
                                    date_header.controls[0].value
                                ),
                            ),
                        ]
                    ),
                ],
            )

            return date_header

        def create_chitieu_thunhap():
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

            # Add on_click event listeners to the buttons.
            button_1.on_click = lambda event: change_button_colors(button_1, button_2)
            button_2.on_click = lambda event: change_button_colors(button_2, button_1)
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
                            controls=[button_1, Text("-150.000đ")],
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
                            controls=[button_2, Text("2.000.000đ")],
                        ),
                    ),
                ],
            )
            return chitieu_thunhap1

        def create_thuchi():
            def change_button_colors(button_1: TextButton):
                button_1.style.bgcolor = GREY_COLOR
                thu_chi1.update()

            # Create two text buttons.
            button_1 = TextButton(
                text="Chi tiêu", style=ButtonStyle(color="White", bgcolor=GREY_COLOR)
            )

            # Add on_click event listeners to the buttons.
            button_1.on_click = lambda event: change_button_colors(button_1)

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
                            controls=[button_1, Text("1.850.000đ")],
                        ),
                    )
                ]
            )
            return thu_chi1

        def create_bieudo():
            def change_button_colors(button_1: TextButton, button_2: TextButton):
                button_1.style.bgcolor = GREY_COLOR
                button_2.style.bgcolor = BG_COLOR
                bieudo1.update()

            # Create two text buttons.
            button_1 = TextButton(
                text="Chi tiêu", style=ButtonStyle(color="White", bgcolor=GREY_COLOR)
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
                        padding=padding.only(right=150),
                        content=Container(
                            bgcolor=PINK,
                        ),
                    ),
                ]
            )
            return bieudo1

        def create_bieudotron():
            normal_radius = 65
            hover_radius = 70
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
                        10,
                        title="Quần áo(10%)",
                        title_style=normal_title_style2,
                        color=ft.colors.BLUE,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        10,
                        title="Tiền nhà(10%)",
                        title_style=normal_title_style2,
                        color=ft.colors.YELLOW,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        10,
                        title="Tiền điện(10%)",
                        title_style=normal_title_style2,
                        color=ft.colors.PURPLE,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        10,
                        title="Ăn uống(10%)",
                        title_style=normal_title_style2,
                        color=ft.colors.GREEN,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        10,
                        title="Gia dụng(10%)",
                        title_style=normal_title_style2,
                        color=ft.colors.RED,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        10,
                        title="Y tế(10%)",
                        title_style=normal_title_style2,
                        color=ft.colors.ORANGE,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        10,
                        title="Giáo dục(10%)",
                        title_style=normal_title_style2,
                        color=ft.colors.PINK,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        10,
                        title="Tiền nước(10%)",
                        title_style=normal_title_style2,
                        color=ft.colors.BROWN,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        10,
                        title="Đi lại(10%)",
                        title_style=normal_title_style2,
                        color=ft.colors.GREY,
                        radius=normal_radius,
                    ),
                    ft.PieChartSection(
                        10,
                        title="Khác(10%)",
                        title_style=normal_title_style2,
                        color=ft.colors.BLACK,
                        radius=normal_radius,
                    ),
                ],
                sections_space=0,
                center_space_radius=75,
                # size=ft.size(150, 150),
                on_chart_event=on_chart_event,
                expand=False,
            )

            return chart

        def create_navbar():
            nav_bar = NavigationBar(
                destinations=[
                    NavigationDestination(icon=icons.EDIT, label="Nhập vào"),
                    NavigationDestination(icon=icons.CALENDAR_MONTH, label="Lịch"),
                    NavigationDestination(icon=icons.PIE_CHART, label="Báo cáo"),
                    NavigationDestination(icon=icons.MORE_HORIZ, label="Khác"),
                ],
                bgcolor=BG_COLOR,
            )

            return nav_bar

        def create_thongke():
            thongke = ListView(
                height=65,
                width=340,
                # scroll='auto',
                spacing=3,
            )
            thongke.controls.append(
                Container(
                    width=340,
                    height=30,
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
                                    Text("45.000"),
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
                    height=30,
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
                                    Text("22.500"),
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
                    height=30,
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
                                    Text("60.000"),
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
                    height=30,
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
                                    Text("45.000"),
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
                    height=30,
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
                                    Text("22.500"),
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
                    height=30,
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
                                    Text("22.500"),
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
                    height=30,
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
                                    Text("22.500"),
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
                    height=30,
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
                                    Text("22.500"),
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
                    height=30,
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
                                    Text("22.500"),
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
                    height=30,
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
                                    Text("22.500"),
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
        chitieu_thunhap = create_chitieu_thunhap()
        thuchi = create_thuchi()
        bieu_do = create_bieudo()
        bieu_do_tron = create_bieudotron()
        navbar = create_navbar()
        thongke1 = create_thongke()

        page_3_child_container = Container(
            padding=padding.only(left=30, top=30, right=30),
            content=Column(
                controls=[
                    header,
                    date_row,
                    chitieu_thunhap,
                    thuchi,
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
