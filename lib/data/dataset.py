STUDENT_REQUIRED_KEYS: list[str] = ["last_name", "first_name", "birth_day", "birth_month", "birth_year", "student_id"]


def check_student_directory(data: dict) -> list | None:
    if all(key in data for key in STUDENT_REQUIRED_KEYS):
        return None
    else:
        array = []

        for key in STUDENT_REQUIRED_KEYS:
            if key not in data:
                array.append(key)

        return array


OPENCV_SUPPORTED_IMREAD_FORMATS: list[str] = [
    # Windows bitmaps
    'bmp', 'dip',
    # JPEG files
    'jpeg', '.jpg', '.jpe', 'jp2',
    # PNG
    'png',
    # Portable image format
    'pbm', 'pgm', 'ppm',
    # Sun rasters
    'sr', 'ras',
    # TIFF
    'tiff', 'tif'
]
