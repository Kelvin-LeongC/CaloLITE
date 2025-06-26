sub_detector_namelist =["PreSamplerB", "EMB1", "EMB2", "EMB3",        # 0, 1, 2, 3
                        "PreSamplerE", "EME1", "EME2", "EME3",        # 4, 5, 5, 7
                        "HEC0", "HEC1", "HEC2", "HEC3",               # 8, 9, 10, 11
                        "TileBar0", "TileBar1", "TileBar2",           # 12, 13, 14 
                        "TileGap1", "TileGap2", "TileGap3",           # 15, 16, 17
                        "TileExt0", "TileExt1", "TileExt2",           # 18, 19, 20
                        "FCAL0", "FCAL1", "FCAL2"                     # 21, 22, 23
                       ]

sub_detector_colorlist = [(0.73, 0, 0.11),          # PreSamplerB
                          (0.18, 0.58, 1.0),        # EMB1
                          (0.01, 0.44, 0.88),       # EMB2
                          (0.01, 0.34, 0.67),       # EMB3
                          (0.73, 0, 0.11),          # PreSamplerE
                          (0.18, 0.58, 1.0),        # EME1
                          (0.01, 0.44, 0.88),       # EME2
                          (0.01, 0.34, 0.67),       # EME3
                          (0.18, 0.72, 0.51),       # HEC0
                          (0.12, 0.70, 0.47),       # HEC1
                          (0.01, 0.67, 0.41),       # HEC2
                          (0.06, 0.45, 0.11),       # HEC3
                          (0.83, 0.42, 0.03),       # TileBar0
                          (0.89, 0.45, 0.07),       # TileBar1
                          (1.0, 0.56, 0),           # TileBar2
                          (0.9, 0.06, 0.88),        # TileGap1
                          (0.61, 0.06, 0.9),        # TileGap2
                          (0.73, 0, 0.11),          # TileGap3
                          (0.49, 0.73, 0),          # TileExt0
                          (1, 0, 0.73),             # TileExt1
                          (0.31, 0.37, 0),          # TileExt2
                          (0.42, 0.42, 0.42),       # FCAL0
                          (0.21, 0.21, 0.21),       # FCAL1
                          (0, 0, 0),                # FCAL2
                          ]

sub_detector_sizelist = [1.5, 1.5, 1.5, 1.5,        # PreSamplerB, EMB1, EMB2, EMB3
                         1.5, 1.5, 1.5, 1.5,        # PreSamplerE, EME1, EME2, EME3
                         1.5, 1.5, 1.5, 1.5,        # HEC0, HEC1, HEC2, HEC3
                         2.5, 2.5, 2.5,             # TileBar0, TileBar1, TileBar2
                         2.5, 2.5, 2.5,             # TileGap1, TileGap2, TileGap3
                         2.5, 2.5, 2.5,             # TileExt0, TileExt1, TileExt2
                         1.5, 1.5, 1.5              # FCAL0, FCAL1, FCAL2
                        ]

detector_group_definitions = {
            "EM Barrel": ["PreSamplerB", "EMB1", "EMB2", "EMB3"],
            "EM Endcap": ["PreSamplerE", "EME1", "EME2", "EME3"],
            "Hadronic Endcap": ["HEC0", "HEC1", "HEC2", "HEC3"],
            "Tile Barrel": ["TileBar0", "TileBar1", "TileBar2"],
            "Tile Gap": ["TileGap1", "TileGap2", "TileGap3"],
            "Tile Extension": ["TileExt0", "TileExt1", "TileExt2"],
            "Forward Calorimeter": ["FCAL0", "FCAL1", "FCAL2"],
}


clusters_color_choices = [(1, 0, 0),
                          (1, 0.31, 0),
                          (1, 0.48, 0),
                          (0.36, 1, 0),
                          (0, 1, 0.63),
                          (0, 1, 0.94)]