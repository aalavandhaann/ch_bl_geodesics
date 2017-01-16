'''
Created on Jun 30, 2016

@author: ashok
'''
import bpy;
from bpy.props import *;
from chenhan_pp.ChenhanOperator import ChenhanGeodesicsOperator;
from chenhan_pp.IsoContours import IsoContours;

bl_info = {
    "name": "Chenhan Geodesics",
    "version": (1, 0),
    "blender": (2, 7, 6),
    "location": "View3D > Object > Chenhan Geodesics",
    "description": "Chenhan geodesics demonstration using Blender",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

if "bpy" in locals():
    import imp;
    print("Reloaded multifiles");
else:
    print("Imported multifiles")

class ChenhanGeodesicsPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_chenhangeodesicpanel"
    bl_label = "Chenhan Geodesic";
    bl_space_type = "VIEW_3D";
    bl_region_type = "TOOLS";
    bl_category = "GEODESICS";
    
    def draw(self, context):        
        #The button to load the humma file and do all preprocessing        
        if(context.active_object):
            layout = self.layout;
            
            row = layout.row(align=True);
            row.prop(context.active_object, "show_wire", "Wireframe");
                        
            row = layout.row(align=True);
            row.prop(context.active_object, "show_all_edges", "Show All Edges");
            
            row = layout.row(align=True);
            row.prop(context.scene, "path_color", "Path Color");            
            
            row = layout.row(align=True);
            row.prop(context.scene, "temp_path_color", "Temp path color");
            
            row = layout.row(align=True);
            row.operator(ChenhanGeodesicsOperator.bl_idname, text="Geodesics");
            
            row = layout.row(align=True);
            row.prop(context.active_object, "isolines_count", "IsoLines Count");
            
            row = layout.row(align=True);
            row.operator(IsoContours.bl_idname, text="IsoContours");

bpy.types.Object.isolines_count = bpy.props.IntProperty(name="Isolines count", description="Total IsoLines", default=10, min=1, max=100);

bpy.types.Scene.path_color = bpy.props.FloatVectorProperty(
    name = "Geodesic Path Color", 
    subtype='COLOR', 
    default=[0.0,0.0,1.0], 
    description = "Color of the geodesic path from normal mesh");

bpy.types.Scene.temp_path_color = bpy.props.FloatVectorProperty(
    name = "Temp Geodesic Path Color", 
    subtype='COLOR', 
    default=[0.5,1.0,1.0], 
    description = "TEMP Color of the geodesic path from normal mesh");
    
    
def register():
    bpy.utils.register_module(__name__);
 
def unregister():    
    bpy.utils.unregister_module(__name__);
 
if __name__ == "__main__":
    register()
