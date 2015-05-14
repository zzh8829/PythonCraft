import zgui.guilocal as local

def GuiError(s):
	local.logger.log('Error: %s'%s)
	local.gui.Quit()
	#raise Exception(s)

def GuiWarning(s):
	local.logger.log('Warning: %s'%s)
