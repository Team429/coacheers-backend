# TODO: google vision testing & implementing
# from google.cloud import videointelligence_v1 as videointelligence
#
#
# def detect_faces(gcs_uri="gs://YOUR_BUCKET_ID/path/to/your/video.mp4"):
#     """Detects faces in a video."""
#
#     client = videointelligence.VideoIntelligenceServiceClient()
#
#     # Configure the request
#     config = videointelligence.FaceDetectionConfig(
#         include_bounding_boxes=True, include_attributes=True
#     )
#     context = videointelligence.VideoContext(face_detection_config=config)
#
#     # Start the asynchronous request
#     operation = client.annotate_video(
#         request={
#             "features": [videointelligence.Feature.FACE_DETECTION],
#             "input_uri": gcs_uri,
#             "video_context": context,
#         }
#     )
#
#     print("\nProcessing video for face detection annotations.")
#     result = operation.result(timeout=300)
#
#     print("\nFinished processing.\n")
#
#     # Retrieve the first result, because a single video was processed.
#     annotation_result = result.annotation_results[0]
#
#     for annotation in annotation_result.face_detection_annotations:
#         print("Face detected:")
#         for track in annotation.tracks:
#             print(
#                 "Segment: {}s to {}s".format(
#                     track.segment.start_time_offset.seconds
#                     + track.segment.start_time_offset.microseconds / 1e6,
#                     track.segment.end_time_offset.seconds
#                     + track.segment.end_time_offset.microseconds / 1e6,
#                 )
#             )
#
#             # Each segment includes timestamped faces that include
#             # characteristics of the face detected.
#             # Grab the first timestamped face
#             timestamped_object = track.timestamped_objects[0]
#             box = timestamped_object.normalized_bounding_box
#             print("Bounding box:")
#             print("\tleft  : {}".format(box.left))
#             print("\ttop   : {}".format(box.top))
#             print("\tright : {}".format(box.right))
#             print("\tbottom: {}".format(box.bottom))
#
#             # Attributes include glasses, headwear, smiling, direction of gaze
#             print("Attributes:")
#             for attribute in timestamped_object.attributes:
#                 print(
#                     "\t{}:{} {}".format(
#                         attribute.name, attribute.value, attribute.confidence
#                     )
#                 )