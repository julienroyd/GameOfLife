import simpleaudio as sa
import os

class SoundManager(object):

    def __init__(self, sound_dir):

        self.sound_dir = sound_dir
        self.all_wav_files = sorted([file for file in os.listdir(self.sound_dir) if file.endswith('.wav')],
                                    key=lambda item: (int(item.partition('_')[0]), item))
        self.all_wave_obj = [sa.WaveObject.from_wave_file(os.path.join('assets', 'notes', wav_file))
                            for wav_file in self.all_wav_files]
        self.n_sounds = len(self.all_wave_obj)

    def play_sound(self, i, wait=False):
        play_obj = self.all_wave_obj[i].play()
        if wait:
            play_obj.wait_done()

# if False:
#     # =================================================================================
#     # EXAMPLE 1: with numpy
#     import numpy as np
#     import simpleaudio as sa
#
#     # calculate note frequencies
#     A_freq = 440
#     Csh_freq = A_freq * 2 ** (4 / 12)
#     E_freq = A_freq * 2 ** (7 / 12)
#
#     # get timesteps for each sample, T is note duration in seconds
#     sample_rate = 44100
#     T = 0.25
#     t = np.linspace(0, T, T * sample_rate, False)
#
#     # generate sine wave notes
#     A_note = np.sin(A_freq * t * 2 * np.pi)
#     Csh_note = np.sin(Csh_freq * t * 2 * np.pi)
#     E_note = np.sin(E_freq * t * 2 * np.pi)
#
#     # concatenate notes
#     audio = np.hstack((A_note, Csh_note, E_note))
#     # normalize to 16-bit range
#     audio *= 32767 / np.max(np.abs(audio))
#     # convert to 16-bit data
#     audio = audio.astype(np.int16)
#
#     # start playback
#     play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
#
#     # wait for playback to finish before exiting
#     play_obj.wait_done()
#
# else:
#     # =================================================================================
#     # EXAMPLE 1: with .wav files
#     import simpleaudio as sa
#     import os
#     import time
#
#     all_wav_notes = [file for file in os.listdir(os.path.join('assets', 'notes')) if file.endswith('.wav')]
#     sorted_wav_notes = sorted(all_wav_notes, key=lambda item: (int(item.partition('_')[0]), item))
#     all_wave_obj = [sa.WaveObject.from_wave_file(os.path.join('assets', 'notes', wav_file))
#                     for wav_file in sorted_wav_notes]
#     for wave_obj in all_wave_obj:
#         play_obj = wave_obj.play()
#         time.sleep(0.2)
#         # play_obj.wait_done()