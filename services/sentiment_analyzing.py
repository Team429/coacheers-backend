import datetime
import os
from pathlib import Path
from typing import Optional

import aiofiles
import cv2
from fastapi import UploadFile
from fastapi.concurrency import run_in_threadpool
from google.cloud import vision

from config.env import get_env


async def analyze_video(file: UploadFile) -> tuple[Path, list]:
    try:
        async with aiofiles.tempfile.NamedTemporaryFile("wb", delete=False) as temp:
            try:
                await file.seek(0)
                contents = await file.read()
                await temp.write(contents)
            except Exception as exception:
                print({"message": "There was an error uploading the file"})
                raise exception
            finally:
                pass

        res, faces = await run_in_threadpool(capture_video, temp.name)  # Pass temp.name to VideoCapture()
    except Exception as exception:
        print({"message": "There was an error processing the file"})
        raise exception
    finally:
        os.remove(temp.name)

    return res, faces


def capture_video(video_path: str, show_info: bool = True, interval_msec: int = 5 * 1000,
                  width: int = 640, height: int = 480) -> tuple[Path, list]:
    cap = cv2.VideoCapture(filename=video_path, apiPreference=cv2.CAP_ANY)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_length_sec = (frame_count / fps)
    interval_sec = (interval_msec / 1000)
    capture_limit_count = video_length_sec / interval_sec

    resource_path = get_env().resource_path
    capture_save_path = Path(resource_path)

    dir_name = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    dir_path = capture_save_path.joinpath(dir_name)
    dir_path.mkdir()

    if show_info:
        print('Frame width:', int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
        print('Frame height:', int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        print('Frame count:', frame_count)
        print('FPS:', fps)
        print('Save path:', str(dir_path))

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)  # seems doesn't work in video file
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  # seems doesn't work in video file

    pos_msec = 0  # start position
    faces = []  # list[Face]
    read_success, frame = cap.read()  # execute capture
    capture_count = 1  # count capture
    try:
        while read_success & capture_count <= capture_limit_count:
            full_path = get_capture_name(dir_path, pos_msec)
            cv2.imwrite(str(full_path), frame)
            frame_bytes = cv2.imencode('.png', frame)[1].tobytes()

            face = detect_face(frame_bytes)
            if face:
                faces.append(face)  # save to array
            if show_info:
                print(f"full_path: ${full_path}")

            pos_msec += interval_msec
            cap.set(cv2.CAP_PROP_POS_MSEC, pos_msec)  # video skip
            read_success, frame = cap.read()
            capture_count += 1

    except Exception as exception:
        print(f"EXCEPTION {exception}")
    finally:
        cap.release()  # capture close

    if show_info:
        for face_info in faces:
            print("{")
            print(f"\tjoy: {face_info.joy}")
            print(f"\tsorrow {face_info.sorrow}")
            print(f"\tanger {face_info.anger}")
            print(f"\tsurprise {face_info.surprise}")
            print("}")

    return dir_path, faces


def get_capture_name(dir_path: Path, pos_msec: int) -> Path:
    pos_second = int(pos_msec / 1000)
    full_path = dir_path.joinpath(str(pos_second) + ".png")
    return full_path


class Face_DTO:
    joy: int
    sorrow: int
    anger: int
    surprise: int

    def __init__(self, face: vision.FaceAnnotation):
        self.anger = int(face.anger_likelihood)
        self.joy = int(face.joy_likelihood)
        self.surprise = int(face.surprise_likelihood.value)
        self.sorrow = int(face.sorrow_likelihood.value)


def detect_face(file_bytes, max_results=4) -> Optional[Face_DTO]:
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=file_bytes)

    response = client.face_detection(image=image, max_results=max_results)
    faces = response.face_annotations

    if len(faces) > 0:
        face = faces[0]
        print("Face detected!")
        print(f"\tdetect_confidence: {face.detection_confidence}")
        vertices = (['({},{})'.format(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices])
        print("\tface bounds: {}".format(','.join(vertices)))
        return Face_DTO(face)
    else:
        return None
