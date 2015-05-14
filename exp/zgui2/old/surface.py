import zgui.guilocal as local
import pygame
import copy
from .guiglobal import *
from .color import *
from .utils import *

class ExSurface(object):
	"""A Extended Surface Class for safety"""

	def __init__(self,*args):
		if len(args)==1:
			if isinstance(args[0],pygame.Surface):
				self.surface = args[0]
			elif isinstance(args[0],ExSurface):
				self.surface = args[0].surface
			elif isinstance(args[0],tuple):
				self.surface = pygame.Surface(args[0])
			else:
				self.surface = pygame.Surface(*args)
		elif len(args)==2:
			if isinstance(args[0],tuple):
				if isinstance(args[1],tuple):
					self.surface = pygame.Surface(args[0])
					self.surface.fill(args[1])
				elif isinstance(args[1],pygame.Color):
					self.surface = pygame.Surface(args[0])
					self.surface.fill(args[1])
				else:
					self.surface = pygame.Surface(*args)
			else:
				self.surface = pygame.Surface(*args)
		else:
			self.surface = pygame.Surface(*args)

	def __getattr__(self,attr):
		"""access surface attr as attr of self"""
		try: return getattr(self.surface,attr)
		except:	raise AttributeError

	def blit(self,surf,pos):
		"""blit to"""
		if isinstance(surf,ExSurface):
			return self.surface.blit(surf.surface,pos)
		elif isinstance(surf,pygame.Surface):
			return self.surface.blit(surf,pos)

	def subsurface(self,rect):
		"""return subsurface with size check"""
		rect = list(rect)
		rect[2],rect[3] = MaxSize((rect[2],rect[3]),pos_minus(self.get_size(),(rect[0],rect[1])))
		rect[0],rect[1] = SafeSize((rect[0],rect[1]))
		return ExSurface(self.surface.subsurface(rect))

	def copy(self):
		"""return copy"""
		return ExSurface(self.surface.copy())


class OldExSurface(pygame.Surface):
	"""old Extend surface, becuase of pygame.Surface is from C, so failed"""

	def __init__(self,*args):
		if len(args) > 1 and isinstance(args[1],tuple):
			self.safe_init(args[0])
			self.fill(args[1])
		elif isinstance(args[0],pygame.Surface):
			if len(args) > 1:
				if args[1] == 'subsurface':
					self = args[0].subsurface(args[0].get_rect())
			else:
				super().__init__(args[0].get_size(),args[0].get_flags())
				self.blit(args[0],(0,0))
		else:
			self.safe_init(*args)

	def safe_init(self,*args):
		args = list(args)
		args[0] = SafeSize(args[0])
		super().__init__(*args)

		
	def __copy__(self):
		"""copy"""
		return self.copy()

	def __deepcopy__(self,memo):
		"""deepcopy"""
		return self.copy()

	def subsurface(self,rect):
		"""return subsurface"""
		size = rect[2],rect[3]
		size = ValidateSize(size,self.get_size())
		super().subsurface(size)