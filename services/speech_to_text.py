import datetime
import io
import math
import tempfile
from pathlib import Path

from fastapi import UploadFile
from google.cloud import speech
from moviepy.editor import AudioClip, VideoFileClip

from config.env import get_env
from services.voice_analyzing import analyse_sound, Data


async def transcript(file: UploadFile, interval: int = 50):
    if interval > 55:
        raise ValueError("PLEASE TYPE interval less than 55")
    with tempfile.NamedTemporaryFile("wb", delete=False) as temp:
        try:
            await file.seek(0)
            contents = await file.read()
            temp.write(contents)
        except Exception as exception:
            print({"message": "There was an error uploading the file"})
            raise exception
        finally:
            pass

    save_path = Path(get_env().resource_path)
    dir_name = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S_audio"))
    dir_path = save_path.joinpath(dir_name)
    dir_path.mkdir()

    video_file_clip = VideoFileClip(temp.name)
    audio_file_clip = video_file_clip.audio

    subclips = subclip_for_api(audio_file_clip, interval=interval)

    paths = write_subclips(subclips, dir_path)

    voice_data_list = analyze_voices(paths)
    high, thick, clean, intensity = get_voice_score(voice_data_list)
    print(f"@@\t mean : h{high}, t{thick}, c{clean}, i{intensity}")
    high_n = (high / 150) * 100
    thick_n = (thick + 15) / 30 * 100
    clean_n = (clean + 15) / 30 * 100
    intensity_n = intensity

    responses = call_google_api(paths)
    results = list(map(lambda r: r.result(), responses))
    full_text = ""
    for result in results:
        # result: speech.LongRunningRecognizeResponse
        for texts in result.results:
            if len(texts.alternatives) >= 1:
                transcript_text = texts.alternatives[0].transcript
                confidence = texts.alternatives[0].confidence
                print(f"@@ \tconfidence: {confidence}, transcript: {transcript_text}")
                if len(transcript_text) > 0:
                    full_text += transcript_text
    print(f"@@ \ttranscri pt DONE")
    temp.close()
    print(f"@@ \tfull_text : {full_text}")
    return full_text, high_n, thick_n, clean_n, intensity_n


def subclip_for_api(full_clip: AudioClip, interval: int = 50) -> list[AudioClip]:
    clips: list[AudioClip] = []
    print(f"@@\t [ duration: {full_clip.duration}, interval : {interval} ]")

    if full_clip.duration < interval:
        print(f"@@ \tuse full clip for transcript. clip less than {interval}")
        clips.append(full_clip)
        return clips

    for t_start, t_end in range_for_subclip(math.floor(full_clip.duration), interval):
        print(f"@@ \tt_start : {t_start}, t_end : {t_end}")
        subclip = full_clip.subclip(t_start, t_end)
        clips.append(subclip)

    print(f"@@ \tmake subclip DONE, interval :{interval}")
    return clips


def range_for_subclip(duration: int, step: int):
    t_start = 0
    for t_end in range(step, duration, step):
        yield t_start, t_end
        t_start += step
    if t_start < duration < (t_start + step):
        yield t_start, duration


def get_capture_name(dir_path: Path, i: int) -> Path:
    pos_second = i
    full_path = dir_path.joinpath(str(pos_second) + ".wav")
    return full_path


def write_subclips(subclips: list[AudioClip], dir_path: Path) -> list[Path]:
    paths = []
    i = 0
    for subclip in subclips:
        full_path = get_capture_name(dir_path, i)
        subclip.write_audiofile(full_path)
        paths.append(full_path)
        i += 1
    print(f"@@ \twrite subclip to file DONE")
    return paths


def call_google_api(paths: list[Path]) -> list:
    client = speech.SpeechClient()
    input_config = speech.RecognitionConfig(
        language_code="ko-KR",
        alternative_language_codes=["en-US", ],
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        audio_channel_count=2,
        enable_automatic_punctuation=True,
        model="latest_long",
    )
    output_config = speech.TranscriptOutputConfig()

    responses = []
    for path in paths:
        with io.open(path, "rb") as content:
            audio = speech.RecognitionAudio(content=content.read())
            recognize_request = speech.LongRunningRecognizeRequest(config=input_config, audio=audio,
                                                                   output_config=output_config)
        response = client.long_running_recognize(request=recognize_request)
        print(f"@@ \tapi called, path : {path}")
        responses.append(response)
    print(f"@@ \tapi called DONE")
    return responses


def analyze_voices(paths: list[Path]) -> list[Data]:
    list = []
    for path in paths:
        data = analyse_sound(path)
        print(
            f"@@ \tvoice data \n\t\tduration : {data.get_duration()}\n\t\thigh : {data.get_high()}, \n\t\tclean : {data.get_clean()}, \n\t\tthick : {data.get_thick()}, \n\t\tintensity : {data.get_intensity()}")
        list.append(data)
    print(f"@@\t analyze voice DONE")
    return list


def get_voice_score(list: list[Data]):
    high_result = 0.0
    thick_result = 0.0
    clean_result = 0.0
    intensity_result = 0.0
    duration_result = 0.0

    for data in list:
        duration = data.get_duration()
        high = data.get_high()
        thick = data.get_thick()
        clean = data.get_clean()
        intensity = data.get_intensity()

        high_result += high * duration
        thick_result += thick * duration
        clean_result += clean * duration
        intensity_result += intensity * duration
        duration_result += duration

    return high_result / duration_result, thick_result / duration_result, clean_result / duration_result, intensity_result / duration_result
