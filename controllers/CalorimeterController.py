from OpenGL.GL import *
from OpenGL.GLU import *

from database import config as cfg
from controllers.Renderable import Renderable
from useCaseClasses.CalorimeterManager import CalorimeterManager

class CalorimeterController():
    def __init__(self, caloManager:CalorimeterManager) -> None:
        self.calo_manager = caloManager
        
        self.SD_namelist = cfg.sub_detector_namelist
        self.SD_colorlist = cfg.sub_detector_colorlist
        self.SD_sizelist = cfg.sub_detector_sizelist
        self.SD_controllers = {}
        
        for idx, samp_name in enumerate(self.SD_namelist):
            SD_cells = self.calo_manager.getCalorimeterCells(samp_name)
            SD_controller = SubDetectorController(SD_cells, size=self.SD_sizelist[idx], color=self.SD_colorlist[idx])
            self.SD_controllers[samp_name] = SD_controller
    
           
    def getSubDetector(self, samp_name: str) -> Renderable:
        return self.SD_controllers[samp_name]
    
    def getAllSubDetector(self):
        return self.SD_controllers


class SubDetectorController(Renderable):
    def __init__(self, SD_cells, size=1.5, color=(0,0,0)):
        self.cells_coords = SD_cells   # List((float, float, float))
        self.point_size = size 
        self.color = color
        
    def render(self, target_stage):
        if not self.cells_coords:
            # Check if list of cell coord is empty, should neve get here
            return
        
        glPointSize(self.point_size)
        glColor3f(*self.color)
        glBegin(GL_POINTS)
        for cell_coord in self.cells_coords:
            glVertex3f(*cell_coord)
        glEnd()
            
            
            
