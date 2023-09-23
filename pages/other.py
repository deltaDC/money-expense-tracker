from flet import *
from const import *
from utils.navbar import create_navbar

class Other(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        def create_row(icon, text):
            row = Container(
                bgcolor=BG_COLOR,
                padding=padding.only(30,10,30,10),
                border=border.only(bottom=border.BorderSide(0.5, "#3c3c3c"), top=border.BorderSide(0.5, "#3c3c3c")),
                content=Row(
                    controls=[
                        Icon(icon, color="white"),
                        Text(text, color="white")
                    ]
                )
            )

            return row
        

        buttons = Column(
            spacing=20,
            controls=[
                Container(
                    padding=30,
                    content=Text("Khác", color="white", size=20),
                ),
                create_row(icons.SETTINGS, "Cài đặt cơ bản"),
                Column(
                    spacing=0,
                    controls=[
                        create_row(icons.BAR_CHART, "Báo cáo trong năm"),
                        create_row(icons.PIE_CHART, "Báo cáo danh mục trong năm"),
                        create_row(icons.INSERT_CHART_OUTLINED, "Báo cáo toàn kì"),
                        create_row(icons.PIE_CHART_OUTLINE, "Báo cáo danh mục toàn kì")
                    ]
                ),
                Column(
                    spacing=0,
                    controls=[
                        create_row(icons.DOWNLOAD, "Đầu ra dữ liệu"),
                        create_row(icons.CLOUD_DOWNLOAD, "Sao lưu dữ liệu")
                    ]
                ),
                Column(
                    spacing=0,
                    controls=[
                        create_row(icons.QUESTION_MARK, "Trợ giúp"),
                        create_row(icons.INFO, "Thông tin ứng dụng")
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