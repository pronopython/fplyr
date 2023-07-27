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
import random
from fplyr.audiobus import *
from pynput import keyboard

class AudioSampleBucket:


	def __init__(self, name=""):
		self.name = name
		self.play_probability = 100
		self.audiosamples = []

		self.play_probability_lower_border = 0
		self.play_probability_upper_border = 0



class Layer:


	def __init__(self, name="",appendSingleBucket=False,no_of_busses=1, waittime_min_sec=0, waittime_max_sec=0, random_pan = False, hotkey = None, pitch_semitone = 0):
		self.name = name
		self.no_of_busses = no_of_busses
		self.waittime_min_sec = waittime_min_sec
		self.waittime_max_sec = waittime_max_sec
		self.random_pan = random_pan
		self.concurrent_play_allowed = False
		self.audiosample_buckets = []
		self.sum_probabilty = 0
		self.hotkey = hotkey
		self.pitch_semitone = pitch_semitone

		self.busses = []

		if appendSingleBucket:
			self.audiosample_buckets.append(AudioSampleBucket())


class Mixer:

	HOTKEYS = "0123456789abcdefghijklmnopqrstuvwxyz"


	def __init__(self,pyaudio_instance):

		self.pyaudio_instance = pyaudio_instance

		self.running = False
		self.layers = []
		self.numberOfAudiosamples = 0
		self.hotkeyDisabled = []
		self.hotkeyNames = {}


	def addAudioSample(self,audiosample):
		for layer in self.layers:
			if layer.name == audiosample.layer:
				for bucket in layer.audiosample_buckets:
					if bucket.name == audiosample.bucket:
						bucket.audiosamples.append(audiosample)
						self.numberOfAudiosamples += 1
						return True
		return False







	def run(self):
		self.running = True
		self.thread = threading.Thread(target=self.mixerLoop, args=())
		self.thread.daemon = True # so these threads get killed when program exits
		self.thread.start()


	def mixerLoop(self):

		self.mixerLoopRunning = True
		print("Mixer started")

		self.busses = []

		print("Spawning audio busses")
		for layer in self.layers:
			print("No. of busses for Layer "+layer.name+":"+str(layer.no_of_busses))
			for i in range(0,layer.no_of_busses):
				bus = AudioBus(self.pyaudio_instance, name=layer.name+"_"+str(i))
				self.busses.append(bus)
				layer.busses.append(bus)


		# set up probabilities
		for layer in self.layers:
			sum_probabilty = 0
			for bucket in layer.audiosample_buckets:
				bucket.play_probability_lower_border = sum_probabilty
				sum_probabilty = sum_probabilty + bucket.play_probability
				bucket.play_probability_upper_border = sum_probabilty
			layer.sum_probabilty = sum_probabilty

		# TODO pynput keyboard reads all keypresses of all windows
		# That's not acceptable so this is currently commented out
		# listener = keyboard.Listener(on_release=self.checkKeyPress)
		# listener.start()
		# print("======> Press Esc to quit! <======")


		while(self.running):

			sleep(0.1) #VERY important, otherwise file handling and other things are slowed down!!!

			for layer in self.layers:
				for bus in layer.busses:
					#print("Checking bus",bus)
					if not bus.is_playing:
						# waittime check
						if layer.waittime_min_sec > 0 or layer.waittime_max_sec > 0:
							if bus.time_next_play <= bus.time_last_play:
								waittime = random.randint(layer.waittime_min_sec,layer.waittime_max_sec)
								print("Bus ",bus," will sleep for ",waittime," seconds")
								bus.time_next_play = time() + waittime
							if bus.time_next_play > time():
								continue

						select_tries = 0
						while select_tries < 5:
							select_tries = select_tries + 1
							# pick bucket by probability
							prob = random.randint(0, layer.sum_probabilty)
							selected_audiosample = None
							for bucket in layer.audiosample_buckets:
								if (bucket.play_probability_lower_border < prob
								   and bucket.play_probability_upper_border > prob):
									if len(bucket.audiosamples) > 0:
										selected_audiosample = random.choice(bucket.audiosamples)
									else:
										print("Bucket",bucket.name,"of layer",layer.name,"is empty!")
									break
							if selected_audiosample == None:
								print("Mixer: No audiosample could be selected for layer",layer.name)
								continue


							# check concurrent play
							collision = False
							if not layer.concurrent_play_allowed:
								for other_bus in layer.busses:
									if other_bus.audiosample == selected_audiosample:
										collision = True
							if collision:
								continue

							if layer.hotkey in self.hotkeyDisabled:
								continue


							# random pan
							pan = 0.0
							if layer.random_pan:
								pan = random.uniform(-1.0,1.0)

							# play
							print(bus.name,"playing",selected_audiosample)
							bus.play(selected_audiosample,pan=pan,pitch_semitone=layer.pitch_semitone)
							break


		print("Mixer loop exited")
		print("Stopping audiobusses")
		for bus in self.busses:
			bus.terminate()



		self.mixerLoopRunning = False


	def getHotkeyName(self,hotkey):
		if hotkey in self.hotkeyNames:
			return self.hotkeyNames[hotkey]
		else:
			return hotkey

	def checkKeyPress(self,key):
		try:
			if key == keyboard.Key.esc:# or key.char == 'q': 
				self.running = False
				print("Quit pressed!")
				return False # stop pynput listener
			if key.char in self.HOTKEYS:
				#print("hotkey pressed")
				if key.char in self.hotkeyDisabled:
					print("Hotkey Bank",self.getHotkeyName(str(key.char)),"now playing")
					self.hotkeyDisabled.remove(key.char)
				else:
					print("Hotkey Bank",self.getHotkeyName(str(key.char)),"stopped")
					self.hotkeyDisabled.append(key.char)
				#print(self.hotkeyDisabled)
		except AttributeError:
			# special keys have no char attribute
			# this prevents that e.g. arrow-up crashes this keyboard loop
			pass

	def terminate(self):
		self.running = False

		while (self.mixerLoopRunning):
			sleep(0.06)


