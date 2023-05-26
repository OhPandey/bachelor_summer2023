STUDENT_REQUIRED_KEYS = ["last_name", "first_name", "birth_day", "birth_month", "birth_year", "student_id"]


def check_student_directory(data):
    if all(key in data for key in STUDENT_REQUIRED_KEYS):
        return None
    else:
        array = []

        for key in STUDENT_REQUIRED_KEYS:
            if key not in data:
                array.append(key)

        return array
