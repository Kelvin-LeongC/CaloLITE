from abc import ABC, abstractclassmethod
from OpenGL.GL import *
from OpenGL.GLU import *
from PySide6.QtGui import QPainter, QFont
from PySide6.QtCore import Qt

# ==== Renderable Interface ====
class Renderable(ABC):
    @abstractclassmethod
    def render(self, target_stage):
        pass
    
    
class Cell(Renderable):
    def __init__(self, coords, size=1.0, color=(0,0,0)):
        self.x, self.y, self.z = coords
        self.size = size
        self.color = color
        
    def render(self, target_stage):
        glPointSize(self.size)
        glColor3f(*self.color)
        glBegin(GL_POINTS)
        glVertex(self.x, self.y, self.z)
        glEnd()



class Axis(Renderable):
    def __init__(self, r_axis_length=4.0, z_axis_length=6.5, cylinder_radius=0.025):
        self.r_axis_length = r_axis_length
        self.z_axis_length = z_axis_length
        self.cylinder_radius = cylinder_radius
        self.quadric = gluNewQuadric()
        # Optional: Set drawing style for the quadric if needed
        #gluQuadricDrawStyle(self.quadric, GLU_FILL) # Default is GLU_FILL
        #gluQuadricNormals(self.quadric, GLU_SMOOTH) # For lighting
        
    def __del__(self):
        # Clean up the quadric object when the Axis instance is deleted
        if self.quadric:
            gluDeleteQuadric(self.quadric)
            self.quadric = None
            
    def render(self, target_stage):
        self._render_axis()
        self._render_label(target_stage)
        
    def _render_axis(self):
        slices = 16  # Number of subdivisions around the axis (complexity of cylinder)
        stacks = 1   # Number of subdivisions along the axis

        # R-axis (red)
        glColor3f(1, 0, 0)
        glPushMatrix()
        glRotatef(90.0, 0.0, 1.0, 0.0)  # Rotate 90 degrees around Y-axis
        gluCylinder(self.quadric, self.cylinder_radius, self.cylinder_radius, self.r_axis_length, slices, stacks)
        glPopMatrix()
        
        # Z-axis (blue)
        glColor3f(0, 0, 1)
        glPushMatrix()
        gluCylinder(self.quadric, self.cylinder_radius, self.cylinder_radius, self.z_axis_length, slices, stacks)
        glPopMatrix()

        
    def _render_label(self, target_stage):
        painter = QPainter(target_stage)
        try:
            mv = glGetDoublev(GL_MODELVIEW_MATRIX)
            pr = glGetDoublev(GL_PROJECTION_MATRIX)
            vp = glGetIntegerv(GL_VIEWPORT)

            # Ensure viewport has valid dimensions
            if vp[2] == 0 or vp[3] == 0:
                return

            painter.setPen(Qt.black)
            painter.setFont(QFont('Sans', 10))
            
            # r-axis label
            for i in range(0, int(self.r_axis_length) + 1):
                try:
                    xw, yw, zw = gluProject(float(i), 0.0, 0.0, mv, pr, vp)
                    # zw is in [0,1] if the point is between near and far planes
                    if 0.0 <= zw <= 1.0: 
                        painter.drawText(int(xw), int(vp[3] - yw), f"{i} m")
                except ValueError:
                    # Skip drawing this label if projection fails
                    pass 
                
            # z-axis label
            for i in range(0, int(self.z_axis_length) + 1):
                try:
                    xw, yw, zw = gluProject(0.0, 0.0, float(i), mv, pr, vp)
                    if 0.0 <= zw <= 1.0:
                        painter.drawText(int(xw), int(vp[3] - yw), f"{i} m")
                except ValueError:
                    # Skip drawing this label if projection fails
                    pass 
        finally:
            painter.end()
            