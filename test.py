import cv2

from detector.cv_face_detector.model import CVFaceDetector
from models.m1.model import M1FaceAntiSpoofing
from models.m2.model import M2FaceAntiSpoofing

import os

face_detector = CVFaceDetector()
spoof_detectors = [M1FaceAntiSpoofing(), M2FaceAntiSpoofing()]

benchmark_dir = "benchmarks"
for spoof_detector in spoof_detectors:
    print("Start ----------------------------- ", type(spoof_detector))
    all_count = 0
    correct_count = 0
    errors = []
    for class_name in ["fake", "real"]:
        class_path = os.path.join(benchmark_dir, class_name)
        for image_name in os.listdir(class_path):
            image_path = os.path.join(class_path, image_name)

            bgr = cv2.imread(image_path)

            face_bboxes = face_detector.get_face_bboxes(bgr)

            for bbox in face_bboxes:
                real_score = spoof_detector.get_real_score(bgr, bbox)
                print("Real score for image name " + image_name + " in class " + class_name + " is: ",
                      real_score)

                if class_name == "fake":
                    if real_score < 0.5:
                        is_correct = True
                    else:
                        is_correct = False
                    errors.append(real_score)

                else:
                    if real_score >= 0.5:
                        is_correct = True
                    else:
                        is_correct = False
                    errors.append(1 - real_score)

                if is_correct:
                    correct_count+=1

                all_count+=1
                print("Correct prediction: ", is_correct)

    print("--- Total count: ", all_count)
    print("--- Correct count: ", correct_count)
    print("--- Average error: ", (sum(errors)/len(errors))*100,"%")
    print("End ----------------------------- ", type(spoof_detector))
