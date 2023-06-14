import os

import numpy as np
import tensorflow as tf
from object_detection.builders import model_builder
from object_detection.utils import config_util

from lib.debugging.debugging import Debugging
from lib.detector.detector import Detector
from lib.utils.position import Position


class DLDetector(Detector, Debugging):
    def __init__(self, frame):
        # Load model
        self.configs = config_util.get_configs_from_pipeline_file(os.path.join('model', 'ssd-100', 'pipeline.config'))
        self.detection_model = model_builder.build(model_config=self.configs['model'], is_training=False)
        # Restore checkpoint
        self.ckpt = tf.compat.v2.train.Checkpoint(model=self.detection_model)
        self.ckpt.restore(os.path.join('model', 'ssd-100', 'ckpt-3')).expect_partial()

        super().__init__(frame)

    @tf.function
    def detect_fn(self, tensor_image):
        image, shapes = self.detection_model.preprocess(tensor_image)
        prediction_dict = self.detection_model.predict(image, shapes)
        detections = self.detection_model.postprocess(prediction_dict, shapes)
        return detections

    @property
    def card(self) -> Position | None:
        """
        Getter method for the card position

        This method returns the location of the student card, represented as a `Position` object.
        If the card location has not been determined yet, the method performs the necessary checks
        and calculations to determine the card's position based on the detected face.

        :return: The location of the student card
        :rtype: Position
        """
        if self._card is None:
            if self._is_card():
                self._card = self.potential_position
                return self._card

        return self._card

    def _is_card(self) -> bool:
        input_tensor = tf.convert_to_tensor(np.expand_dims(self.frame, 0), dtype=tf.float32)
        detections = self.detect_fn(input_tensor)
        num_detections = int(detections.pop('num_detections'))

        detections = {key: value[0, :num_detections].numpy()
                      for key, value in detections.items()}
        detections['num_detections'] = num_detections

        detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

        detection_boxes = detections['detection_boxes']
        detection_scores = detections['detection_scores']
        for i in range(num_detections):
            score = detection_scores[i]
            print(score)
            if score > 0.5:
                y1, x1, y2, x2 = detection_boxes[i]
                h, w, z = self.frame.shape

                x1 = int(x1 * w)
                y1 = int(y1 * h)
                x2 = int(x2 * w)
                y2 = int(y2 * h)
                self.potential_position = Position(x1, y1, x2, y2)
                return True
        return False
