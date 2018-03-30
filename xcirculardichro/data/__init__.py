from enum import Enum
# Make definitions to simplify the import process.  Eliminates the need
# to directly reference the module name when referring to a class
# makes this more Java like.
SELECTED_NODES = 'selectedNodes'
DATA_SELECTION = 'dataSelection' 

class DataSelectionTypes(Enum):
    RAW, AVERAGED, STEP_NORMALIZED, FULL_NORMALIZED = range(4)

from .datanode import DataNode
from .filedatanode import FileDataNode
from .scandatanode import ScanDataNode
from .intermediatescannode import IntermediateScanNode
from .intermediatedatanode import IntermediateDataNode
from .specscannode import SpecScanNode
from .specfiledatanode import SpecFileDataNode


