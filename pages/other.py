from flet import *
from const import *
from utils.navbar import create_navbar

class Other(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def create_row(icon, text,duongdan):
            row = Container(
                bgcolor=BG_COLOR,
                padding=padding.only(30,10,30,10),
                border=border.only(bottom=border.BorderSide(0.5, "#3c3c3c"), top=border.BorderSide(0.5, "#3c3c3c")),
                content=Row(
                    controls=[
                        IconButton(icon, icon_color="white",
                                    on_click=lambda e:self.page.go(duongdan)
                                   ),
                        TextButton(text, icon_color="white",
                                    on_click=lambda e:self.page.go(duongdan)
                                   )
                    ]
                )
            )

            return row
        

        buttons = Column(
            spacing=0,
            controls=[
                Container(
                    padding=15,
                    content=Text("Khác", color="white", size=15),
                ),
                create_row(icons.SETTINGS, "Cài đặt cơ bản",'/report_2'),
                Column(
                    spacing=0,
                    controls=[
                        create_row(icons.BAR_CHART, "Báo cáo trong năm",'/report_2'),
                        create_row(icons.PIE_CHART, "Báo cáo danh mục trong năm",'/report_2'),
                        create_row(icons.INSERT_CHART_OUTLINED, "Báo cáo toàn kì",'/report_2'),
                        create_row(icons.PIE_CHART_OUTLINE, "Báo cáo danh mục toàn kì",'/report_2')
                    ]
                ),
                Column(
                    spacing=0,
                    controls=[
                        create_row(icons.DOWNLOAD, "Đầu ra dữ liệu",'/report_2'),
                        create_row(icons.CLOUD_DOWNLOAD, "Sao lưu dữ liệu",'/report_2')
                    ]
                ),
                Column(
                    spacing=0,
                    controls=[
                        create_row(icons.QUESTION_MARK, "Trợ giúp",'/report_2'),
                        create_row(icons.INFO, "Thông tin ứng dụng",'/report_2')
                    ]
                ),
            ]
        )
        
        navbar = create_navbar(self.page, 3)
        
        other_page = Container(
            width=400,
            height=712,
            border_radius=35,
            bgcolor="#0d0d0d",
            content=Column(
                alignment="spaceBetween",
                controls=[
                    buttons,
                    navbar
                ]
            )
        )
        
        return other_page