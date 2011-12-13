=========================================
Developing a Command Parser Based ZenPack
=========================================
.. contents::
   :depth: 3

Inspiration
===========
I still consider myself a relative newb with Zenoss as well Python development.
A while back I set outp to write a custom `ZenPack for use with F5 LTMs`_. I never
would have been able to figure this out with the assistance of a great guide
written by Jane Curry. Her outstanding document can be found on the Zenoss 
community site: http://community.zenoss.org/docs/DOC-10268

I recently had a need for a ZenPack to interact with a couple of Varnish 3.x
servers. I scoured the net of course hoping someone had already done the work
for me, but no such luck. I didn't come across a few solutions for 2.x, but
from what I've been able to gather the interface to get these stats has change some
(no more fetching stats over the management port). So I set out to write my own.

I of course cracked Jane's document open, but I quickly realized that it was very
SNMP-centric. This was perfect for F5 pack as the device supports SNMP. However,
in this case SNMP is not an option. I've done enough research to know that what
I wanted to do is a custom Command Parser. The good news is that most of the concepts
from Jane's doc still applied, the bad news is that the mechanics were going to be
very different.

I search around a bit and I was able to find a few other ZenPacks that had taken
this approach, but I couldn't find any "how-to" style documentation. As I mentioned
before I don't consider myself a seasoned Python developer so for me reverse-engineering
someone's else's ZenPack would be a challenge for me. There is a small snippet of 
information in the `Zenoss Developer's Guide`_, but its far from a walk-through or 
step-by-step guide like Jane's document.

So I came to sad realization that the approach was going to have to be looking
at what others had already done. So I figured I should probably document the process
and make it available to others in case they find themselve in a similar situation

Conventions and Assumptions
===========================
Throughout this document I hope to link to existing documentation where it exists
so for things that are already covered elsewhere I will try and link to them, rather
than recreate similar documentation

Nearly everything done from the command line on a Zenoss server should be done
while logged in as the Zenoss user (as opposed to root). Whenever I say *as the zenoss user*
that means::

   ssh root@your_zenoss_server
   su - zenoss


Lets Get To It
==============
Create Your Empty ZenPack Shell
-------------------------------
Creating an empty ZenPack is covered in numerous locations so I won't dive into the 
details here. If you don't know how to create an empty shell, refer to section
3.2 of the `Zenoss Developer's Guide`_. Additionally Jane's 
`Creating Zenoss ZenPacks for Zenoss 3`_ covers it in section 2.1
of her document. In this case we will be creating **ZenPacks.community.Varnish3**.

Once the empty shell is created, you will certainly want to move it *out* of the
main ZenPack directory, and into a seperate folder which we will put under
source control. My Zenoss development instance is running on a Virtual Box VM
and I stored the files on a shared folder. This is totally personal preference
and feel free to put the files anywhere you want, just remember that every time I
reference '/media/zenpack_git_sources/ZenPacks.community.Varnish3/' you should
replace that with whatever folder you copied your pack out to. Here is what I ran
*as the zenoss user*::

   cp -R $ZENHOME/ZenPacks/ZenPacks.community.Varnish3 /media/zenpack_git_sources/ZenPacks.community.Varnish3
   zenpack --link --install=/media/zenpack_git_sources/ZenPacks.community.Varnish3
   zenoss restart
   
The full restart is arguably overkill, but I find knowing which situations require
restarting which deamons to be inconsistent so while it takes longer, I usually just
do a full restart rather than pick and choose which deamons to restart.

Initialize a new GIT Repo in your ZenPack Folder
------------------------------------------------
As Zenoss seems to be making the move to git as outline in `ZenPack Development Process`_
we are going to cooperate with that effort :) The `ZenPack Development Process`_ 
document does a good job already of providing both step-by-step as well as in-depth
explanation of the process. For me I've got the GIT client on my Zenoss VM, rather
than my host PC, but since we are using shared folders it should work equally well
from either. Here is what I ran to initialize the new repo::
   cd /media/zenpack_git_sources/ZenPacks.community.Varnish3
   git init
   
Next I grabbed the 'master' .gitignore file::
   cd /media/zenpack_git_sources/ZenPacks.community.Varnish3
   https://raw.github.com/zenoss/Community-ZenPacks-SubModules/master/.gitignore

Additionally I use Eclipse with the pydev module on my PC as my IDE. As a result 
there are a couple of extra files we will want to add to the .gitignore file. 
If you use some other IDE (or none at all) you can skip the following lines::
   cd /media/zenpack_git_sources/ZenPacks.community.Varnish3
   echo .pydevproject >> .gitignore
   echo .project >> .gitignore
   
Now add everything and do a commit. You should note that this commit does **not** 
push anything up to github, it simply commits the files into your local repo::
   git add -A
   git status
   git commit -m 'Commiting the initial empty shell'
   

   

   














.. External References Below. Nothing Below This Line Should Be Rendered


.. _ZenPack for use with F5 LTMs: http://github.com/dpetzel/ZenPacks.community.f5
.. _Zenoss Developer's Guide: http://community.zenoss.org/community/documentation/official_documentation/zenoss-dev-guide
.. _Creating Zenoss ZenPacks for Zenoss 3: http://community.zenoss.org/docs/DOC-10268
.. _ZenPack Development Process: http://community.zenoss.org/docs/DOC-8495 
