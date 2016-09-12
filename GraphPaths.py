import sys, time;
# from mathtoolbox import ensurelookuptable;
from chenhan_pp.MeshTools import ensurelookuptable;
from chenhan_pp.CICHWithFurtherPriorityQueue import CICHWithFurtherPriorityQueue
# from chenhan.geodesics import CICHWithFurtherPriorityQueue;

class GraphPaths:
    #Reference to the blender object;
    m_mesh = None;
    #Reference to the bm_data;
    m_bmesh = None;
    #Reference to the blender context;
    m_context = None;
    #indices of seed paths;
    m_seed_indices = None;
    
    def __init__(self, context, mesh, bm_mesh):
        self.m_mesh = mesh;
        self.m_bmesh = bm_mesh;
        self.m_context = context;
        self.m_seed_indices = [];
    
    
    def removeSeedIndex(self, seed_index):
        try:
            index = self.m_seed_indices.index(seed_index);
            self.m_seed_indices.remove(seed_index);
            return index;
        except ValueError:
            return -1;
    
    def addSeedIndex(self, seed_index, passive=False):
        try:
            self.m_seed_indices.index(seed_index);
        except ValueError:
            self.m_seed_indices.append(seed_index);
    
    def path_between(self, seed_index, target_index):        
        return [];
    
    def getSeedIndices(self):
        return self.m_seed_indices;


class ChenhanGeodesics(GraphPaths):
    
    m_all_geos = None;
    m_richmodel = None;
    algo = None;
    
    def __init__(self, context, mesh, bm_mesh, richmodel):
        super().__init__(context, mesh, bm_mesh);
        self.m_all_geos = [];
        self.m_richmodel = richmodel;
        ensurelookuptable(bm_mesh);
#         self.algo = CICHWithFurtherPriorityQueue(inputModel=self.m_richmodel, indexOfSourceVerts=[v.index for v in bm_mesh.verts]);
#         self.algo.Execute();
#         self.algo.PickShortestPaths(self.m_richmodel.GetNumOfVerts());
#         print('TABLE OF RESULTING PATHS ::: ');
#         print(self.algo.m_tableOfResultingPaths[0], self.m_richmodel.Vert(0));
        
    def addSeedIndex(self, seed_index, passive=False):
        super().addSeedIndex(seed_index);
        index = self.m_seed_indices.index(seed_index);
        if(not passive):
            try:
                geos_index = self.m_all_geos[index];
            except IndexError:
                alg = None;
                start = time.time();
                alg = CICHWithFurtherPriorityQueue(inputModel=self.m_richmodel, indexOfSourceVerts=[seed_index]);
                alg.Execute();
                end = time.time();
                print('TOTAL TIME FOR SEEDING ::: ', (end - start)," seconds");
                self.m_all_geos.append(alg);
#                 self.m_all_geos.append(self.algo);
        else:
            self.m_all_geos.append(None);
    
    def removeSeedIndex(self, seed_index):
        removed_index = super().removeSeedIndex(seed_index);
        if(removed_index != -1):
            del self.m_all_geos[removed_index];
            
    def path_between(self, seed_index, target_index):        
        try:
            indice = self.m_seed_indices.index(seed_index);
            
            if(not self.m_all_geos[indice]):
                alg = None;
                alg = CICHWithFurtherPriorityQueue(inputModel=self.m_richmodel, indexOfSourceVerts=[seed_index]);
                alg.Execute();
#                 self.m_all_geos[indice] = alg;
#                 ensurelookuptable(self.m_bmesh);
#                 self.algo = CICHWithFurtherPriorityQueue(inputModel=self.m_richmodel, indexOfSourceVerts=[v.index for v in self.m_bmesh.verts]);
#                 self.algo.Execute();
#                 self.m_all_geos[indice] = self.algo;
            
            pathp3d, sourceindex = self.m_all_geos[indice].FindSourceVertex(target_index);
            path = [];
#             print('SOURCE INDEX ::: ', sourceindex, ' GIVEN SEED INDEX ::: ', seed_index, ' GIVEN TARGET INDEX ', target_index);
#             print('TABLE OF RESULTING PATHS ::: ');
#             print(self.algo.m_tableOfResultingPaths);
            
            
            for eitem in pathp3d:
                vco = eitem.Get3DPoint(self.m_richmodel);
                path.append(self.m_mesh.matrix_world *  vco);
            
            return path;
        
        except ValueError:
            print("THE intended seed_index does not exist, so returning NONE");
            return None;
        
        