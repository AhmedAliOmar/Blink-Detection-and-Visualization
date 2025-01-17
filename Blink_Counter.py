import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
plotY = LivePlot(640, 360, [20, 50], invert=True)

idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
ratioList = []
blinkCounter = 0
counter = 0
color = (255, 0, 255)

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(img, tuple(face[id]), 5, color, cv2.FILLED)

        leftUp = tuple(face[159])
        leftDown = tuple(face[23])
        leftLeft = tuple(face[130])
        leftRight = tuple(face[243])
        lengthVer, _ = detector.findDistance(leftUp, leftDown)
        lengthHor, _ = detector.findDistance(leftLeft, leftRight)

        cv2.line(img, leftUp, leftDown, (0, 200, 0), 3)
        cv2.line(img, leftLeft, leftRight, (0, 200, 0), 3)

        ratio = int((lengthVer / lengthHor) * 100)
        ratioList.append(ratio)
        if len(ratioList) > 3:
            ratioList.pop(0)
        ratioAvg = sum(ratioList) / len(ratioList)

        if ratioAvg < 35 and counter == 0:
            blinkCounter += 1
            color = (0, 200, 0)
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (255, 0, 255)

        cv2.putText(img, f'Blink Count: {blinkCounter}', (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        imgPlot = plotY.update(ratioAvg, color)
        img = cv2.resize(img, (640, 360))
        # imgStack = cvzone.stackImages([img, imgPlot], 2, 1)
        imgStack = cv2.vconcat([img, imgPlot])
    else:
        img = cv2.resize(img, (640, 360))
        # imgStack = cvzone.stackImages([img, img], 2, 1)
        imgStack = cv2.vconcat([img, img])

    cv2.imshow("Image", imgStack)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
