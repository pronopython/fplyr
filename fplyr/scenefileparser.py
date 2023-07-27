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

from fplyr.audiosample import *
from fplyr.mixer import *
import yaml


class SceneFileParser():


	def __init__(self):
		self.layers = []
		self.hotkeyNames = {}
		self.root_dirs = []

	def parseSceneFile(self, filename):

		with open(filename, 'r') as file:
			scene = yaml.safe_load(file)
			#print(scene)

			self.root_dirs = scene["root_dirs"]

			if "hotkeys" in scene:
				d = scene["hotkeys"]
				d = {str(k):str(v) for k,v in d.items()} # convert everything to string
				self.hotkeyNames = d


			for layer in scene["layers"]:
				layername = layer["layer"]
				if "busses" in layer:
					no_of_busses = layer["busses"]
				else:
					no_of_busses = 1
				if "waittime_min_sec" in layer:
					waittime_min_sec = layer["waittime_min_sec"]
				else:
					waittime_min_sec = 0
				if "waittime_max_sec" in layer:
					waittime_max_sec = layer["waittime_max_sec"]
				else:
					waittime_max_sec = 0
				if "pitch" in layer:
					pitch_semitone = layer["pitch"]
				else:
					pitch_semitone = 0
				if "random_pan" in layer:
					random_pan = layer["random_pan"]
				else:
					random_pan = False
				if "hotkey" in layer:
					hotkey = str(layer["hotkey"])
				else:
					hotkey = None


				# TODO handle buckets

				self.layers.append(Layer(layername,appendSingleBucket=True,no_of_busses=no_of_busses, waittime_min_sec=waittime_min_sec, waittime_max_sec=waittime_max_sec,random_pan=random_pan,hotkey=hotkey,pitch_semitone = pitch_semitone))


