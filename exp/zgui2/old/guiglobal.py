import zgui.guilocal as local
import os
from .base import *
from .color import *
from .root import *
from .signal import *
from .slot import *
from .logger import *
from .mouse import *
from .keyboard import *
from .exception import *
from .layout import *
from .theme import *
from .filedialog import *
from .resmanager import *

def init(**args):
	
	local.logger = Logger('Gui')
	local.logger.info('zgui Initializing')
	local.size = pygame.display.get_surface().get_size()
	local.logger.info('Screen Size:', local.size)
	local.gui = MainWindow(size = local.size )
	local.mouse = Mouse()
	local.keyboard = Keyboard()
	local.resMgr = ResourceManager()
	local.folder = os.path.dirname(__file__)
	local.theme = Theme(**args)
	

	return local.gui

def safe_get(key,dic):
	try: 
		return dic[key]
	except:
		GuiError(str(key)+' is not in dict')

