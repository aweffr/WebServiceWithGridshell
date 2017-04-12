# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 6.13-4 replay file
# Internal Version: 2014_01_04-09.03.49 126873
# Run by ZouLe on Wed Apr 12 15:21:02 2017
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(1.76302, 1.76389), width=259.517, 
    height=174.978)
session.viewports['Viewport: 1'].makeCurrent()
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
execfile('./AbaqusAPI/BuildModel.py', __main__.__dict__)
#: The model "Model A" has been created.
#: The section "ConnSect-Link" has been assigned to 8 wires or attachment lines.
#: Now Job created!
#: Now Job submitted!
#: The model database has been saved to "D:\My Docs\00.MasterDegree\software\AbaqusFiles\mdbFile-0.cae".
print 'RT script done'
#: RT script done
