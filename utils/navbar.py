from flet import *
from const import *


# class NavBar(UserControl):
#     def __init__(self, page):
#         super().__init__()
#         page = page

#     def build(self):
#         def change_tab(e):
#             my_index = e.control.selected_index
#             if my_index == 0:
#                 nav_bar.selected_index = 0
#                 page.go("/")
#             elif my_index == 1:
#                 nav_bar.selected_index = 1
#                 page.go("/calendar")
#             elif my_index == 2:
#                 nav_bar.selected_index = 2
#                 page.go("/report")
#             elif my_index == 3:
#                 nav_bar.selected_index = 3
#                 pass

#         def check_selected_index():
#             if page.route == "/":
#                 nav_bar.selected_index = 0
#             elif page.route == "/calendar":
#                 nav_bar.selected_index = 1
#             elif page.route == "report":
#                 nav_bar.selected_index = 2
#             else:
#                 pass

#         nav_bar = NavigationBar(
#             destinations=[
#                 NavigationDestination(
#                     icon=icons.EDIT, 
#                     label="Nhập vào",
#                 ),
#                 NavigationDestination(
#                     icon=icons.CALENDAR_MONTH, 
#                     label="Lịch",
#                 ),
#                 NavigationDestination(icon=icons.PIE_CHART,label="Báo cáo",),
#                 NavigationDestination(icon=icons.MORE_HORIZ,label="Khác",),
#             ],
#             # bgcolor=BG_COLOR,
#             on_change=functools.partial(change_tab, check_selected_index)
#         )

#         return nav_bar

def create_navbar(page: Page, selected_index):
    def change_tab(e):
        my_index = e.control.selected_index
        if my_index == 0:
            page.go("/")
        elif my_index == 1:
            page.go("/calendar")
        elif my_index == 2:
            page.go("/report_outcome")
        elif my_index == 3:
            page.go("/other")

        page.update()

    nav_bar = NavigationBar(
        destinations=[
            NavigationDestination(
                icon=icons.EDIT, 
                label="Nhập vào",
            ),
            NavigationDestination(
                icon=icons.CALENDAR_MONTH, 
                label="Lịch",
            ),
            NavigationDestination(icon=icons.PIE_CHART,label="Báo cáo",),
            NavigationDestination(icon=icons.MORE_HORIZ,label="Khác",),
        ],
        bgcolor=BG_COLOR,
        selected_index=selected_index,
        on_change=change_tab
    )

    return nav_bar  