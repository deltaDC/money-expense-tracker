from flet import *
import calendar
import datetime
from utils.navbar import create_navbar

# some constants
CELL_SIZE = (28, 28)
CELL_BG_COLOR = "while10"
TODAY_BG_COLOR = "teal600"
BG_COLOR = "#000000"
GREY_COLOR = "#3f3f3f"


# let's start
class SetCalendar(UserControl):
    def __init__(self, start_year=datetime.date.today().year):
        # we'll need a few class instances up here first
        # this widget will display the 12 months of years 2023. But an additional instance can be added to display other eyars as well

        self.current_year = start_year  # the current year

        self.m1 = datetime.date.today().month  # current month
        self.m2 = self.m1 + 1  # the second month, needed for the calendar module

        self.click_count: list = []  # for tracking clicks
        self.long_press_count: list = []  # same as above

        self.current_color = "blue"  # highlight color

        self.slected_date = any  # the sleected data from the calendar

        self.calendar_grid = Column(
            wrap=True,
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
        )

        super().__init__()

    # first let's create the ability to paginate the months
    def _change_month(self, delta):
        # recall that we stored the current month + month2 abvoe as self.m1 and self.m2
        # we can use hte max and min to make sure the numbers stay between 1 and 13, as per the calendar library
        # the below now keeps m1 between 1 and 12, and m2 between 2 and 13.
        self.m1 = min(max(1, self.m1 + delta), 12)
        self.m2 = min(max(2, self.m2 + delta), 13)

        # we need to create a new calendar varaible
        new_calendar = self.create_month_calendar(self.current_year)
        self.calendar_grid = new_calendar
        self.update()  # this should update the calendar by month

    # final we can keep adding more functions to make the widget more complex.Let's highlight the container when it's clicked.
    def one_click_date(self, e):
        # if we want to change the text title to the highlighted click, we can also do this but it'll requre a third button
        self.selected_date = e.control.data
        e.control.bgcolor = "blue600"
        e.control.update()
        self.update()

    def long_click_date(self, e):
        # now for multiple dates.
        # we can set this up so that a user can click two dates and it'll highlight all the dates in between

        # 1. Save the two clicks to a list
        self.long_press_count.append(e.control.data)
        # 2. Check to see if there are indeed 2 clicks
        if len(self.long_press_count) == 2:
            # 3. Set two dates by unpacking the list
            date1, date2 = self.long_press_count
            # 4. Get the absolute distance between them
            delta = abs(date2 - date1)
            # 5. Now check to see if it's past selection or future
            if date1 < date2:
                dates = [
                    date1 + datetime.timedelta(days=x) for x in range(delta.days + 1)
                ]
            else:
                dates = [
                    date2 + datetime.timedelta(days=x) for x in range(delta.days + 1)
                ]

            # 6. We loop over the calendar matrix and color the boxes
            for _ in self.calendar_grid.controls[:]:
                for __ in _.controls[:]:
                    if isinstance(__, Row):
                        for box in __.controls[:]:
                            # 7. Here we check to see if the dates list above matches the dates we created for each container data
                            if box.data in dates:
                                box.bgcolor = "blue600"
                                box.update()

            self.long_press_count = []

        else:
            pass

    # we can now create the logic for calendar
    def create_month_calendar(self, year):
        self.current_year = year  # get the current year
        self.calendar_grid.controls: list = []  # clear the calendar grid

        for month in range(self.m1, self.m2):
            # this gets the month name + year
            month_label = Text(
                f"{calendar.month_name[month]} {self.current_year}",
                size=14,
                weight="bold",
            )

            # now we need a month matrix
            # this gets the days of the month as per the year passed
            month_matrix = calendar.monthcalendar(self.current_year, month)
            month_grid = Column(alignment=MainAxisAlignment.CENTER)
            month_grid.controls.append(
                Row(
                    alignment=MainAxisAlignment.START,
                    controls=[month_label],
                )
            )

            # now lets get the weekday labels
            # this is in the form of list. compr.
            weekday_labels = [
                Container(
                    width=28,
                    height=28,
                    alignment=alignment.center,
                    content=Text(
                        weekday,
                        size=12,
                        color="white54",
                    ),
                )
                for weekday in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            ]

            # now put the list of weekenday containers in a row
            weekday_row = Row(controls=weekday_labels)
            month_grid.controls.append(weekday_row)

            # now for the days
            for week in month_matrix:
                week_container = Row()
                for day in week:
                    if day == 0:  # if the day in gird is empty
                        day_container = Container(
                            width=28,
                            height=28,
                        )
                    else:
                        day_container = Container(
                            width=28,
                            height=28,
                            border=border.all(0.5, "white24"),
                            alignment=alignment.center,
                            # we need to pass in some additonal paramters to the main day cont.
                            # we use this data for the above!
                            data=datetime.date(
                                year=self.current_year,
                                month=month,
                                day=day,
                            ),
                            on_click=lambda e: self.one_click_date(e),
                            on_long_press=lambda e: self.long_click_date(e),
                            animate=400,
                        )
                    day_label = Text(str(day), size=12)

                    # we need to make a second check here
                    if day == 0:
                        day_label = None
                    if (
                        day == datetime.date.today().day
                        and month == datetime.date.today().month
                        and self.current_year == datetime.date.today().year
                    ):
                        day_container.bgcolor = "teal700"
                    day_container.content = day_label
                    week_container.controls.append(day_container)
                month_grid.controls.append(week_container)

        self.calendar_grid.controls.append(month_grid)

        return self.calendar_grid

    def build(self):
        return self.create_month_calendar(self.current_year)


# let's switch and get to the upper level UI
class DataSetup(UserControl):
    def __init__(self, cal_gird):
        self.cal_gird = cal_gird  # this is the calendar intance

        # we can now create the buttons here
        self.prev_btn = BTNPagnation("Prev", lambda e: cal_gird._change_month(-1))
        self.next_btn = BTNPagnation("Next", lambda e: cal_gird._change_month(1))

        self.today = Text(
            datetime.date.today().strftime("%B %d, %Y"),
            width=260,
            size=13,
            color="white54",
            weight="w400",
        )

        # this will hold the pagination button
        self.btn_container = Row(
            alignment=MainAxisAlignment.CENTER,
            controls=[
                # buttons go in here
                self.prev_btn,
                self.next_btn,
            ],
        )

        # this container will store the calendar you see to the right
        self.calendar = Container(
            width=320,
            height=45,
            bgcolor="#313131",
            border_radius=8,
            animate=300,
            clip_behavior=ClipBehavior.HARD_EDGE,
            alignment=alignment.center,
            content=Column(
                alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    # here we can pass in the actual calendar instance plus the buttons
                    Divider(height=60, color="transparent"),
                    self.cal_gird,
                    Divider(height=10, color="transparent"),
                    self.btn_container,
                ],
            ),
        )

        super().__init__()

    # we need a function to expand the stack to see the calendar
    def _get_calendar(self, e: None):
        if self.calendar.height == 45:
            self.calendar.height = 400
            self.calendar.update()
        else:
            self.calendar.height = 45
            self.calendar.update()

    def build(self):
        return Stack(
            # use a stack to stack the controls ontop of each other
            width=320,
            controls=[
                self.calendar,
                Container(
                    on_click=lambda e: self._get_calendar(e),
                    width=320,
                    height=45,
                    border_radius=8,
                    bgcolor="#313131",
                    padding=padding.only(left=15, right=5),
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=CrossAxisAlignment.CENTER,
                        controls=[
                            self.today,
                            Container(
                                width=32,
                                height=32,
                                border=border.only(
                                    left=BorderSide(0.9, "white24"),
                                ),
                                alignment=alignment.center,
                                content=Icon(
                                    name=icons.CALENDAR_MONTH_SHARP,
                                    size=15,
                                    opacity=0.65,
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        )


# let's divert quickly and c reate the buttons for pagination
class BTNPagnation(UserControl):
    def __init__(self, txt_name, function):
        self.txt_name = txt_name
        self.function = function
        super().__init__()

    def build(self):
        return IconButton(
            content=Text(self.txt_name, size=8, weight="bold"),
            width=56,
            height=28,
            on_click=self.function,
            style=ButtonStyle(
                shape={"": RoundedRectangleBorder(radius=6)}, bgcolor={"": "teal600"}
            ),
        )


class details_month(UserControl):
    def __init__(self, revenue, spending_money):
        self.revenue = revenue
        self.spending_money = spending_money
        super().__init__()

    def build(self):
        return Column(
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.START,
            controls=[
                Container(
                    width=340,
                    height=30,
                    border_radius=5,
                    bgcolor=GREY_COLOR,
                    padding=1,
                    content=Row(
                        alignment="spaceBetween",
                        controls=[
                            Row(alignment="start", controls=[Text("Thu nhập:")]),
                            Row(
                                alignment="end",
                                controls=[
                                    Text(
                                        f"{self.revenue} đ",
                                        style=TextStyle(color=colors.BLUE_100),
                                    )
                                ],
                            ),
                        ],
                    ),
                ),
                Container(
                    width=340,
                    height=30,
                    border_radius=5,
                    bgcolor=GREY_COLOR,
                    padding=1,
                    content=Row(
                        alignment="spaceBetween",
                        controls=[
                            Row(alignment="start", controls=[Text("Chi tiêu:")]),
                            Row(
                                alignment="end",
                                controls=[
                                    Text(
                                        f"{self.spending_money} đ",
                                        style=TextStyle(color=colors.RED_100),
                                    )
                                ],
                            ),
                        ],
                    ),
                ),
                Container(
                    width=340,
                    height=30,
                    border_radius=5,
                    bgcolor=GREY_COLOR,
                    content=Row(
                        alignment="spaceBetween",
                        controls=[
                            Row(alignment="start", controls=[Text("Tổng:")]),
                            Row(
                                alignment="end",
                                controls=[
                                    Text(
                                        f"{self.revenue + self.spending_money} đ",
                                        style=TextStyle(color=colors.BLUE_400),
                                    )
                                ],
                            ),
                        ],
                    ),
                ),
            ],
        )


class Calendar(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        self.page.horizontal_alignment = "center"
        self.page.vertical_alignment = "center"
        test = SafeArea(
            Column(
                spacing=10,
                controls=[
                    Row(
                        alignment="spaceBetween",
                        controls=[
                            Text(
                                text_align=TextAlign.CENTER,
                                value="Lịch",
                                style=TextStyle(
                                    size=20,
                                    weight=FontWeight.W_200,
                                ),
                            ),
                            IconButton(
                                icon=icons.SEARCH,
                                icon_size=20,
                                tooltip="Search for expenses",
                            ),
                        ],
                    ),
                ],
            )
        )
        cal = SetCalendar()
        date = DataSetup(cal)
        total = details_month(0, 0)
        navbar = create_navbar(self.page, 1)

        main_page_child_container = Container(
            padding=padding.only(left=30, top=30, right=30),
            content=Column(
                controls=[
                    test, 
                    date, 
                    total
                ]
            )
        )

        main_page = Container(
            width=400,
            height=712,
            border_radius=35,
            bgcolor=BG_COLOR,
            content=Column(
                alignment="spaceBetween",
                controls=[
                    main_page_child_container,
                    navbar
                ],
            ),
        )

        return main_page
