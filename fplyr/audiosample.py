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

from pydub import AudioSegment
from pydub.utils import make_chunks
from pyaudio import PyAudio
import librosa
import numpy as np
import os

class AudioSample():
	def printInfoOfSegment(self, audio):
		print({
			'duration' : audio.duration_seconds,
			'sample_rate' : audio.frame_rate,
			'channels' : audio.channels,
			'sample_width' : audio.sample_width,
			'frame_count' : audio.frame_count(),
			'frame_rate' : audio.frame_rate,
			'frame_width' : audio.frame_width,
		})


	def __init__(self, filename, repeat = False,start_sec=0,end_sec=-1,speed=1.0, pan = 0.0, volume_decrease = 0, layer = "", bucket = "", pitch_semitone = 0):
		self.is_loaded = False

		self.filename = filename
		self.repeat = repeat
		self.start_sec = start_sec
		self.end_sec = end_sec
		self.speed = speed
		self.pan = pan
		self.volume_decrease = volume_decrease
		self.layer = layer
		self.bucket = bucket
		self.pitch_semitone = pitch_semitone
		self.seg = None


	def __str__(self):
		if self.bucket == "":
			return self.filename + " from " + str(self.start_sec) + " to " + str(self.end_sec) + " @ " + self.layer
		else:
			return self.filename + " from " + str(self.start_sec) + " to " + str(self.end_sec) + " @ " + self.layer + "/" + self.bucket



	def pitch_shift(self, seg, pitch_semitone):
		print("Pitch shifting....")
		samples = seg.get_array_of_samples()
		arr = np.array(samples).astype(np.float32)
		y = librosa.effects.pitch_shift(arr, sr=seg.frame_rate, n_steps=pitch_semitone)
		z = y.astype(np.int16)
		newseg = AudioSegment(z.tobytes(),frame_rate=seg.frame_rate,sample_width=seg.sample_width,channels=seg.channels)
		print("Pitch shifting done")
		return newseg



	def load(self):
		self.seg = AudioSegment.from_file(self.filename)

		# trim
		if self.start_sec > 0 or self.end_sec != -1:
			if self.end_sec != -1:
				self.seg = self.seg[self.start_sec*1000:self.end_sec*1000]
			else:
				self.seg = self.seg[self.start_sec*1000:]

		# pan
		#Takes one positional argument, pan amount, which should be between -1.0 (100% left) and +1.0 (100% right)
		if self.pan != 0.0:
			self.seg = self.seg.pan(self.pan)

		# volume
		if self.volume_decrease < 0:
			self.seg = self.seg + self.volume_decrease # reduce volume by x db

		#self.printInfoOfSegment(self.seg)

		# stretch
		if self.speed != 1.0:
			print("Stretching....")
			samples = self.seg.get_array_of_samples()
			arr = np.array(samples).astype(np.float32)
			y = librosa.effects.time_stretch(arr, rate=self.speed)
			z = y.astype(np.int16)
			newseg = AudioSegment(z.tobytes(),frame_rate=self.seg.frame_rate,sample_width=self.seg.sample_width,channels=self.seg.channels)
			self.seg = newseg
			print("Stretching done")


		# pitch shift
		if self.pitch_semitone != 0:
			self.seg = self.pitch_shift(self.seg,pitch_semitone)
			#print("Pitch shifting....")
			#samples = self.seg.get_array_of_samples()
			#arr = np.array(samples).astype(np.float32)
			#y = librosa.effects.pitch_shift(arr, sr=self.seg.frame_rate, n_steps=self.pitch_semitone)
			#z = y.astype(np.int16)
			#newseg = AudioSegment(z.tobytes(),frame_rate=self.seg.frame_rate,sample_width=self.seg.sample_width,channels=self.seg.channels)
			#self.seg = newseg
			#print("Pitch shifting done")



		self.is_loaded = True

