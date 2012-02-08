===========================
ZenPacks.community.Varnish3
===========================

.. contents::
   :depth: 3


Description
===========
A ZenPack to provide support for Varnish version 3.x metrics. It introduces
a new command parser that is intended to be run over SSH. Metrics are parsed
from the output of the *varnishstat* command on the Varnish 3.x server

Components
==========
The ZenPack has the following: 

* A new command parser

  * ZenPacks.community.Varnish3.parsers.VarnishStat

* A new monitoring template

  * Varnish3 in /Server/Linux

Requirements & Dependencies
===========================
* Tested on Zenoss Version(s): 3.2.1
* External Dependencies: SSH Access to Varnish Server
* ZenPack Dependencies: None

Download
========
Download the appropriate package for your Zenoss version from the list
below.

* Zenoss 3.0+ `Latest Package for Python 2.6`_
* Zenoss 4.1+ `Latest Package for Python 2.7`_

Installation
============
Normal Installation (packaged egg)
----------------------------------
Copy the downloaded .egg to your Zenoss server and run the following commands as the zenoss
user::

    zenpack --install <package.egg>
    zenoss restart
    
Developer Installation (link mode)
----------------------------------
If you wish to further develop and possibly contribute back to the Varnish3
ZenPack you should clone the git repository, then install the ZenPack in
developer mode using the following commands::

    git clone git://github.com/dpetzel/ZenPacks.community.Varnish3.git
    zenpack --link --install ZenPacks.community.Varnish3
    zenoss restart
    
Configuration
=============
* Ensure SSH access from your Zenoss server to your Varnish server is setup
  and working properly.
* Ensure the SSH user you are using has access to run the *varnishstat*
  command
* The provided monitoring template is not automatically bound to any specific
  device class. You will need to either create a new device class and bind the
  template to this device class, or bind the template directly to your Varnish
  3.x servers in an existing device class.

Customizing or Changing The Monitoring Template
===============================================

Varnish 3.x outputs a large quantity of statistics. Different stats are going
to be valuable to different people. The provided template is simply a starting
point. I tried to pick stats I thought would have common interest. 

The command parser will support any of the stats that *varnishstat* will output
however you'll need to create a new datapoint that matches the name of the stat
you are interested in if its not already configured. Running *varnishstat -x* 
on your Varnish 3.x server will produce XML output containing all the stats. 
The <name>...</name> attribute of a stat would be the value to use when 
creating the new datapoint.

When adding datapoints, be sure to add them to the existing datasource. There is
no need to create a second datasource. Keeping a single datasource will keep 
the number of SSH calls needed to a minimum.

Handling Statistics With The Same Name
======================================
When dumping the *varnishstat* output via XML, some stats will actually have
the same value in their <name> node. Since each datapoint needs to have a unique
name the command parser will do some alerations to ensure uniqueness. The parser
will prepend the value of the <ident> node followed by a "-". Lets look at a 
real world example::

   <stat>
      <type>SMA</type>
      <ident>s0</ident>
      <name>g_bytes</name>
      <value>1973411487</value>
      <flag>i</flag>
      <description>Bytes outstanding</description>
   </stat>
   <stat>
      <type>SMA</type>
      <ident>Transient</ident>
      <name>g_bytes</name>
      <value>297633</value>
      <flag>i</flag>
      <description>Bytes outstanding</description>
   </stat>

In this example the command parser will produce the name "s0-g_bytes" for the
first stat and "Transient-g_bytes" for the second one. Its important to 
understand this if you intend to add any additional datapoints to the template.


Change History
==============
* 1.0

  * Initial Release

* 1.1

  * Some new datapoints and graphs on monitoring template
  * Added logic into the parser to handle conditions when multiple stats
    share the same name value
  * Updated install method to work around `Trac Ticket 7551`_ and enforce an
    rrdmin of 0 on all DERIVE datapoints in the provided template.
  * Added varnishd OSProcess
 
Screenshots
===========
|Varnish3_Cache_Hit_Rate|
|Varnish3_CacheHits_vs_Misses|
|Varnish3_Client_Connections|
|Varnish3_Client_Requests|
|Varnish3_Expired_Objects|
|Varnish3_Backend_Too_Late|

    
.. External References Below. Nothing Below This Line Should Be Rendered

.. _Latest Package for Python 2.6: http://github.com/downloads/dpetzel/ZenPacks.community.Varnish3/ZenPacks.community.Varnish3-1.1-py2.6.egg
.. _Latest Package for Python 2.7: http://github.com/downloads/dpetzel/ZenPacks.community.Varnish3/ZenPacks.community.Varnish3-1.1-py2.7.egg
.. _Trac Ticket 7551: http://dev.zenoss.com/trac/ticket/7551

.. |Varnish3_Cache_Hit_Rate| image:: http://github.com/dpetzel/ZenPacks.community.Varnish3/raw/master/docs/screen_shots/Varnish3_Cache_Hit_Rate.PNG
.. |Varnish3_CacheHits_vs_Misses| image:: http://github.com/dpetzel/ZenPacks.community.Varnish3/raw/master/docs/screen_shots/Varnish3_CacheHits_vs_Misses.PNG
.. |Varnish3_Client_Connections| image:: http://github.com/dpetzel/ZenPacks.community.Varnish3/raw/master/docs/screen_shots/Varnish3_Client_Connections.PNG
.. |Varnish3_Client_Requests| image:: http://github.com/dpetzel/ZenPacks.community.Varnish3/raw/master/docs/screen_shots/Varnish3_Client_Requests.PNG
.. |Varnish3_Expired_Objects| image:: http://github.com/dpetzel/ZenPacks.community.Varnish3/raw/master/docs/screen_shots/Varnish3_Expired_Objects.PNG
.. |Varnish3_Backend_Too_Late| image:: http://github.com/dpetzel/ZenPacks.community.Varnish3/raw/master/docs/screen_shots/Varnish3_Backend_Too_Late.PNG
.. |Varnish3_GZIP_Operations| image:: http://github.com/dpetzel/ZenPacks.community.Varnish3/raw/master/docs/screen_shots/Varnish3_GZIP_Operations.PNG