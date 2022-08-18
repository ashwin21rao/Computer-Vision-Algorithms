import cv2
import numpy as np


def removeGreenScreen(video_path, background_path, output_path):
    # foreground
    video1 = cv2.VideoCapture(video_path)
    width = int(video1.get(3))
    height = int(video1.get(4))

    # background
    video2 = cv2.VideoCapture(background_path)

    # combined video
    fps = int(video1.get(5))
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # process video frame by frame
    frame_num = 0
    while True:
        ret1, frame1 = video1.read()

        ret2, frame2 = video2.read()
        frame2 = cv2.resize(frame2, (width, height), interpolation=cv2.INTER_AREA)

        if not ret1 or not ret2:
            break

        # generate mask
        l_green = np.array([0, 80, 0])
        u_green = np.array([85, 255, 85])
        mask = cv2.inRange(frame1, l_green, u_green)

        if frame_num == 120:
            cv2.imwrite("orig.png", frame1)
            cv2.imwrite("bg.png", frame2)

        # apply mask
        frame1[mask != 0] = frame2[mask != 0]

        # display frame
        cv2.imshow("video", frame1)
        if cv2.waitKey(1) == ord('q'):
            break

        # write frame to video
        out.write(frame1)

        if frame_num == 120:
            cv2.imwrite("new.png", frame1)
        frame_num += 1

    video1.release()
    video2.release()
    out.release()


removeGreenScreen("video.mp4", "background_long.mp4", "combined.mp4")
