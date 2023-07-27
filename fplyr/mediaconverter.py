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

from ffmpy import FFmpeg
from ffmpy import FFRuntimeError
import os



class MediaConverter():

	def __init__(self):

		pass


	def getProxyFilePath(self, original_file):
		of_name, of_ext = os.path.splitext(original_file)
		path = os.path.dirname(original_file)
		proxy_file = os.path.join(path, of_name+".fpx")

		if not os.path.isfile(proxy_file):
			try:
				ff = FFmpeg(
					inputs={original_file: None},
					#outputs={proxy_file: '-f wav -acodec pcm_s16le -ar 44100 -ac 2'}
                    #outputs={proxy_file: '-f mp3 -vn -acodec mp3 -ar 44100 -ac 2 -b:a 192k'}
                    outputs={proxy_file: '-hide_banner -v quiet -stats -f mp3 -vn -acodec mp3 -ar 44100 -ac 2 -b:a 192k'}

					#-f wav -bitexact -acodec pcm_s16le -ar 22050 -ac 1 "ffmpeg.wav"
					)
				#print(ff.cmd)
				print("Creating proxy file for",original_file,"with ffmpeg:")
				ff.run()

				return proxy_file
			except(FFRuntimeError):
				return None
		else:
			return proxy_file




