import sys
import argparse
from PySide6.QtGui import QSurfaceFormat
from PySide6.QtWidgets import QApplication

from useCaseClasses.CalorimeterManager import CalorimeterManager
from useCaseClasses.EventManager import EventManager
from controllers.CalorimeterController import CalorimeterController
from controllers.EventController import EventController
from controllers.Renderable import Axis
from presenters.MainStage import MainStage, Scene
from UI.CaloLITE_UI import CaloLITE_Window
   

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This file lauches a GUI to display single event in the ATLAS Calorimeter")
    parser.add_argument('-ft', "--file_type", type=str, default="pi0", choices=["pi0", "pi+"], help="Choose event file type (pi0, pi+)")
    parser.add_argument('-et', "--event_tree", type=str, default="EventTree", help="TTree name in the event file")
    parser.add_argument('-cb', "--cell_coord_branch", type=str, default="mgex422_cluster_cell", help="TTree branch prefix of the cell coordinates in the event file")
    args = parser.parse_args()
    
    # Handle file name based choices of file type in argument (this can be freely changed)
    if args.file_type == "pi0": f = "pi0.mltree.root"
    elif args.file_type == "pi+": f = "piplus.mltree.root"
    
    # Create the QApplication instance
    app = QApplication(sys.argv)

    # Set the default surface format for OpenGL
    fmt = QSurfaceFormat()
    fmt.setDepthBufferSize(24)
    QSurfaceFormat.setDefaultFormat(fmt)

    # =====================================================
    # Initialize the useCase classes (for handling the database)
    calorimeter_manager = CalorimeterManager("database/cell_geo+.root")    
    event_manager = EventManager(f"database/{f}", args.event_tree, args.cell_coord_branch)
    
    # =====================================================
    # Initialize the controller classes 
    # (instances that contain instructions how the object in supposed to be drawn)
    axis_controller = Axis()
    calorimeter_controller = CalorimeterController(calorimeter_manager)
    sub_detector_controllers = calorimeter_controller.getAllSubDetector()
    event_controller = EventController(event_manager)
    
    # =====================================================
    # Initialize the presenter classes 
    # (instances that execute the instructions for drawing the objects, connected to UI buttons)
    ## Assemble the mainStage (Scene for overall control, objects like: axis, ...)
    scene = Scene()
    mainStage = MainStage(scene, axis_controller, sub_detector_controllers, event_controller)

    # =====================================================
    # Initialize the UI class (display window)
    window = CaloLITE_Window(mainStage, event_manager.getEventNumbers()) # Pass mainStage here
    window.show()
    sys.exit(app.exec())
