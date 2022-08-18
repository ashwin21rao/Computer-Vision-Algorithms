import cv2
import os
import shutil


def splitVideoIntoFrames(video_path, save_path):
    video = cv2.VideoCapture(video_path)

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

    video.release()


def mergeFramesIntoVideo(img_path, video_path, fps=None):
    filename = os.listdir(img_path)[0]

    frame_num_len = None
    for i, c in enumerate(filename):
        if c.isdigit():
            frame_num_len = len(filename[i: filename.find(".")])
            break

    video = cv2.VideoCapture(os.path.join(img_path, f"frame%0{frame_num_len}d.png"))
    width = int(video.get(3))
    height = int(video.get(4))
    if fps is None:
        fps = int(video.get(5))

    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # process each frame
    while True:
        ret, frame = video.read()
        if not ret:
            break

        # write frame to video
        out.write(frame)

    video.release()
    out.release()


frames_path = "frames"
splitVideoIntoFrames("race.mp4", frames_path)
mergeFramesIntoVideo(frames_path, "merged.mp4", fps=20)
