"""
VarnishStat.py
@summary: A Custom Zenoss Command Parser for VarnishStat output
@author: David Petzel
"""

import re
from xml.etree.ElementTree import ElementTree, fromstring
import logging

from Products.ZenRRD.CommandParser import CommandParser
from Products.ZenUtils.Utils import getExitMessage

logger = logging.getLogger(".".join(["zen", __name__]))

class VarnishStat(CommandParser):
    
    def processResults(self, cmd, result):
        """
        """
        if self._errors_found(cmd, result):
            err_msg = "Errors were detected prevent further processing" + \
                "Review log files for additional details"
                
        stat_list = []
        if "varnishstat -x" in cmd.command:
            stat_list = self._xml_to_stat_list(cmd.result.output)
        elif "varnishstat -1" in cmd.command:
            stat_list = self._txt_to_stat_list(cmd.result.output)
        else:
            err_msg = "Unknown command options used. I don't know how to " + \
                "parse that."
            logger.error(err_msg)
            return
        if stat_list == []:
            err_msg = "Something wen't wrong, I was unable to get a list " + \
                "of stats. Please review log files for more details"
            logger.error(err_msg)
        
           
        #Fetch a dictionary of stats from stat list we built
        stat_dict = self._stat_dict(stat_list)
        
        #Now loop through the data points and see check if we have a stat
        for dp in cmd.points:
            if dp.id in stat_dict:
                if 'value' in  stat_dict[dp.id]:
                    result.values.append( (dp, stat_dict[dp.id]['value']) )
                else:
                    logger.error("No Value for stat %s", stat_dict[dp.id] )
            else:
                err_msg = "You've requested a data point %s for which " + \
                    "there is no matching stat name. Please double check " + \
                    "Your data points names against varnishstat output"
                logger.error(err_msg, dp.id)
  
    def _xml_to_stat_list(self, xml_string):
        """
        Convert XML output string to a list of dictionarys
        @type xml_string: String
        @param xml_string: The raw XML string output produced
            from the varnishstat -x command
        @rtype: List
        @return: A list of 'stats' where is each Stat is a dictionary
            representation of the XML output
        """
        stat_results = []
        tree = fromstring(xml_string)
        
        stat_list = tree.findall("stat")
        for stat in stat_list:
            stat_data = {}
            for stat_attribute in list(stat):
                stat_data[stat_attribute.tag] = stat_attribute.text
            stat_results.append(stat_data)
        logger.debug(stat_results)
        return  stat_results
    
    def _txt_to_stat_list(self, txt_string):
        """
        Unimplemented Stub. At this time I don't really see the need for this
        but stubbing it out to make adding it in the future a little more
        obvious should it come to that
        """
        err_msg = "Only XML based parsing is supported right now. " + \
            "Please update your command to use -x instead of -1"
        logger.error(err_msg)
        return []
    
    def _stat_dict(self, stat_list):
        """
        We want a dictionary of stats where the name of the stat matches
        the name of the datapoints. This will allow us flexibily when new
        stats are added, we don't need to alter the code.
        
        Most Stats have names, however VBE's throw a monkey wrench into this.
        So for the sake of this dictionary we are going to forget about them
        We may use them later in some sort of modeler if I get ambitious
        
        LCK items also seem to give us some grief
        
        """
        return_dict = {}
        
        for stat in stat_list:
            b_process = True
            if 'type' in stat:
                if stat['type'] == "VBE" or stat['type'] == "LCK":
                    b_process = False
                    continue
                else:
                    b_process = True
            if b_process == True:
                if 'name' in stat:
                    name = ""
                    if 'ident' in stat:
                        """
                        Some Stats share a common <name> node
                        for those we need to ensure unique names
                        since the name is the key in our stat dictionary.
                        It seems that such stats have an additional <ident>
                        node. Lets combine the ident with the name to ensure
                        we generate a unique key
                        """
                        name = "-".join([stat['ident'], stat['name']])
                    else:
                        name = stat['name']
                    #No point in duplicating the name
                    #drop it from the new child dict
                    del(stat['name'])
                    if name not in return_dict:
                        return_dict[name] = stat
                    else:
                        logger.error("Duplicate stat name %s detected", name)
                else:
                    logger.error("Stat without a name detected: %s", stat)
        return return_dict
    
    def _errors_found(self, cmd, result):
        """
        Run through a series of error checks
        @param cmd: The Command Object which was passed into processResults
        @rtype: Boolean
        @return: Boolean indicating if errors were found
        """
        errors_found = False
        #Check for non 0 exit code in the command
        exit_code = cmd.result.exitCode
        if exit_code != 0:
            errors_found = True
            msg = 'VarnishStat cmd parser error: %s - Code: %s - Msg: %s' % (
                cmd.command, exit_code, getExitMessage(exit_code))
            result.events.append(dict(device=cmd.deviceConfig.device,
                                      summary=msg,
                                      severity=cmd.severity,
                                      eventKey=cmd.eventKey,
                                      eventClass=cmd.eventClass,
                                      rawOutput=cmd.result.output,
                                      component=cmd.component))  
        return errors_found  
    

        
        
