import sqlite3
from flet import *
import csv
from const import *


class Exportdata(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def export_data_from_db():
            conn = sqlite3.connect("db/app.db")
            cursor = conn.cursor()
            data1 = cursor.execute("""SELECT * FROM financial_transaction""")
            data = [row for row in data1]
            csv_file = "sample.csv"

            with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as file:
                # writer = csv.writer(file)
                writer = csv.writer(file, delimiter=",")
                # Write the header row
                writer.writerow(
                    [
                        "ID",
                        "Date",
                        "Description",
                        "Amount",
                        "Category",
                        "Transaction Type",
                    ]
                )

                # Write the data rows
                for row in data:
                    writer.writerow(row)

            print(f"Data has been written to {csv_file}")
            conn.close()

        def create_header():
            # Create a function to change the background color of the buttons.
            def change_button_colors(button_1: TextButton):
                button_1.style.bgcolor = GREY_COLOR
                header.update()

            # Create two text buttons.
            button_1 = Text("Xuất toàn bộ dữ liệu", color="white", weight="bold")

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

            def export_data_and_close_dlg(e):
                export_data_from_db()
                close_dlg(e)

            dlg_modal = AlertDialog(
                modal=True,
                title=Text("Vui lòng xác nhận"),
                content=Text(
                    "Bạn có chắc chắn muốn xuất tất cả dữ liệu dưới dạng csv không"
                ),
                actions=[
                    TextButton("Yes", on_click=lambda e: export_data_and_close_dlg(e)),
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
                        Text("Xuất toàn bộ dữ liệu", color="yellow"),
                    ]
                ),
                on_click=lambda e: open_dlg(e),
            )

            return row

        header = create_header()
        delete_row = create_delete_row()

        exportdata_page_child_container = Container(
            padding=padding.only(left=10, top=30, right=30),
            content=Column(controls=[header, delete_row]),
        )

        exportdata_page = Container(
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            border_radius=35,
            bgcolor=BG_COLOR,
            content=Column(
                alignment="spaceBetween",
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    exportdata_page_child_container,
                ],
            ),
        )

        return exportdata_page
