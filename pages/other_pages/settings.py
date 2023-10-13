import sqlite3
from flet import *
from const import *


BG_COLOR = "#191919"
GREY_COLOR = "#3f3f3f"
PINK = "#eb06ff"


class Settings(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def delete_all_data_from_db():
            conn = sqlite3.connect("db/app.db")
            cursor = conn.cursor()

            # Build the SQL query to delete all data from the table
            sql_query = "DELETE FROM financial_transaction"

            # Execute the query to delete all data
            cursor.execute(sql_query)

            # Commit the changes to the database
            conn.commit()

            conn.close()

        def create_header():
            # Create a function to change the background color of the buttons.
            def change_button_colors(button_1: TextButton):
                button_1.style.bgcolor = GREY_COLOR
                header.update()

            # Create two text buttons.
            button_1 = Text("Cài đặt cơ bản", color="white", weight="bold")

            # Add on_click event listeners to the buttons.
            button_1.on_click = lambda event: change_button_colors(button_1)

            # Add the buttons to the page.
            header = Row(
                alignment=MainAxisAlignment.START,
                controls=[
                    IconButton(
                        icons.ARROW_BACK,
                        icon_color="white",
                        on_click=lambda e: self.page.go("/other"),
                    ),
                    button_1,
                ],
            )
            return header

        def create_delete_row():
            def open_dlg(e):
                self.page.dialog = dlg_modal
                dlg_modal.open = True
                self.page.update()

            def close_dlg(e):
                dlg_modal.open = False
                self.page.update()

            def delete_data_and_close_dlg(e):
                delete_all_data_from_db()
                close_dlg(e)

            dlg_modal = AlertDialog(
                modal=True,
                title=Text("Vui lòng xác nhận"),
                content=Text("Bạn có chắc chắn muốn xóa tất cả dữ liệu không"),
                actions=[
                    TextButton("Yes", on_click=lambda e: delete_data_and_close_dlg(e)),
                    TextButton("No", on_click=lambda e: close_dlg(e)),
                ],
                actions_alignment=MainAxisAlignment.END,
                on_dismiss=lambda e: print("Modal dialog dismissed!"),
            )

            row = Container(
                bgcolor=BG_COLOR,
                padding=padding.only(30, 10, 30, 10),
                border=border.only(
                    bottom=border.BorderSide(0.5, "#3c3c3c"),
                    top=border.BorderSide(0.5, "#3c3c3c"),
                ),
                content=Row(
                    controls=[
                        Icon(icons.DELETE, color="red"),
                        Text("Xóa toàn bộ dữ liệu", color="red"),
                    ]
                ),
                on_click=lambda e: open_dlg(e),
            )

            return row

        header = create_header()
        delete_row = create_delete_row()

        setting_page_child_container = Container(
            padding=padding.only(left=10, top=30, right=30),
            content=Column(controls=[header, delete_row]),
        )

        setting_page = Container(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            border_radius=35,
            bgcolor=BG_COLOR,
            content=Column(
                alignment="spaceBetween",
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    setting_page_child_container,
                ],
            ),
        )

        return setting_page
