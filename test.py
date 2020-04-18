import numpy as np
import imutils
import pickle
import cv2
import os

def main(image_path):
    detector = "face_detection_model"
    embedding_model = "openface_nn4.small2.v1.t7"
    recognizer = "output/recognizer.pickle"
    le = "output/le.pickle"

    print("[INFO] loading face detector...")
    protoPath = os.path.sep.join([detector, "deploy.prototxt"])
    modelPath = os.path.sep.join([detector,
        "res10_300x300_ssd_iter_140000.caffemodel"])
    detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

    print("[INFO] loading face recognizer...")
    embedder = cv2.dnn.readNetFromTorch(embedding_model)

    recognizer = pickle.loads(open(recognizer, "rb").read())
    le = pickle.loads(open(le, "rb").read())

    image = cv2.imread(image_path)
    image = imutils.resize(image, width=600)
    (h, w) = image.shape[:2]

    imageBlob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)), 1.0, (300, 300),
        (104.0, 177.0, 123.0), swapRB=False, crop=False)

    detector.setInput(imageBlob)
    detections = detector.forward()

    ans = 0

    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.4:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            face = image[startY:endY, startX:endX]
            (fH, fW) = face.shape[:2]

            if fW < 20 or fH < 20:
                continue

            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
                (0, 0, 0), swapRB=True, crop=False)
            embedder.setInput(faceBlob)
            vec = embedder.forward()

            preds = recognizer.predict_proba(vec)[0]
            j = np.argmax(preds)
            proba = preds[j]
            name = le.classes_[j]

            text = "{}: {:.2f}%".format(name, proba * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(image, (startX, startY), (endX, endY),
                (0, 0, 255), 2)
            cv2.putText(image, text, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            #print(name)
            #print(proba * 100)
            ans = proba * 100
            

    cv2.imwrite("static/output/output.jpg", image)
    cv2.waitKey(0)
    return ans

if __name__ == "__main__":
    print(main("check.jpg"))
