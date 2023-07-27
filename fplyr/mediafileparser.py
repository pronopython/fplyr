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
from fplyr.colors import *
from itertools import chain
import csv


class MediafileParser():


	def __init__(self):
		pass

	def hms_to_s(self,s):
		t = 0
		for u in s.split(':'):
			t = 60 * t + int(u)
		return t

	def printParserError(self,filename,linenumber,csvrow):
		print(color.YELLOW+"Cannot interpret .fpl line "+str(linenumber)+" in "+filename+":")
		rowstr = ' '.join(csvrow)
		print(rowstr+color.NORMAL)



	def createAudioSamplesFromMediaFile(self, filenameFpl, filenameMedia):

		volume_decrease = 0
		speed = 1.0
		layer = ""
		bucket = ""
		pan = 0.0
		repeat = False
		pitch_semitone = 0

		audiosamples = []

		with open(filenameFpl, newline='') as csvfile:
			fplFileRows = csv.reader(csvfile, delimiter=' ', quotechar='|')
			for linenumber, row in enumerate(fplFileRows):
				if len(row) > 0 and row[0].startswith("#"):
					continue
				if len(row) == 1:
					if row[0] == "repeat":
						repeat = True
						#print("Repeat enabled")
						continue
					self.printParserError(filenameFpl, linenumber+1,row)
				if len(row) == 2:
					if row[0] == "vol":
						volume_decrease = int(row[1])
						#print("Volume decrease set to:",volume_decrease)
						continue
					elif row[0] == "layer":
						layer = row[1]
						#print("Layer set to:",layer)
						continue
					elif row[0] == "bucket":
						bucket = row[1]
						#print("Bucket set to:",bucket)
						continue
					elif row[0] == "speed":
						speed = float(row[1])
						#print("Speed set to:",speed)
						continue
					elif row[0] == "pan":
						pan = float(row[1])
						#print("Pan set to:",pan)
						continue
					elif row[0] == "pitch":
						pitch_semitone = int(row[1])
						continue
					#elif row[0].startswith("#"):
					#	pass
				if len(row) >= 2: # column 3 and beyond can be a comment
					try:
						start_sec = self.hms_to_s(row[0])
						if row[1] == "-1":
							end_sec = -1
						else:
							end_sec = self.hms_to_s(row[1])
						#print("Time sec: ",start_sec,end_sec)

						audiosample = AudioSample(filenameMedia, repeat = repeat,speed=speed,start_sec=start_sec,end_sec=end_sec,pan=pan,volume_decrease=volume_decrease, layer=layer, bucket=bucket, pitch_semitone = pitch_semitone)
						audiosamples.append(audiosample)
						continue

					except ValueError as ve:
						self.printParserError(filenameFpl, linenumber+1,row)
						continue
					self.printParserError(filenameFpl, linenumber+1,row)
		return audiosamples


