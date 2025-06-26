import uproot
from database import config as cfg

class CalorimeterManager:
    def __init__(self, file_name: str) -> None:
        self.fileName = file_name
        self.treeName = "CellGeo"
        
        with uproot.open(self.fileName) as f:
            tree = f[self.treeName]
            
            self.cell_geo_ID = tree['cell_geo_ID'].array()[0]
            self.cell_geo_samp = tree['cell_geo_sampling'].array()[0]
            self.cell_geo_X = tree['cell_geo_X'].array()[0]
            self.cell_geo_Y = tree['cell_geo_Y'].array()[0]
            self.cell_geo_Z = tree['cell_geo_Z'].array()[0]
            
        self.map_samp_cellsCoord = {} 
        self._makeSubdetectorToCellsCoordMap()
        
    # Map cell coordinates for all 24 sampling layer
    def _makeSubdetectorToCellsCoordMap(self) -> None:
        for samp_num, samp_name in enumerate(cfg.sub_detector_namelist):
            cells_coord = self._makeSampLayerAllCellCoord(samp_num)
            self.map_samp_cellsCoord[samp_name] = cells_coord
            
    # Map cell coordinates for a specific sampling layer
    def _makeSampLayerAllCellCoord(self, samp_num: int):
        cells_X = self.cell_geo_X[self.cell_geo_samp == samp_num] /1000 #[m]
        cells_Y = self.cell_geo_Y[self.cell_geo_samp == samp_num] /1000 #[m]
        cells_Z = self.cell_geo_Z[self.cell_geo_samp == samp_num] /1000 #[m]
        
        cells_coord = list(zip(cells_X, cells_Y, cells_Z))
        return cells_coord
    
    # (Public) Return all cells coordinate for a particular layer 
    def getCalorimeterCells(self, samp_name: str):
        return self.map_samp_cellsCoord[samp_name]
    
    # (Public) Return calorimeter cell namelist
    #def getCalorimeterNames(self):
    #    return cfg.sub_detector_namelist
        

#if __name__ == '__main__':
#    _ = CalorimeterManager("../database/cell_geo+.root")