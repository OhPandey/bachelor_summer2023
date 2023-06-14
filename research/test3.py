import csv
import os
import time

import cv2
import numpy
import numpy as np
import tensorflow as tf
import easyocr
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util

from lib.utils.position import Position
from lib.utils.processing_data import processing_data_easyocr



def read_text(capture):
    # Easyocr
    reader = easyocr.Reader(['en'], gpu=True)
    all_results = reader.readtext(capture)
    if all_results is None:
        return None

    results = list()

    for place, text, prob in all_results:
        if prob >= 0.5:
            # Debugging
            print(f'Text: {text}, Confidence {prob:.2f}')
            results.append(text)

    if len(results) < 3:
        return None

    return processing_data_easyocr(results)


def analyse_easyocr(capture):
    # To generate average time
    time_arrays = []

    # To count the frames
    count = 0

    while capture.isOpened():
        ret, frame = capture.read()

        if not ret:
            print("End of stream")
            break

        start = time.time()
        result = read_text(frame)
        end = round(time.time() - start, 3)

        time_arrays.append(end)
        count += 1
        print(f'[Frame {count}] Result: {result}, Time: {end}')
        return result
    return None


if __name__ == '__main__':
    iterations = 1

    print("-- Frame Analyzer For Educational Purposes --")

    export_data = [
        [
            "Run",
            "last_name",
            "first_name",
            "birth_day",
            "birth_month",
            "birth_year",
            "student_id"
        ]
    ]

    for e in range(1, iterations + 1):
        print(f"-- Run {e} --")
        capture_positive = cv2.VideoCapture('../testing_movies/one.mov')
        data = analyse_easyocr(capture_positive)
        if data is not None:
            export_data.append([
                f"{e}",
                f"{data['last_name']}",
                f"{data['first_name']}",
                f"{data['birth_day']}",
                f"{data['birth_month']}",
                f"{data['birth_year']}",
                f"{data['student_id']}",
            ])
        capture_positive.release()

    with open(f"results2.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(export_data)

