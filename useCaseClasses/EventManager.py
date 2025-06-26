import uproot
import numpy as np
from tqdm import tqdm
import awkward as ak

class EventManager:
    def __init__(self, file_name, tree_name, cell_coord_branch_prefix):
        self.fileName = file_name
        self.treeName = tree_name
        self.branch_prefix = cell_coord_branch_prefix
        
        with uproot.open(self.fileName) as f:
            tree = f[self.treeName]
            
            self.event_number_awkarr = tree['eventNumber'].array()
            self.truthPartEta_awkarr = tree['truthPartEta'].array()
            self.truthPartPhi_awkarr = tree['truthPartPhi'].array()
            
            self.cluster_cell_X_awkarr = tree[f'{self.branch_prefix}_X'].array() / 1000 #[m]
            self.cluster_cell_Y_awkarr = tree[f'{self.branch_prefix}_Y'].array() / 1000 #[m]
            self.cluster_cell_Z_awkarr = tree[f'{self.branch_prefix}_Z'].array() / 1000 #[m]
            

        self.trajectory_length = 10.0
        self.map_evtnum_truthPartEndTrajEtaPhi = {}
        self._storeMapTrajEtaPhi()
        print("Finished Loading all Events EtaPhi Trajectory")
        self.map_evtnum_truthPartEndTrajXYZ = {}
        self._storeMapTrajXYZ()
        print("Finished Loading all Events XYZ Trajectory")
        self.map_evtnum_ClustersCellsCoord = {}
        self._storeMapClustersCellsCoor()
        print("Finished Loading all Events Cluster Cells Coordinates")
        
        self.event_number_sorted_list = sorted(self.event_number_awkarr.tolist())
        
    # (Public) Return a list of all event numbers
    def getEventNumbers(self):
        return self.event_number_sorted_list
    
    def getTruthEndTrajXYZforAnEvent(self, evtnum: int):
        return self.map_evtnum_truthPartEndTrajXYZ[evtnum]
    
    def getTruthEndTrajEtaPhiforAnEvent(self, evtnum: int):
        return self.map_evtnum_truthPartEndTrajEtaPhi[evtnum]
    
    def getClustersCellsCoordforAnEvent(self, evtnum: int):
        return self.map_evtnum_ClustersCellsCoord[evtnum]
    
    
    def _storeMapClustersCellsCoor(self):
        coords_awk = ak.zip([self.cluster_cell_X_awkarr, self.cluster_cell_Y_awkarr, self.cluster_cell_Z_awkarr])
        coords_list_of_lists_of_tuples = ak.to_list(coords_awk)
        
        for i, evtnum in tqdm(enumerate(self.event_number_awkarr), desc="Processing Clusters Cells Coordinates", total=len(self.event_number_awkarr)):
            clusters_data_for_event = coords_list_of_lists_of_tuples[i]
            self.map_evtnum_ClustersCellsCoord[evtnum] = [[tuple(cell_coords) for cell_coords in cluster_data] for cluster_data in clusters_data_for_event]
    
    def _calculateTruthTrajectoryXYZ(self):
        theta = 2 * np.arctan(np.exp(self.truthPartEta_awkarr))
        r = self.trajectory_length * np.sin(theta)
        
        x = r * np.cos(self.truthPartPhi_awkarr)
        y = r * np.sin(self.truthPartPhi_awkarr)
        z = 0.5 * r * (np.exp(self.truthPartEta_awkarr) - np.exp(-self.truthPartEta_awkarr))
        
        return x, y, z
        
    def _storeMapTrajXYZ(self):
        truthPartX_awkarr, truthPartY_awkarr, truthPartZ_awkarr = self._calculateTruthTrajectoryXYZ()
        xyz_awk = ak.zip([truthPartX_awkarr, truthPartY_awkarr, truthPartZ_awkarr])
        xyz_awk_list = ak.to_list(xyz_awk)

        for i, evtnum in tqdm(enumerate(self.event_number_awkarr), desc="Processing Trajectory XYZ", total=len(self.event_number_awkarr)):
            xyz_awk_for_event = xyz_awk_list[i]
            self.map_evtnum_truthPartEndTrajXYZ[evtnum] = [tuple(xyz_traj) for xyz_traj in xyz_awk_for_event]

            
    def _storeMapTrajEtaPhi(self):
        eta_phi_awk = ak.zip([self.truthPartEta_awkarr, self.truthPartPhi_awkarr])
        eta_phi_awk_list = ak.to_list(eta_phi_awk)
        
        for i, evtnum in tqdm(enumerate(self.event_number_awkarr), desc="Processing Trajectory EtaPhi", total=len(self.event_number_awkarr)):
            eta_phi_awk_for_event = eta_phi_awk_list[i]
            self.map_evtnum_truthPartEndTrajEtaPhi[evtnum] = [tuple(eta_phi_traj) for eta_phi_traj in eta_phi_awk_for_event]
            
#if __name__ == '__main__':
#    EventManager("../database/piplus.mltree.root")