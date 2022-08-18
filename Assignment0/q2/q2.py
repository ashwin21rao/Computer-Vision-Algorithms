import cv2
import os
import shutil


def captureWebcam(save_path):
    video = cv2.VideoCapture(0)

    # fps of webcam
    print(video.get(5))

    # empty contents of save_path or create it
    if os.path.exists(save_path) and os.path.isdir(save_path):
        shutil.rmtree(save_path)
    os.makedirs(save_path)

    # process video frame by frame
    frame_num = 1
    while True:
        ret, frame = video.read()
        if not ret:
            break

        # write frame to file
        cv2.imwrite(os.path.join(save_path, f"frame{str(frame_num).zfill(6)}.png"), frame)
        frame_num += 1

        # display frame
        cv2.imshow("webcam", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    video.release()


frames_path = "frames"
captureWebcam(frames_path)
