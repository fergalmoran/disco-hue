import time as _time

import aubio
import pyaudio


class BeatDetector:

    def __init__(self,  callback):
        self.callback = callback
        self.beat_number = 0
        self.win_s = 1024  # fft size
        self.hop_s = self.win_s // 2  # hop size

    def __callback_internal(self, _in_data, _frame_count, _time_info, _status):
        samples, read = self.a_source()
        is_beat = self.a_tempo(samples)
        if is_beat:
            self.callback(self.beat_number)
            self.beat_number += 1

        audiobuf = samples.tobytes()
        if read < self.hop_s:
            return audiobuf, pyaudio.paComplete

        return audiobuf, pyaudio.paContinue


    def play_audio_file(self, file):

        samplerate = 44100
        pyaudio_format = pyaudio.paFloat32
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
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio_format,
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
        p.terminate()


