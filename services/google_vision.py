from typing import Optional

from google.cloud import vision


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
