class Student:

    def __init__(self, last_name, first_name, birth_day, birth_month, birth_year, student_id, seat):
        self.last_name = last_name
        self.first_name = first_name
        self.birth_day = birth_day
        self.birth_month = birth_month
        self.birth_year = birth_year
        self.student_id = student_id
        self.seat = seat

    def get_month_number(self) -> int | None:
        months = {
            'January': 1,
            'February': 2,
            'March': 3,
            'April': 4,
            'May': 5,
            'June': 6,
            'July': 7,
            'August': 8,
            'September': 9,
            'October': 10,
            'November': 11,
            'December': 12
        }

        for month, num in months.items():
            print(month)
            if month == self.birth_month:
                return num

        return self.birth_month
