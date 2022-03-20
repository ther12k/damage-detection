import os

#========================== DIRECTORY =====================================
ROOT 					= os.path.normpath(os.path.dirname(__file__))

DIRECTORY_MODEL         = os.path.expanduser('~/.Halotec/Models')

DIRECTORY_LOGGER        = os.path.expanduser('~/.Halotec/Loggers')

#============================ MODELS ======================================
DETECTION_MODEL = {
	'damage_detection' : {
		'filename'  : 'damage_detection.pt',
		'url'       : 'https://www.dropbox.com/s/2vplxv80kxzti0q/damage_detection.pt?dl=1',
		'file_size' : 14753191
	}
}
#============================ CLASESS ======================================
CLASSES_DETECTION   = ['damage']
CLASSES_FILTERED    = ['damage']