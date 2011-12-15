
import Globals
import os.path
from Products.ZenModel.ZenPack import ZenPackBase
import logging
from transaction import commit

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())
    
#Create a logger in the "zen" namespace. Creating it as a child of zen
#Ensures we inherit existing logging configuration. We then append the zenpack
#name to create a unique logger
logger = logging.getLogger('.'.join(['zen', __name__]))

class ZenPack(ZenPackBase):
    """
    Varnish3 Loader
    """
    
    TEMPLATE_NAME = "Varnish3"
    
    def install(self, app):
        """
        Extend base install() in order to run custom code during installation
        
        This is currently here simply as an indicator as to how/where
            this extension would occur. In this particular pack we have
            no custom installation code.
        """
        logger.debug("Executing custom installation code")
        super(ZenPack, self).install(app)
        
        """
        Now lets work around my favorite bug. Apply an rrdmin of 0
            to all of our DERIVE datapoints
        @see: http://dev.zenoss.com/trac/ticket/7551
        @see: http://community.zenoss.org/message/59914
        """
        for template in dmd.Devices.getAllRRDTemplates():
            if template.id == TEMPLATE_NAME:
                for dp in template.getRRDDataPoints():
                    if dp.rrdtype == "DERIVE":
                        dp.rrdmin = 0 
                
        
        
    def remove(self, dmd, leaveObjects=False):
        """
        Extend base remove() in order to run custom code during pack removal
        
        This is currently here simply as an indicator as to how/where
            this extension would occur. In this particular pack we have
            no custom removal code.
        """
        logger.debug("Executing custom removal code")
        super(ZenPack, self).remove(dmd, leaveObjects=leaveObjects)
