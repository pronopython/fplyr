from setuptools import setup

setup(name='Fplyr',
	version='0.1.0-alpha',
	description='fplyr is a background audio sample and music player for adult entertainment purpose',
	url='https://github.com/pronopython/fplyr',
	author='pronopython',
	author_email='pronopython@proton.me',
	license='GNU GENERAL PUBLIC LICENSE V3',
	packages=['fplyr'],
	package_data={'fplyr':['*']},
	include_package_data=True,
	zip_safe=False,
	install_requires=['pydub','pyaudio','librosa','numpy','ffmpy','sounddevice','pynput','pyyaml'],
	entry_points={
        'console_scripts': [
            'fplyr=fplyr.fplyr:main'
		]
    	}
    )


