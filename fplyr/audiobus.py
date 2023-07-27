#!/usr/bin/env python3
#
##############################################################################################
#
# fplyr - Adult entertainment background audio sample and music player
#
# For updates see git-repo at
# https://github.com/pronopython/fplyr
#
##############################################################################################
#
VERSION = "0.1.0-alpha"
#
##############################################################################################
#
# Copyright (C) 2023 PronoPython
#
# Contact me at pronopython@proton.me
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################################
#


import threading
from time import sleep,time
from pydub.utils import make_chunks

class AudioBus:

	def __init__(self, pyaudio_instance, name=""):
		self.lock = threading.Lock()
		self.audiosample = None
		self.stream = None
		self.pyaudio_instance = pyaudio_instance

		self.audioBusLoopRunning = False
		self.is_playing = False
		self.running = True
		self.time_last_play = 0
		self.time_next_play = 0
		self.name = name
		self.pan = 0.0 # random pan only for playback
		self.pitch_semitone = 0 # layer based pitch
		self.run()


	def __str__(self):
		return self.name

	def run(self):
		self.thread = threading.Thread(target=self.audioBusLoop, args=())
		self.thread.daemon = True # so these threads get killed when program exits
		self.thread.start()

	def get_stream(self, seg):
		self.lock.acquire()
		stream = self.pyaudio_instance.open(format=self.pyaudio_instance.get_format_from_width(seg.sample_width),
						   channels=seg.channels,
						   rate=seg.frame_rate,
						   output=True,frames_per_buffer=32000)
		self.lock.release()
		return stream

	def audioBusLoop(self):

		self.audioBusLoopRunning = True
		print("AudioBus started")

		self.state = 0

		while(self.running):

			if self.state == 0:
				if self.audiosample != None:
					if not self.audiosample.is_loaded:
						self.audiosample.load()
					self.stream = self.get_stream(self.audiosample.seg)
					chunk_count = 0
					seg = self.audiosample.seg
					if self.pitch_semitone != 0:
						seg = self.audiosample.pitch_shift(seg,self.pitch_semitone)
					if self.pan != 0:
						seg = seg.pan(self.pan)
					chunks = make_chunks(seg, 100) # 100 = chunk length in ms
					self.state = 10
				else:
					sleep(0.06)


			if self.state == 10:

				if chunk_count < len(chunks):
					data = (chunks[chunk_count])._data
					chunk_count += 1
					self.stream.write(data)
				if chunk_count >= len(chunks):
					if self.audiosample.repeat:
						chunk_count = 0
					else:
						sleep(2)
						self.stream.stop_stream()
						self.stream.close()
						self.state = 0
						self.time_last_play = time()
						self.audiosample = None
						self.is_playing = False
		self.is_running = False

		print("AudioBus",self.name,"loop exited")
		self.audioBusLoopRunning = False



	def play(self, audiosample,pan=0, pitch_semitone = 0):
		self.audiosample = audiosample
		self.pan = pan
		self.pitch_semitone = pitch_semitone
		self.is_playing = True



	def terminate(self):
		self.running = False

		while (self.audioBusLoopRunning):
			sleep(0.06)


