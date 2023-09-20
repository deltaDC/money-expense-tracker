from flet import *
import datetime
from const import *


# main
def main(page: Page):
    header = create_header()
    date_row = create_date()
    note_row = create_note()
    money_row = create_money_input()
    category_row = create_category()
    submit_row = create_submit()
    nav_bar_row = create_navbar()

    page_1_child_container = Container(
        padding=padding.only(left=30, top=30, right=30),
        content=Column(
            controls=[
                header,
                date_row,
                note_row,
                money_row,
                category_row,
            ]
        )
    )

    # define page 1 properties
    page_1 = Container(
        width=400,
        height=712,
        border_radius=35,
        bgcolor=BG_COLOR,
        content=Column(
            alignment="spaceBetween",
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                page_1_child_container,
                submit_row,
                nav_bar_row
            ]
        ),
    )
    

    page.add(page_1)


def create_header():
    # Create a function to change the background color of the buttons.
    def change_button_colors(button_1: TextButton, button_2: TextButton):
        button_1.style.bgcolor = GREY_COLOR
        button_2.style.bgcolor = BG_COLOR
        header.update()

    # Create two text buttons.
    button_1 = TextButton(
        text="Tiền thu", style=ButtonStyle(color="White", bgcolor=GREY_COLOR)
    )
    button_2 = TextButton(text="Tiền chi", style=ButtonStyle(color="White"))

    # Add on_click event listeners to the buttons.
    button_1.on_click = lambda event: change_button_colors(button_1, button_2)
    button_2.on_click = lambda event: change_button_colors(button_2, button_1)

    # Add the buttons to the page.
    header = Row(
        alignment="spaceBetween",
        controls=[
            Row(
                controls=[
                    button_1,
                    button_2,
                ]
            ),
            Icon(name=icons.EDIT, color="White"),
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
            Text(datetime.date.today(), color="white"),
            # Create a row to contain the arrow buttons.
            Row(
                controls=[
                    # Create an icon button for the previous arrow.
                    IconButton(
                        icon=icons.ARROW_LEFT,
                        icon_color="White",
                        on_click=lambda event: get_prev_date(
                            date_header.controls[0].value
                        ),
                    ),
                    # Create an icon button for the next arrow.
                    IconButton(
                        icon=icons.ARROW_RIGHT,
                        icon_color=colors.WHITE,
                        on_click=lambda event: get_next_date(
                            date_header.controls[0].value
                        ),
                    ),
                ]
            ),
        ],
    )

    return date_header


def create_note():
    note_header = Row(
        alignment="spaceBetween",
        # spacing=20,
        controls=[
            Text("Ghi chú", color="White"),
            TextField(
                label="Nhập ghi chú",
                label_style=TextStyle(color="White"),
                width=250,
                height=50,
                border_color="White",
                color="White",
            ),
        ],
    )

    return note_header


def create_money_input():
    money_input = Row(
        alignment="spaceBetween",
        controls=[
            Text("Tiền chi"),
            Row(
                controls=[
                    TextField(
                        hint_text="Nhập số tiền",
                        border="underline",
                        width=200,
                        height=40
                    ),
                    Text("đ", size=16),
                ]
            ),
        ],
    )

    return money_input


def create_category():
    global current_button
    current_button = None

    def create_category_button(text, icon, icon_color):
        category_button = Container(
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Icon(icon, color=icon_color, size=30),
                    Text(text),
                ],
            ),
            alignment=alignment.center,
            bgcolor=BG_COLOR,
            width=10,
            height=10,
            border=border.all(3, BORDER_COLOR),
            border_radius=10,
            on_click=lambda e: on_button_click(e, category_button),
        )

        return category_button

    def on_button_click(e, button):
        global current_button
        # Set the border color of the current button to a new color.
        button.border = border.all(3, "#a9a9a9")

        # Set the border color of the previous button to the default color.
        if current_button is not None:
            current_button.border = border.all(3, BORDER_COLOR)

        # Set the current button to the button that is clicked.
        current_button = button
        category.update()

    category_header = Text("Danh mục")

    category_content = GridView(
        # expand=True,
        runs_count=3,
        max_extent=100,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
        controls=[
            create_category_button("Ăn uống", icons.LOCAL_DINING, "#d78638"),
            create_category_button("Gia dụng", icons.HOME_REPAIR_SERVICE, "#049c4b"),
            create_category_button("Quần áo", icons.CHECKROOM, "#c9ae1d"),
            create_category_button("Y tế", icons.EMERGENCY, "#c1455c"),
            create_category_button("Giáo dục", icons.SCHOOL, "#66bb88"),
            create_category_button("Tiền điện", icons.ELECTRIC_BOLT, "#dddddd"),
            create_category_button("Tiền nhà", icons.HOUSE, "#d89825"),
            create_category_button("Tiền nước", icons.WATER_DROP, "#23bbdc"),
            create_category_button("Đi lại", icons.DIRECTIONS_BUS, "#fbc932"),
            create_category_button("Khác", icons.QUESTION_MARK, "#d78638"),
        ],
    )

    category = Column(controls=[category_header, category_content])
    return category


def create_submit():
    submit_button = TextButton(
        text="Nhập Khoản Tiền",
        style=ButtonStyle(
            color="White", bgcolor=GREY_COLOR
        ),
        width=350
    )

    return submit_button


def create_navbar():

    nav_bar = NavigationBar(
        destinations=[
            NavigationDestination(icon=icons.EDIT, label="Nhập vào"),
            NavigationDestination(icon=icons.CALENDAR_MONTH, label="Lịch"),
            NavigationDestination(icon=icons.PIE_CHART,label="Báo cáo"),
            NavigationDestination(icon=icons.MORE_HORIZ,label="Khác"),
        ],
        bgcolor=BG_COLOR
    )

    return nav_bar


app(target=main)
