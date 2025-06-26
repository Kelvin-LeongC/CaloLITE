from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea, QCheckBox, QComboBox, QPushButton, QLabel
from PySide6.QtCore import Qt
from functools import partial
import contextlib

from database import config as cfg
from presenters.MainStage import MainStage

class CaloLITE_Window(QMainWindow):
    def __init__(self, mainStage:MainStage, eventNumbers: list[int]):
        super().__init__()
        self.setWindowTitle("Calo-LITE")
        self.resize(1200, 800)
        self.subDetector_checkboxes = {}            # dict[str: QCheckBox]
        self.group_checkboxes = {}                  # dict[str: QCheckBox]
        self.eventNumbers = eventNumbers            # list[int]

        # Store mainStage presenter to UI (should already have scene, etc initialized in it)
        self.mainStageWidget = mainStage
        
        # Setup main layout
        mainContainerBase = QWidget(self)            
        self.setCentralWidget(mainContainerBase)
        mainContainerLayout = QGridLayout(mainContainerBase) 
        
        # Add the side panel onto the 3D interactive window
        event_selection_panel = self._create_event_selection_panel()
        detector_selection_panel = self._create_detector_selection_panel()
        axis_panel = self._create_auxfunc_panel()
        
        # Create a scroll area for the sub-detector side panel
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setWidget(detector_selection_panel)
        
        # Assemble all panel to main container
        mainContainerLayout.addWidget(self.mainStageWidget, 0, 0, 3, 1)     # row, col, rowSpan, colSpan
        mainContainerLayout.addWidget(event_selection_panel, 0, 1)          # upper left
        mainContainerLayout.addWidget(scrollArea, 1, 1)                     # middle right
        mainContainerLayout.addWidget(axis_panel, 2, 1)                     # lower right
        mainContainerLayout.setColumnStretch(0, 4)          # Main stage column gets 3 parts of stretch
        mainContainerLayout.setColumnStretch(1, 1)          # Side panel column gets 1 part of stretch
        
        
        
    # =========================================================
    # UI-level wrapper functions to call onto the presenter-level toggle function 
    def on_axis_toggled(self, checked): 
        self.mainStageWidget.set_axis_visibility(checked)
        
    def on_reset_camera_clicked(self):
        self.mainStageWidget.resetCamera()
     
    def on_subdet_toggled(self, subDetectorName:str, checked:bool):
        self.mainStageWidget.set_sub_detector_visibility(subDetectorName, checked)
        self._update_group_header_state(subDetectorName)

    def on_group_toggled(self, group_display_name: str, checked: bool):
        # Find the member names for this group
        member_names_for_group = self._find_all_member_names_in_group(group_display_name)
        
        # Programmatically setting checked state will trigger its own toggled signal
        for individual_name in member_names_for_group:
            child_checkbox = self.subDetector_checkboxes[individual_name]
        
            # Block child checkbox signal to prevent on_subdet_toggled
            with self._signal_blocker(child_checkbox):
                child_checkbox.setChecked(checked)
                
            # Manually trigger the visibility update normally done by on_subdet_toggled
            self.mainStageWidget.set_sub_detector_visibility(individual_name, checked)

        # After all children are set to the new 'checked' state, then run _update_group_header_state
        # to update the header state also to 'checked' state
        self._update_group_header_state(member_names_for_group[0])
        
    def number_changed(self, text):
        if text == "<Default>":
            self.mainStageWidget.resetEventDisplay()
        else:
            self.mainStageWidget.changeEventDisplay(int(text))
        self.drop_down_list.hidePopup() 

                
    # =============================================================            
    # Helper functions
    # =============================================================
    
    def _create_event_selection_panel(self) -> QWidget:
        """
        Creates a panel with a drop-down list of event numbers, where the selected event will be displayed on screen
        """
        sidePanelBase = QWidget(self)
        sidePanelLayout = QVBoxLayout(sidePanelBase)
        self.drop_down_list = QComboBox()
        self.drop_down_list.setStyleSheet("combobox-popup: 0;")
        self.drop_down_list.setMaxVisibleItems(20) # Set maximum visible items in dropdown
        display_items = ["<Default>"] + [str(event) for event in self.eventNumbers]
        self.drop_down_list.addItems(display_items)
        self.drop_down_list.currentTextChanged.connect(self.number_changed)
        self.drop_down_list.setCurrentIndex(0)
        
        sidePanelLayout.addWidget(self.drop_down_list)
        
        return sidePanelBase
    
    def _create_detector_selection_panel(self) -> QWidget:
        """
        Creates panel containing group header and sub-detector checkboxes
        """
        sidePanelBase = QWidget(self)
        sidePanelLayout = QVBoxLayout(sidePanelBase)
        
        # Checkboxes UI that connects to show-on or show-off functions in the presenters
        # Create checkboxes for groups and their individual sub-detectors
        for group_display_name, member_names in cfg.detector_group_definitions.items():
            # Create and add the group header checkbox
            group_header_checkbox = self.CustomGroupHeaderCheckBox(group_display_name)
            group_header_checkbox.setChecked(True)  # initial state
             
            group_header_checkbox.toggled.connect(
                partial(self.on_group_toggled, group_display_name)
            )
            sidePanelLayout.addWidget(group_header_checkbox)
            self.group_checkboxes[group_display_name] = group_header_checkbox

            # Create a container and layout for the children of this group
            children_container = QWidget()
            children_layout = QGridLayout(children_container)
            children_layout.setContentsMargins(20, 5, 5, 5)     # Indent children slightly

            for child_idx, individual_name in enumerate(member_names):
                checkbox = QCheckBox(individual_name)
                checkbox.setCheckable(True)
                checkbox.setChecked(True) 
                checkbox.toggled.connect(
                    partial(self.on_subdet_toggled, individual_name)
                )
                self.subDetector_checkboxes[individual_name] = checkbox
                # Arrange in 3 columns
                child_row, child_col = child_idx // 3, child_idx % 3 
                children_layout.addWidget(checkbox, child_row, child_col)
            sidePanelLayout.addWidget(children_container)
        
        sidePanelLayout.addStretch(1) # Push all group sections to the top
        return sidePanelBase
    
    def _create_auxfunc_panel(self) -> QWidget:
        """
        Creates panel for axis control
        """
        sidePanelBase = QWidget(self)
        sidePanelLayout = QHBoxLayout(sidePanelBase)
        
        self.toggle_axis = QCheckBox("Toggle XZ-axis")
        self.toggle_axis.setCheckable(True)
        self.toggle_axis.setChecked(True)
        self.toggle_axis.toggled.connect(self.on_axis_toggled)
        
        self.reset_cam = QPushButton("Reset Cam")
        self.reset_cam.clicked.connect(self.on_reset_camera_clicked)
         
        sidePanelLayout.addWidget(self.toggle_axis)
        sidePanelLayout.addWidget(self.reset_cam) 
        
        return sidePanelBase
    
    
    def _find_group_for_subdetector(self, subDetectorName: str) -> str:
        """
        Given a sub-detector name, return the group header name that this sub-detector 
        is supposed to be in
        """
        for group_name, member in cfg.detector_group_definitions.items():
            if subDetectorName in member:
                return group_name
    
    def _find_all_member_names_in_group(self, group_name: str) -> list[str]:
        """
        Given header group name, obtain the list of all sub-detector that belongs to this group
        """
        return cfg.detector_group_definitions.get(group_name)
    
    @contextlib.contextmanager
    def _signal_blocker(self, widget:QWidget):
        """
        A context manager to temporarily block signals for a given widget
        """
        original_signals_blocked = widget.signalsBlocked()
        widget.blockSignals(True)
        try:
            yield
        finally:
            widget.blockSignals(original_signals_blocked)
    
    def _update_group_header_state(self, subDetectorName: str):
        """
        Helper function for when the individual sub-detector checkbox is interacted by the user,
        -> will update the checkbox state of the group header accordingly if needed.
        """
        
        group_name = self._find_group_for_subdetector(subDetectorName)

        group_header_checkbox = self.group_checkboxes.get(group_name)   # QtCheckbox
        group_header_state = group_header_checkbox.checkState()
        
        # Find the member names for this group
        all_member_names_in_group = self._find_all_member_names_in_group(group_name)
        
        # Check how many children in the group are checked
        checked_children_count = 0
        for individual_name in all_member_names_in_group:
            child_checkbox = self.subDetector_checkboxes.get(individual_name)
            if child_checkbox.isChecked():
                checked_children_count += 1
                
        new_group_header_state = None
        if checked_children_count == 0:
            new_group_header_state = Qt.CheckState.Unchecked
        elif checked_children_count == len(all_member_names_in_group):
            new_group_header_state = Qt.CheckState.Checked
        else:
            new_group_header_state = Qt.CheckState.PartiallyChecked
            
        if group_header_state != new_group_header_state:
            # Block original group header state, and set new state for it
            with self._signal_blocker(group_header_checkbox):
                group_header_checkbox.setCheckState(new_group_header_state) 
    
        
    # Our own checkboxes sub-class with custom behaviour
    class CustomGroupHeaderCheckBox(QCheckBox):
        def __init__(self, text, parent=None):
            super().__init__(text, parent)
            self.setTristate()
            
        def nextCheckState(self):
            """
            Unchceked -> Checked
            Checked -> Unchecked
            PartiallyChecked -> Unchecked
            """
            current_state = self.checkState()
            if current_state == Qt.CheckState.PartiallyChecked:
                self.setCheckState(Qt.CheckState.Unchecked)
            else:
                # Default behavior for Unchecked -> Checked and Checked -> Unchecked
                super().nextCheckState()