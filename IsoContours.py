import gc
# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import bpy, bmesh, bgl, math, os, mathutils, sys;
import blf, time, datetime;
from bpy_extras.view3d_utils import location_3d_to_region_2d, region_2d_to_vector_3d, region_2d_to_location_3d, region_2d_to_origin_3d
from bpy_extras import view3d_utils;


from bpy.props import StringProperty;
from bpy.props import FloatVectorProperty;
from mathutils import Vector, Matrix;
from mathutils.bvhtree import BVHTree;

from chenhan_pp.MeshData import RichModel
from chenhan_pp.CICHWithFurtherPriorityQueue import CICHWithFurtherPriorityQueue
from chenhan_pp.helpers import getBMMesh, ensurelookuptable, getBarycentricCoordinate, getCartesianFromBarycentre, getTriangleArea, getGeneralCartesianFromPolygonFace;
from chenhan_pp.helpers import buildKDTree, getDuplicatedObject, getQuadMesh;
from chenhan_pp.helpers import getScreenLookAxis, drawLine, drawText, drawTriangle, ScreenPoint3D, createIsoContourMesh;
from chenhan_pp.helpers import getTriangleMappedPoints, getBarycentricValue, getMappedContourSegments;

__date__ ="$Mar 23, 2015 8:16:11 PM$"

def DrawGL(self, context):
    bgl.glEnable(bgl.GL_DEPTH_TEST);
    if(context.scene.showisolines):
        bgl.glDisable(bgl.GL_DEPTH_TEST);
        bgl.glColor4f(*(1.0, 1.0, 0.0,1.0));
        bgl.glPointSize(15.0);
        bgl.glBegin(bgl.GL_POINTS);
        bgl.glVertex3f(*self.highlight_point);
        bgl.glEnd();
        bgl.glEnable(bgl.GL_DEPTH_TEST);
        if(len(self.isolines)):            
            bgl.glColor4f(*(0.0, 1.0, 0.0,1.0));
            bgl.glPointSize(15.0);
            bgl.glBegin(bgl.GL_POINTS);
            bgl.glVertex3f(*self.isoorigin);
            bgl.glEnd();        
            
            for segment in self.isolines:
                drawLine(segment['start'], segment['end'], 1.0, (0.0, 0.0, 0.0,1.0));
            
            bgl.glDisable(bgl.GL_DEPTH_TEST);
            
            drawText(context, "Iso Origin", self.isoorigin);
    
    # restore opengl defaults
    bgl.glLineWidth(1);
    bgl.glDisable(bgl.GL_BLEND);
    bgl.glEnable(bgl.GL_DEPTH_TEST);
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0);

class IsoContours(bpy.types.Operator):
    """Draw a line with the mouse"""
    bl_idname = "ashok.isocontours";
    bl_label = "Isolines Visualizer";
    bl_description = "Given a mesh show isolines"
    hit = FloatVectorProperty(name="hit", size=3);    
    
    def getWorldFacePoint(self, context, mesh, face):
        arr = [];
        path = [mesh.data.vertices[vindex].co for vindex in face.vertices];
        for co in path:
            arr.append(mesh.matrix_world * co);
        
        return arr;    
    
#     def saveIsoContoursMesh(self, context):
        
    
    def modal(self, context, event):
        region = context.region;
        rv3d = context.region_data;
        obj = context.active_object;
        context.area.tag_redraw();
        
        if(not context.scene.isolinesupdated and self.alg):
            self.isolines = self.alg.GetIsoLines(self.subject.isolines_count+1);
            createIsoContourMesh(context, self.subject, self.isolines);   
            
            for segment in self.isolines:
                segment['start'] = self.subject.matrix_world * segment['start'];
                segment['end'] = self.subject.matrix_world * segment['end'];
            
            context.scene.isolinesupdated = True;
        
        
        if event.type in {'ESC'}:       
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW'); 
            return {'CANCELLED'}
        
        elif(event.type == 'I' and event.value == 'PRESS'):
            diffkey = time.time() - self.lastkeypress;
            if(diffkey > 3):
                self.lastkeypress = time.time();
                if(event.type == "I"):
                    self.hit, onMesh, face_index, hitpoint = ScreenPoint3D(context, event, self.subject, position_mouse = False);
                    if(self.richmodel):
                        vco, vindex, dist = self.kd.find(hitpoint);
                        self.alg = CICHWithFurtherPriorityQueue(inputModel=self.richmodel, indexOfSourceVerts=[vindex]);
                        self.alg.Execute();
                        self.isoorigin = self.subject.matrix_world * self.subject.data.vertices[vindex].co;
                        context.scene.isolinesupdated = False;
                        return {'RUNNING_MODAL'};
        
        elif(event.type == 'MOUSEMOVE'):
            self.hit, onMesh, face_index, hitpoint = ScreenPoint3D(context, event, self.subject, position_mouse = False);
            if(onMesh):
                if(face_index):
                    vco, vindex, dist = self.kd.find(hitpoint);
                    self.highlight_point = self.subject.matrix_world * self.subject.data.vertices[vindex].co;        
        
        return {'PASS_THROUGH'};
        
    def invoke(self, context, event):
        if(context.active_object):
            self.subject = context.active_object;            
            bm = getBMMesh(context, self.subject, False);            
            try:
                self.richmodel = RichModel(bm, self.subject);
                self.richmodel.Preprocess();
            except: 
                self.richmodel = None;
            
            self.alg = None;
            self.isolines = [];
            self.isoorigin = ();
            self.highlight_point = (0,0,0);
            self.kd = buildKDTree(context, self.subject, type="VERT");
            self.lastkeypress = time.time();
            
            context.scene.objects.active = self.subject;
            self.subject.select = True;
            args = (self, context); 
            self._handle = bpy.types.SpaceView3D.draw_handler_add(DrawGL, args, 'WINDOW', 'POST_VIEW');
            context.window_manager.modal_handler_add(self);
        return {'RUNNING_MODAL'}