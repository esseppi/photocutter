import math

import cv2

inputY = 0
inputX = 0

# Height and width desired for final image
width, height = 733, 433
# Face detection library
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Upload image
path = "./face3.jpg"
img = cv2.imread(path)
cv2.imshow("original", img)
print("Original image" + str(img.shape))

# QUAL'E' IL LATO PIU' LUNGO
goldenRatio = height / width
inverseGoldenRatio = width / height
ratio = img.shape[0] / img.shape[1]
inverseRatio = img.shape[1] / img.shape[0]
print(str("Ratio:") + str(ratio))
print(str("Golden Ratio:") + str(goldenRatio))



# RESIZING
if ratio == goldenRatio:
    img = cv2.resize(img, (width, height))
elif ratio < height / width:
    this_height = img.shape[0]
    hratio = height / this_height
    img = cv2.resize(img, (math.floor(width * inverseRatio * goldenRatio), math.floor(this_height * hratio)))
elif ratio > height / width:
    this_width = img.shape[1]
    wratio = width / this_width
    img = cv2.resize(img, (math.floor(this_width * wratio), math.floor(height * ratio * inverseGoldenRatio)))
print("Resized image" + str(img.shape))

# CUTTING
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
# face detection
if len(faces) > 0:
    for (x, y, w, h) in faces:
        _y = y + h / 2
        _x = x + w / 2
    if ratio < height / width:

        if _x - width / 2 > 0 and _x + width / 2 < img.shape[1]:
            x1 = math.floor(_x - width / 2)
            x2 = math.floor(_x + width / 2)
        elif _x - width / 2 < 0:
            x1 = 0
            x2 = width
        elif _x + width / 2 > img.shape[1]:
            plus = img.shape[1] - width
            x1 = _x - width / 2 - plus
            x2 = img.shape[1]
        imgCropped = img[0: height, math.floor(x1):math.floor(x2)]
        cv2.imshow("Final", imgCropped)
    elif ratio > height / width:
        if _y - height / 2 > 0 and _y + height / 2 < img.shape[0]:
            y1 = math.floor(_y - height / 2)
            y2 = math.floor(_y + height / 2)
        elif _y - height / 2 < 0:
            y1 = 0
            y2 = height
        elif _y + height / 2 > img.shape[0]:
            plus = img.shape[0] - height
            y1 = _y - height / 2 - plus
            y2 = img.shape[0]
        imgCropped = img[y1:y2, 0: width]
        cv2.imshow("Final", imgCropped)
    else:
        imgCropped = img[0: height, 0: width]
        cv2.imshow("Final", imgCropped)
    print("Cropped image" + str(imgCropped.shape))
# If no faces are detected or changed by user with input
if len(faces) == 0 or inputX or inputY:
    if inputX is not None or inputY is not None:
        # Security check
        if float(inputX) + float(width) > math.floor(img.shape[1]):
            inputX = math.floor(img.shape[1] - width)
        if float(inputY) + float(height) >= math.floor(img.shape[0]):
            inputY = math.floor(img.shape[0] - height)

    if ratio > height / width:
        if not inputY:
            y1 = math.floor((img.shape[0] - height) / 2)
            y2 = math.floor((img.shape[0] + height) / 2)
        else:
            y1 = inputY
            y2 = inputY + height
        imgCropped = img[y1:y2, 0: width]
    elif ratio < height / width:
        if inputX:
            x1 = inputX
            x2 = inputX + width
        else:
            x1 = math.floor((img.shape[1] - width) / 2)
            x2 = math.floor((img.shape[1] + width) / 2)

        imgCropped = img[0: height, x1:x2]
    else:
        imgCropped = img

    cv2.imshow("Final", imgCropped)
    print("Cutted image" + str(imgCropped.shape))
    print("No faces detected")

if len(faces) > 0:
    facedImg = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imshow("FaceDetect sized", facedImg)

print('newRatio: ' + str(imgCropped.shape[0] / imgCropped.shape[1]))
cv2.waitKey(0)
