import datetime
import logging
import os
from pathlib import Path

import aiofiles
import cv2
from fastapi import UploadFile
from fastapi.concurrency import run_in_threadpool

from config.env import get_env


async def analyze_video(file: UploadFile):
    try:
        async with aiofiles.tempfile.NamedTemporaryFile("wb", delete=False) as temp:
            try:
                contents = await file.read()
                await temp.write(contents)
            except Exception:
                return {"message": "There was an error uploading the file"}
            finally:
                await file.close()

        # capture_video(temp.name)
        res = await run_in_threadpool(capture_video, temp.name)  # Pass temp.name to VideoCapture()
    except Exception:
        return {"message": "There was an error processing the file"}
    finally:
        os.remove(temp.name)

    return res


def capture_video(video_path: str, show_info: bool = True, interval: int = 5000, width: int = 640, height: int = 480):
    cap = cv2.VideoCapture(filename=video_path, apiPreference=cv2.CAP_ANY)
    fps = cap.get(cv2.CAP_PROP_FPS)

    if show_info:
        print('Frame width:', int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
        print('Frame height:', int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        print('Frame count:', int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))

        print('FPS:', fps)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    resource_path = get_env().resource_path

    capture_save_path = Path(resource_path)

    read_success = True
    pos_msec = 0
    dir_name = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    dir_path = capture_save_path.joinpath(dir_name)
    dir_path.mkdir()

    while read_success:
        read_success, frame = cap.read()
        full_path = get_capture_name(dir_path, pos_msec)
        cv2.imwrite(str(full_path), frame)
        if show_info:
            if read_success:
                logging.info(("capture success {}", full_path))
            else:
                logging.info(("capture failed {}", full_path))

        pos_msec += interval
        cap.set(cv2.CAP_PROP_POS_MSEC, pos_msec)

    cap.release()

    return dir_path


def get_capture_name(dir_path: Path, pos_msec: int) -> Path:
    pos_second = int(pos_msec / 1000)
    full_path = dir_path.joinpath(str(pos_second) + ".png")
    return full_path
