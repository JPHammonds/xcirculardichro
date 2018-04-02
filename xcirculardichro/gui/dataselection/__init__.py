from enum import Enum

class SelectionTypeNames(Enum):
    DUMMY_SELECTION, SPEC_SELECTION, INTERMEDIATE_SELECTION = range(3)


from .AbstractSelectionDisplay import AbstractSelectionDisplay
from .pointselectioninfo import PointSetSelector, PointSetInfo, \
    PointSelectionInfo
from .rangeselectioninfo import RangeSetSelector, RangeSetInfo, \
    RangeSelectionInfo
from .dummyselectiondisplay import DummySelectionDisplay
from .intermediatedataselection import IntermediateDataSelection
from .specdisplay import SpecDisplay
from .selectionholder import SelectionHolder