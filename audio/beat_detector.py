import time as _time

import aubio
import pyaudio


class BeatDetector:

    def __init__(self, filename, callback):

        self.beat_number = 0

        self.win_s = 1024  # fft size
        self.hop_s = self.win_s // 2  # hop size
        self.filename = filename
        self.callback = callback
        self.samplerate = 0

        self.a_source = aubio.source(
            self.filename,
            self.samplerate,
            self.hop_s
        )

        self.samplerate = self.a_source.samplerate

        self.a_tempo = aubio.tempo(
            "default",
            self.win_s,
            self.hop_s,
            self.samplerate
        )

        self.pyaudio_format = pyaudio.paFloat32
        self.frames_per_buffer = self.hop_s
        self.n_channels = 1

    def start_playing(self):
        p = pyaudio.PyAudio()
        stream = p.open(
            format=self.pyaudio_format,
            channels=self.n_channels,
            rate=self.samplerate,
            output=True,
            frames_per_buffer=self.frames_per_buffer,
            stream_callback=self.pyaudio_callback
        )

        stream.start_stream()

        while stream.is_active():
            _time.sleep(0.1)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def pyaudio_callback(self, _in_data, _frame_count, _time_info, _status):
        samples, read = self.a_source()
        is_beat = self.a_tempo(samples)
        if is_beat:
            self.callback(self.beat_number)
            self.beat_number += 1

        audiobuf = samples.tobytes()
        if read < self.hop_s:
            return audiobuf, pyaudio.paComplete

        return audiobuf, pyaudio.paContinue
