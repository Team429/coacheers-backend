from pathlib import Path

import parselmouth
from parselmouth.praat import call


class Data:
    f0_mean: float
    localJitter: float
    localabsoluteJitter: float
    rapJitter: float
    ppq5Jitter: float
    localShimmer: float
    localdbShimmer: float
    apq3Shimmer: float
    aqpq5Shimmer: float
    apq11Shimmer: float
    hnr05: float
    hnr15: float
    hnr25: float
    hnr35: float
    hnr38: float
    ltas: float
    intensity: float
    cpp: float

    def get_clean(self):
        return self.cpp

    def get_thick(self):
        return self.ltas

    def get_high(self):
        return self.f0_mean

    def get_intensity(self):
        return self.intensity


def analyse_sound(filepath: Path) -> Data:
    return measurePitch(str(filepath), 75, 1000)


def measurePitch(voiceID, f0min, f0max) -> Data:
    sound = parselmouth.Sound(voiceID)  # read the sound
    print(sound.duration)
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max)
    f0_mean = call(pitch, "Get mean", 0, 0, "Hertz")
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)  # create a praat pitch object
    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer = call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    aqpq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq11Shimmer = call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    harmonicity05 = call(sound, "To Harmonicity (cc)", 0.01, 500, 0.1, 1.0)
    hnr05 = call(harmonicity05, "Get mean", 0, 0)
    harmonicity15 = call(sound, "To Harmonicity (cc)", 0.01, 1500, 0.1, 1.0)
    hnr15 = call(harmonicity15, "Get mean", 0, 0)
    harmonicity25 = call(sound, "To Harmonicity (cc)", 0.01, 2500, 0.1, 1.0)
    hnr25 = call(harmonicity25, "Get mean", 0, 0)
    harmonicity35 = call(sound, "To Harmonicity (cc)", 0.01, 3500, 0.1, 1.0)
    hnr35 = call(harmonicity35, "Get mean", 0, 0)
    harmonicity38 = call(sound, "To Harmonicity (cc)", 0.01, 3800, 0.1, 1.0)
    hnr38 = call(harmonicity38, "Get mean", 0, 0)

    longTermAvarageSpectrumSlope = call(sound, "To Ltas", 3800)
    ltas = call(longTermAvarageSpectrumSlope, "Get mean", 0, 0, "dB")  # energy, sones, dB

    intensity = call(sound, "Get intensity (dB)")

    power_cepstrogram = call(sound, "To PowerCepstrogram", 60, 0.01, f0max, 50)
    cpp = call(power_cepstrogram, "Get CPPS", True, 0.01, 0.001, 60.0, 330.0, 0.005, 'parabolic', 0.001, 0.05,
               "Exponential decay",
               "Robust slow")

    data = Data()
    data.f0_mean = f0_mean
    data.localJitter = localJitter,
    data.localabsoluteJitter = localabsoluteJitter
    data.rapJitter = rapJitter
    data.ppq5Jitter = ppq5Jitter
    data.localShimmer = localShimmer
    data.localdbShimmerdata = localdbShimmer
    data.apq3Shimmer = apq3Shimmer
    data.aqpq5Shimmer = aqpq5Shimmer
    data.apq11Shimmer = apq11Shimmer
    data.hnr05 = hnr05
    data.hnr15 = hnr15
    data.hnr25 = hnr25
    data.hnr35 = hnr35
    data.hnr38 = hnr38
    data.ltas = ltas
    data.intensity = intensity
    data.cpp = cpp

    return data

# 청음/탁음 : BW2, CPP
# 가늘다/굵다 : sAPQ, SPI, LTAS, H1-A2
# 높낮이 : F0_mean, Jitter, LTAS, SPI
# 세기 : Intensity, H1, H2, A1, A2, A3, H2K, HNR05~35

# BW 1~4 = 대역폭

# https://koreascience.kr/article/JAKO201707851601923.pdf
