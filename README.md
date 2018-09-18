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

Version 0.9 2018-04-16
    - Changes based on meeting with Beamline group
    - Change in how the selection for step correction range is done.  
    now instead of selecting a group of points on each side to use a
    range of values on each side are selected and points that lie inside 
    that range are used.  An option for automatic selection of a few 
    percent on either side is possible.  Sometimes still the user needs 
    to apply this range to get the proper corrections done but now this 
    is a bit more straightforward.
    - Have improved capture and file saving for different combinations of
    data.  There were issues selecting data from several intermediate data 
    sets or in saving the final combination of data.
    - For 4-ID-C added options to select (and/or) TEY/TFY/REF data.  With
    all of these chosen, it seems to get fairly complicated having individual
    plots for each of these showing up and tracking these in a legend, etc.
    If we can deal with these more one at a time then it will hpefully be 
    more straightforward for the user.  Still need to go through more on 
    how this data will be processed.
    
 Version 0.9.1 2018-08-17
 Fixes for things found in testing at the beamline:
   - Add code to handle inverting intermediate data sets
   - Add/fix code for close function to remove data sets
   - Add reload function so that the spec file can be updated to bring in more data as acquisition continues.
   - Clean up some of the Capture methods, especially the full normalized data
   - It has been noticed that as data is reloaded more memory is used on each close.  Spent time looking at this but have not yet found good reason for this to keep happening.  Have communicated this as well to Pete to keep this in mind as spec2nexus develops.
   
   Version 0.9.2 2018-09-17
   Change name for "Full Normalized" to "Two Field"
   Do more catches to check when we have the right scans selected to enable 
   capture menu items.
   Change some garbage collection to speed things up.
   
   Version 0.9.3 2018-09-18
   Change a missed text reference from Full Normalized To TwoField.   

   Version 0.9.4 2018-09-18
   Copy scritps xcirculardichro and xcirculardichro.bat to 
   plotxmcd and plotxmcd.bat.  