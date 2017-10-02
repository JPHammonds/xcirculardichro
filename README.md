xcirculardichro is a python program for


Version 0.0.1 
	Started 5/10/2017
	
Version 0.1   2017-10-02
Refine features for the first major release.  
 - Allow selection of scans from the spec file
 - Choose what type of scan to deal with.  Most work here has been done with 
   non-lockin type from Haskel's Examples and then lockin type.  Still need to 
   get better example files from Keavney.
 - Allow selection of a set of scans from the spec file to process and then store 
   as an intermediate set.
 - Enable point selection for pre/post edge reference points.  Here these points
   are averaged to give a value before peak and after peak.  Need to take a 
   ratio of these averages and then divide both XAS and XMCD by these values to 
   normalize the data.
   
Version 0.2   2017-10-02
  - Change comments saying pyqt4 to pyqt5 	
  
Version 0.3   2017-10-02
  - Change requirement for pyqt from pyqt5 to pyqt

Version 0.4   2017-10-02
  - Remove requirement for pyqt from setup.py.  It is not available through pip.
    If using anaconda, user will need to do conda install.  Still cannot leave 
    this as a requirement.  Not finding it.
    
Version 0.5  2017-10-02
   - Increase required version of specguiutils
   
Version 0.6  2017-10-02
   - Something wrong with 0.5
   
Version 0.7 2017-10-02
	- Set ScanBrowser in IntermediateDataSelexction so that the table is not editable.
    - Add in singal handling so that point selection for pre/post peak levels can be adjusted to provide for normalization.
    
Version 0.7 2017-10-02
    - change vesion number for specguiutils