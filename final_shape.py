

import os
import sys
import bpy
import math
import shutil

argv_ori = sys.argv
argv = argv_ori[argv_ori.index("--") + 1:argv_ori.index("++")]

model_name = argv[0]
igname = argv[1]

Scenename = 'Scene'

for item in bpy.data.objects:
	if item.type == "MESH":
		bpy.data.objects[item.name].select = True
	if item.type != "MESH":
		bpy.data.objects[item.name].select = False

bpy.ops.object.delete()
for item in bpy.data.meshes:
	bpy.data.meshes.remove(item)


#model
bpy.ops.import_scene.obj(filepath=model_name)






mat_name = "Material"
image_path = igname

mat = (bpy.data.materials.get(mat_name))# or bpy.data.materials.new(mat_name))

mat.use_nodes = True
nt = mat.node_tree
nodes = nt.nodes
links = nt.links

# clear
while(nodes): nodes.remove(nodes[0])

output  = nodes.new("ShaderNodeOutputMaterial")
diffuse = nodes.new("ShaderNodeBsdfDiffuse")
texture = nodes.new("ShaderNodeTexImage")
#uvmap   = nodes.new("ShaderNodeUVMap")

texture.image = bpy.data.images.load(image_path)
#uvmap.uv_map = "UV"

links.new( output.inputs['Surface'], diffuse.outputs['BSDF'])
links.new(diffuse.inputs['Color'],   texture.outputs['Color'])
#links.new(texture.inputs['Vector'],    uvmap.outputs['UV'])

bpy.data.materials['Material'].node_tree.nodes["Diffuse BSDF"].inputs[1].default_value = 1

for item in bpy.data.objects:
	if item.type == "MESH":
		if item.name.rfind('0') >= 0:
			item.data.materials.append(bpy.data.materials['Material'])


for item in bpy.data.objects:
	if item.type == "MESH":			
		if item.name.rfind('0') < 0:
			bpy.ops.material.new()
			bpy.data.materials['Material.001'].node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = (0.1,0.1,0.1,1) 
			bpy.data.materials['Material.001'].node_tree.nodes["Diffuse BSDF"].inputs[1].default_value = 1
			item.data.materials.append(bpy.data.materials['Material.001'])

bpy.data.scenes['Scene'].render.filepath = igname[0:-21]+'_relighting.png'
bpy.context.scene.camera = bpy.data.objects['Camera']
bpy.ops.render.render(animation=False,write_still=True,scene=Scenename)


#bpy.ops.export_scene.obj(filepath = igname[0:-21]+'_shape_final_mat.obj', use_materials = True)


bpy.ops.wm.save_as_mainfile(filepath = igname[0:-21]+'_relighting_final.blend')
