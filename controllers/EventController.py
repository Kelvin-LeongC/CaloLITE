from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from database import config as cfg
from useCaseClasses.EventManager import EventManager
from controllers.Renderable import Renderable


class EventController(Renderable):
    def __init__(self, eventManager: EventManager):
        self.eventManager = eventManager
        self.targetEvt_num = None
        self.targetEvt_TruthEndTrajXYZ = None       # Now a list of tuples: [(x1,y1,z1), (x2,y2,z2), ...]
        self.targetEvt_TruthEndTrajEtaPhi = None
        self.targetEvt_ClustersCellsCoord = None    # [cluster 1: [cell 1: (x1, y1, z1), cell2: (x2, y2, z2)], cluster 2: [...], ... ]
        self.point_size = 8.0
        self.color_choices = cfg.clusters_color_choices                      
    
    def updateTargetEventDisplay(self, targetEvt_num):
        self.targetEvt_num = targetEvt_num
        self.targetEvt_TruthEndTrajXYZ = self.eventManager.getTruthEndTrajXYZforAnEvent(self.targetEvt_num)
        self.targetEvt_TruthEndTrajEtaPhi = self.eventManager.getTruthEndTrajEtaPhiforAnEvent(self.targetEvt_num)
        self.targetEvt_ClustersCellsCoord = self.eventManager.getClustersCellsCoordforAnEvent(self.targetEvt_num)

        print(f"EventController: Updated target trajectory for event {self.targetEvt_num}: ")
        for particle_idx in range(len(self.targetEvt_TruthEndTrajXYZ)):
            print(f"    Particle {particle_idx}: (Eta,Phi)=({self.targetEvt_TruthEndTrajEtaPhi[particle_idx][0]:.3f}, {self.targetEvt_TruthEndTrajEtaPhi[particle_idx][1]:.3f}); \
                  (x,y,z)=({self.targetEvt_TruthEndTrajXYZ[particle_idx][0]:.3f}, {self.targetEvt_TruthEndTrajXYZ[particle_idx][1]:.3f}, {self.targetEvt_TruthEndTrajXYZ[particle_idx][2]:.3f})")
        for cluster_idx in range(len(self.targetEvt_ClustersCellsCoord)):
            print(f"    Cluster {cluster_idx}: {len(self.targetEvt_ClustersCellsCoord[cluster_idx])} cell(s)")

    def reset(self):
        self.targetEvt_num = None
        self.targetEvt_TruthEndTrajXYZ = None
        self.targetEvt_TruthEndTrajEtaPhi = None
        self.targetEvt_ClustersCellsCoord = None
        
    def render(self, target_stage):
        self._render_truth_trajectory()
        self._render_cluster_cells()
    
    def _render_cluster_cells(self):
        if self.targetEvt_ClustersCellsCoord is not None:
            for cluster_idx in range(len(self.targetEvt_ClustersCellsCoord)):
                color = self.color_choices[cluster_idx % len(self.color_choices)]
                glPointSize(self.point_size)
                glColor3f(*color)
                glBegin(GL_POINTS)
                cell_coords = self.targetEvt_ClustersCellsCoord[cluster_idx]
                for cell_coord in cell_coords:
                    glVertex3f(*cell_coord)
                glEnd()
            
    def _render_truth_trajectory(self):
        # self.targetEvt_TruthEndTrajXYZ is now a list of (x,y,z) tuples, or None
        if self.targetEvt_TruthEndTrajXYZ is not None:
            for particle_traj_coords in self.targetEvt_TruthEndTrajXYZ:
                try:
                    # Check for non-finite values (NaN, inf) for this specific particle's trajectory
                    if any(not np.isfinite(coord) for coord in particle_traj_coords):
                        print(f"Warning: Non-finite coordinates in a particle trajectory for event {self.targetEvt_num}: {particle_traj_coords}")
                        continue # Skip this particle's trajectory, try the next

                    glBegin(GL_LINES)
                    glColor3f(0.0, 0.0, 0.0) 
                    glVertex3f(0.0, 0.0, 0.0)           # Start trajectory from origin
                    glVertex3f(*particle_traj_coords)   # End at the calculated trajectory point
                    glEnd()

                except TypeError as e:
                    print(f"Error rendering a particle trajectory (TypeError) for event {self.targetEvt_num}: {e}")
                    print(f"Problematic particle_traj_coords was: {particle_traj_coords}, type: {type(particle_traj_coords)}")
                except Exception as e:
                    print(f"Unexpected error rendering a particle trajectory for event {self.targetEvt_num}: {e}")
                    print(f"Problematic particle_traj_coords was: {particle_traj_coords}")