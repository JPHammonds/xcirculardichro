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
	- Set ScanBrowser in IntermediateDataSelexction so that the table is not 
	  editable.
    - Add in signal handling so that point selection for pre/post peak levels 
      can be adjusted to provide for normalization.
    
Version 0.8 2017-10-02
    - change version number for specguiutils
    
Version 0.8pre1
   - Add extraction of data into intermediate sets which are more manageable.  
   Can Extract Groups of individual scans, average of a group of scans, or 
   Edge-Normalized spectra.  
   - Can  plot Normalized data
   - Can save intermediate results to a file.  File will be text delimited columns with a header for extra information and then a row of named columns.
   - Added the ability to add selected parameters/positioners into the spec data selector's scanBrowser so that the user can see extra information that may help them distinguish between runs that go together and those that should be processed separately.

Version 0.8.rc5 2018-01-10
    - Initial code added for reading files from David Keavney.  Problems exist with data display after reading which crash the application. This data has multiple XAS and XMCD per file.  This causes a problem with the code bit that allows selection of points for step normalization.
    - Add code for selecting parameters from the positioner list.   This is used to add columns to the ScanBrowser for extra data selection information.
    - Add code for the user parameters at sector 4 to display in the scan browser table.
