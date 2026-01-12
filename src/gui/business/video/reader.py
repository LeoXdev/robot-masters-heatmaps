import cv2
import numpy as np

def read_frame(video_capture, frame_index) -> np.ndarray:
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
    ok, frame = video_capture.read()
    if not ok:
        return None
    return frame

def get_total_frames(video_capture) -> int:
    # these two methods are not always accurate
    #return int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    #video_capture.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
    #return int(video_capture.get(cv2.CAP_PROP_POS_FRAMES))

    # in practice, it should not be necessary to preserve the position of the video capture
    # as every frame read attempt re-establishes the position (video.reader.read_frame)
    pos = int(video_capture.get(cv2.CAP_PROP_POS_FRAMES))

    count = 0
    while True:
        ok, _ = video_capture.read()
        if not ok:
            break
        count += 1

    video_capture.set(cv2.CAP_PROP_POS_FRAMES, pos)
    return count

def get_video_shape(video_capture) -> tuple[int, int]:
    """
    get_video_shape takes a video capture and returns the dimensions of its source in (h, w) format.
    """
    return (
        int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    )
