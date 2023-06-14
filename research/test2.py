import csv
import os
import time

import cv2
import numpy
import numpy as np
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util

# Load model
configs = config_util.get_configs_from_pipeline_file(os.path.join('../model', 'ssd-20', 'pipeline.config'))
detection_model = model_builder.build(model_config=configs['model'], is_training=False)
# Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join('../model', 'ssd-20', 'ckpt-3')).expect_partial()


@tf.function
def detect_fn(tensor_image):
    image, shapes = detection_model.preprocess(tensor_image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections


def cnn(capture):
    image_np = np.array(capture)

    input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
    detections = detect_fn(input_tensor)
    num_detections = int(detections.pop('num_detections'))

    detections = {key: value[0, :num_detections].numpy()
                  for key, value in detections.items()}
    detections['num_detections'] = num_detections

    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    detection_scores = detections['detection_scores']

    for i in range(num_detections):
        score = detection_scores[i]
        if score > 0.9:
            return True

    return False


def analyse_cnn(capture):
    # To generate average time
    time_arrays = []

    # To count the frames
    count = 0

    # Actual data gathered
    trues = 0
    falses = 0

    while capture.isOpened():
        ret, frame = capture.read()

        if not ret:
            print("End of stream")
            break

        start = time.time()
        result = cnn(frame)
        end = round(time.time() - start, 3)

        if result:
            trues += 1
        else:
            falses += 1

        time_arrays.append(end)
        count += 1
        print(f'[Frame {count}] Result: {result}, Time: {end}')

    if count >= 0:
        average_time = numpy.average(time_arrays)
        recall = trues / count

        print(f"-- Results --")
        print(f"Frames analysed: {count}")
        print(f"Average processing time: {average_time}")
        print(f"Detected: {trues}")
        print(f"Not detected: {falses}")
        print(f"Recall: {recall}")
        print("-- END of Analysing Feature Matching --")
        return [count, average_time, trues, falses, recall]
    else:
        return [0, 0, 0, 0, 0]


if __name__ == '__main__':
    iterations = 50

    print("-- Frame Analyzer For Educational Purposes --")

    export_data = [
        [
            "Run",
            "Count",
            "Time",
            "Recall",
        ]
    ]

    for e in range(1, iterations + 1):
        print(f"-- Run {e} --")
        capture_positive = cv2.VideoCapture('../testing_movies/four.mov')
        data = analyse_cnn(capture_positive)
        export_data.append([
            f"{e}",
            f"{data[0]}",
            f"{data[1]}",
            f"{data[4]}"
        ])
        capture_positive.release()

    for e in range(1, iterations + 1):
        print(f"-- Run {e} --")
        capture_positive = cv2.VideoCapture('../testing_movies/five.mov')
        data = analyse_cnn(capture_positive)
        export_data.append([
            f"{e}",
            f"{data[0]}",
            f"{data[1]}",
            f"{data[4]}"
        ])
        capture_positive.release()

    for e in range(1, iterations + 1):
        print(f"-- Run {e} --")
        capture_positive = cv2.VideoCapture('../testing_movies/six.mov')
        data = analyse_cnn(capture_positive)
        export_data.append([
            f"{e}",
            f"{data[0]}",
            f"{data[1]}",
            f"{data[4]}"
        ])
        capture_positive.release()

    with open(f"results2.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(export_data)
