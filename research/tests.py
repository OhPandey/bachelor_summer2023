import csv
import time
import cv2
import numpy


def feature_matching(current_frame: numpy, distance_threshold: float, object_threshold: int) -> []:
    def find_features() -> int:
        template = cv2.imread('../truetemplate.jpg', 0)
        sift = cv2.SIFT_create()
        kp1, des1 = sift.detectAndCompute(template, None)
        kp2, des2 = sift.detectAndCompute(current_frame, None)

        if des2 is not None:
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)

            goodMatches = []

            for i, pair in enumerate(matches):
                try:
                    m, n = pair
                    if m.distance <= distance_threshold * n.distance:
                        goodMatches.append(m)
                except ValueError:
                    pass

            return len(goodMatches)

        return 0

    value = find_features()

    return [bool(value >= object_threshold), value]


def analysing_feature_matching(capture, distance_threshold: float, object_threshold: int):
    print("-- START of Analysing Feature Matching --")

    # To generate average time
    time_arrays = []

    # To count the frames
    count = 0

    # Actual data gathered
    trues = 0
    true_matches = []
    falses = 0
    false_matches = []

    while capture.isOpened():
        ret, frame = capture.read()

        if not ret:
            print("End of stream")
            break

        start = time.time()
        result = feature_matching(frame, distance_threshold, object_threshold)
        end = round(time.time() - start, 3)

        if result[0]:
            trues += 1
            true_matches.append(result[1])
        else:
            falses += 1
            false_matches.append(result[1])

        time_arrays.append(end)
        count += 1
        print(f'[Frame {count}] Result: {result[0]} (Matches: {result[1]}), Time: {end}')

    if count >= 0:
        average_time = numpy.average(time_arrays)
        if trues == 0:
            average_true_matches = 0
        else:
            average_true_matches = numpy.average(true_matches)

        if falses == 0:
            average_false_matches = 0
        else:
            average_false_matches = numpy.average(false_matches)

        average_matches = numpy.average(true_matches + false_matches)

        recall = trues/count

        print(f"-- Results --")
        print(f"Settings: distance_threshold: {distance_threshold}, object_threshold: {object_threshold}")
        print(f"Frames analysed: {count}")
        print(f"Average processing time: {average_time}")
        print(f"Detected: {trues}")
        print(f"Average matches when detected: {average_true_matches}")
        print(f"Not detected: {falses}")
        print(f"Average matches when not detected: {average_false_matches}")
        print(f"Overall average matches:{average_matches}")
        print(f"Recall: {recall}")
        print("-- END of Analysing Feature Matching --")
        return [count, average_time, trues, falses, average_true_matches, average_false_matches, recall]
    else:
        return [0, 0, 0, 0, 0, 0]


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

    for e in range(1, iterations+1):
        print(f"-- Run {e} --")
        capture_positive = cv2.VideoCapture('../testing_movies/one.mov')
        data = analysing_feature_matching(capture_positive, 0.5, 10)
        export_data.append([
            f"{e}",
            f"{data[0]}",
            f"{data[1]}",
            f"{data[6]}"
        ])
        capture_positive.release()

    for e in range(1, iterations + 1):
        print(f"-- Run {e} --")
        capture_positive = cv2.VideoCapture('../testing_movies/two.mov')
        data = analysing_feature_matching(capture_positive, 0.5, 10)
        export_data.append([
            f"{e}",
            f"{data[0]}",
            f"{data[1]}",
            f"{data[6]}"
        ])
        capture_positive.release()

    for e in range(1, iterations + 1):
        print(f"-- Run {e} --")
        capture_positive = cv2.VideoCapture('../testing_movies/three.mov')
        data = analysing_feature_matching(capture_positive, 0.5, 10)
        export_data.append([
            f"{e}",
            f"{data[0]}",
            f"{data[1]}",
            f"{data[6]}"
        ])
        capture_positive.release()

    with open(f"results.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(export_data)


