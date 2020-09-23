import time as _time

import aubio
import pyaudio
import numpy as np


class BeatDetector:

    def __init__(self,  callback):
        self.callback = callback
        self.beat_number = 0
        self.win_s = 1024  # fft size
        self.hop_s = self.win_s // 2  # hop size
        self.pyaudio_format = pyaudio.paFloat32
        self.p = pyaudio.PyAudio()

    def __invoke_external_callback(self):
        self.callback(self.beat_number)
        self.beat_number += 1

    def __callback_internal(self, _in_data, _frame_count, _time_info, _status):
        samples, read = self.a_source()
        is_beat = self.a_tempo(samples)
        if is_beat:
            self.__invoke_external_callback()

        audiobuf = samples.tobytes()
        if read < self.hop_s:
            return audiobuf, pyaudio.paComplete

        return audiobuf, pyaudio.paContinue

    def play_captured(self):
        samplerate = 44100
        n_channels = 1
        buffer_size = 512

        stream = self.p.open(
            format=self.pyaudio_format,
            channels=n_channels,
            rate=samplerate,
            input=True,
            frames_per_buffer=buffer_size)

        self.a_tempo = aubio.tempo(
            "default",
            self.win_s,
            self.hop_s,
            samplerate
        )

        while True:
            try:
                audiobuffer = stream.read(buffer_size)
                signal = np.fromstring(audiobuffer, dtype=np.float32)

                is_beat = self.a_tempo(signal)
                if is_beat:
                    self.__invoke_external_callback()

            except KeyboardInterrupt:
                print("*** Ctrl+C pressed, exiting")
                break

    def play_audio_file(self, file):

        samplerate = 0
        frames_per_buffer = self.hop_s
        n_channels = 1

        self.a_tempo = aubio.tempo(
            "default",
            self.win_s,
            self.hop_s,
            samplerate
        )

        self.a_source = aubio.source(
            file,
            samplerate,
            self.hop_s
        )

        samplerate = self.a_source.samplerate
        stream = self.p.open(
            format=self.pyaudio_format,
            channels=n_channels,
            rate=samplerate,
            output=True,
            frames_per_buffer=frames_per_buffer,
            stream_callback=self.__callback_internal
        )

        stream.start_stream()

        while stream.is_active():
            _time.sleep(0.1)

        stream.stop_stream()
        stream.close()
        self.p.terminate()
