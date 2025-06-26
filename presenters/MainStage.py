from OpenGL.GL import *
from OpenGL.GLU import *
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt, QPoint

from controllers.Renderable import Axis
from controllers.CalorimeterController import SubDetectorController
from controllers.EventController import EventController
from presenters.Scene import Scene


class MainStage(QOpenGLWidget):
    def __init__(self, scene:Scene, axis:Axis, subDetectorControllers:dict[str, SubDetectorController], eventController: EventController, parent=None):
        super().__init__(parent)
        self.lastPos = QPoint()
        self.xRot = 0.0
        self.yRot = 0.0
        self.zoom = 1.0
        self.xTrans = 0.0
        self.yTrans = 0.0
        self.cam_dist_init = 15
        self.translation_sensitivity = 0.03 # Adjust for desired panning speed
        
        self.axis = axis
        self.show_axis = True
        
        self.subDetectorControllers = subDetectorControllers
        self.subDetectorNames = list(subDetectorControllers.keys())
        self.subDetector_visibilities = {}
        for name in self.subDetectorNames:
            self.subDetector_visibilities[name] = True
        
        self.eventController = eventController
        
        self.scene = scene
        self.scene.add(axis)
        for controller in self.subDetectorControllers.values():
            self.scene.add(controller)
        self.scene.add(eventController)
        
    # =====================================================================
    # Basic camera/interactive window controls
    
    def initializeGL(self):
        glClearColor(0.8, 0.8, 0.8, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_POINT_SMOOTH)
        
    def resizeGL(self, w, h):
        if h == 0: return
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, w/h, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
    
    def mousePressEvent(self, event):
        self.lastPos = event.position().toPoint() if hasattr(event, 'position') else event.pos()
        
    def mouseMoveEvent(self, event):
        pos = event.position().toPoint() if hasattr(event, 'position') else event.pos()
        dx = pos.x() - self.lastPos.x()
        dy = pos.y() - self.lastPos.y()
        if event.buttons() & Qt.LeftButton:
            self.xRot += dy
            self.yRot += dx
            self.update()
        elif event.buttons() & Qt.MiddleButton:
            effective_sensitivity = self.translation_sensitivity / self.zoom
            self.xTrans += dx * effective_sensitivity
            self.yTrans -= dy * effective_sensitivity # Screen Y is inverted relative to OpenGL Y
            self.update()
        self.lastPos = pos
        
    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 360 
        self.zoom = max(0.1, min(self.zoom + delta*0.1, 10.0))
        self.update()
        
    def resetCamera(self):
        self.lastPos = QPoint()
        self.xRot = 0.0
        self.yRot = 0.0
        self.zoom = 1.0
        self.xTrans = 0.0
        self.yTrans = 0.0
        self.cam_dist_init = 15
        self.update()
        
    # ==============================================================================================
        
        
    # Render objects on scene, and controls over how it supposed to be rendered on scene
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Apply camera pull-back and panning
        glTranslatef(0.0, 0.0, -self.cam_dist_init)
        glTranslatef(self.xTrans, self.yTrans, 0.0) 
        
        glScalef(self.zoom, self.zoom, self.zoom)
        glRotatef(self.xRot, 1.0, 0.0, 0.0)
        glRotatef(self.yRot, 0.0, 1.0, 0.0)
        
        self.scene.render_all(self)
        
    def set_axis_visibility(self, visible: bool):
        self.show_axis = visible
        if self.show_axis:
            self.scene.add(self.axis)
        else:
            self.scene.remove(self.axis)
            
        # Request repaint after changing scene content
        self.update() 

    def set_sub_detector_visibility(self, name: str, visible: bool):
        self.subDetector_visibilities[name] = visible
        if visible:
            self.scene.add(self.subDetectorControllers[name])
        else:
            self.scene.remove(self.subDetectorControllers[name])

        self.update()
        
    def changeEventDisplay(self, eventNumber: int):
        self.eventController.updateTargetEventDisplay(eventNumber)
        self.update()
        
    def resetEventDisplay(self):
        self.eventController.reset()
        self.update()