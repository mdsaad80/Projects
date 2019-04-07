import cv2

cap = cv2.VideoCapture('vid.mp4')
count = 0

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        cv2.imwrite('new/frame{:d}.jpg'.format(count), frame)
        count += 1 # i.e. at 30 fps, this advances one second
        cap.set(1, count)
    else:
        cap.release()
        break
