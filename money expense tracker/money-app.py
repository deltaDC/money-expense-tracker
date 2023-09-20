from flet import *
import datetime

# const
BG_COLOR = "#191919"
GREY_COLOR = "#3f3f3f"


# main
def main(page: Page):
    header = create_header()
    date_row = create_date()
    note_row = create_note()

    # define main page properties
    main_page = Container(
        width=400,
        height=850,
        border_radius=35,
        bgcolor=BG_COLOR,
        padding=padding.only(left=40, top=30, right=40),
        content=Column(controls=[header, date_row, note_row]),
    )

    page.add(main_page)


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
                border_color="White",
                color="White",
            ),
        ],
    )

    return note_header


app(target=main)
