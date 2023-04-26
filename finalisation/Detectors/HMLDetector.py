import cv2

from finalisation.Detectors.Detector import Detector


# This is a mix of machine learning and non-machine learning approach (Half machine-learning - HML)
# It checks the card in a normal non-machine learning approach
# but takes advantage of the face recognition (that is easily available) to find the card position
class HMLDetector(Detector):
    def isStudentCard(self):
        if self._findFeatures() >= 10:
            print('YES!')
            return True

        return False

    def print(self, fname):
        cv2.putText(self.frame, str(self.getQuality()), (0, 100), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 3)
        cv2.imwrite(fname, self.frame)

    def _findFeatures(self):
        template = cv2.imread(self.template, 0)
        sift = cv2.SIFT_create()
        kp1, des1 = sift.detectAndCompute(template, None)
        kp2, des2 = sift.detectAndCompute(self.grayFrame, None)

        if des2 is not None:
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, des2, k=2)

            goodMatches = []

            for i, pair in enumerate(matches):
                try:
                    m, n = pair
                    if m.distance <= 0.5 * n.distance:
                        goodMatches.append(m)
                except ValueError:
                    pass
            print(len(goodMatches))
            return len(goodMatches)

        return 0

    def facePosition(self):
        faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml').detectMultiScale(self.frame, 1.1, 4)

        # Check for a face
        if len(faces) == 1:
            face = faces[0]

            # Check if the face is close enough
            if face[2] >= 80 and face[3] >= 80:
                offset = 20
                x1 = face[0] - offset
                y1 = face[1] - offset
                x2 = face[0] + face[2] + offset
                y2 = face[1] + face[3] + offset
                cv2.imwrite("Cropped Image.jpg", self.frame[y1:y2, x1:x2])

                self.facePosition = Position(x1, y1, x2, y2)

                if self.state == 'development':
                    cv2.rectangle(self.frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
