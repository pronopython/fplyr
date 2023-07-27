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
from fplyr.audiobus import *
from fplyr.mixer import *
from fplyr.mediafileparser import *
from fplyr.mediaconverter import *
from fplyr.scenefileparser import *
from time import sleep,time
import os
import sys
import sounddevice # just the import of this module silences all the error output from pyaudio
from fplyr.colors import *



class App():


	def __init__(self):
		pass

	def run(self):
		pyaudio = PyAudio()
		mixer = Mixer(pyaudio)

		scenefile = "default.scn"

		if len(sys.argv) > 1:
			scenefile = sys.argv[1]

		if not os.path.isfile(scenefile):
			print("Following scene file not found:",scenefile)
			sys.exit()


		sfp = SceneFileParser()

		sfp.parseSceneFile(scenefile)


		roots = sfp.root_dirs
		mixer.layers = sfp.layers
		mixer.hotkeyNames = sfp.hotkeyNames


		mfp = MediafileParser()



		mconv = MediaConverter()



		for basedir in roots:
			for root, d_names, filenames in os.walk(basedir):
				for filename in filenames:
					f_name, f_ext = os.path.splitext(filename)
					if f_ext.lower() == ".fpl":
						media_found = False
						path_fpl = os.path.join(root,filename)
						for mediafilename in filenames:
							mf_name, mf_ext = os.path.splitext(mediafilename)
							if f_name == mf_name and mf_ext.lower() != ".fpl":
								media_found = True
								path_mf = os.path.join(root,mediafilename)

								path_pf = mconv.getProxyFilePath(path_mf)
								if path_pf != None:
									path_mf = path_pf
								else:
									print(color.YELLOW+"No proxy file created for "+path_mf+" (ffmpeg could not read it) - ignoring file"+color.NORMAL)
									continue

								audiosamples = mfp.createAudioSamplesFromMediaFile(path_fpl,path_mf)
								for audiosample in audiosamples:
									audiosample_added = mixer.addAudioSample(audiosample)
									if not audiosample_added:
										print(color.YELLOW+"Could not find layer+bucket for audiosample "+str(audiosample)+color.NORMAL)
									else:
										pass
								break
						if not media_found:
							print("No media file found for .fpl-file:",path_fpl)



		if mixer.numberOfAudiosamples == 0:
			print("No audiosamples found for layers specified in the scene file")
			sys.exit()
		print("Number of audiosamples in mixer:",mixer.numberOfAudiosamples)

		mixer.run()


		while mixer.running or mixer.mixerLoopRunning:
			sleep(3)


		print("Closing pyaudio")
		pyaudio.terminate()

		print("Bye!")




if __name__ == "__main__":
	app = App()
	app.run()


def main():
	app = App()
	app.run()
