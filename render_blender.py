import sys
import bpy
import math

# Capturar argumentos pasados desde Streamlit
args = sys.argv[sys.argv.index("--") + 1:]
color_r = float(args[0])
color_g = float(args[1])
color_b = float(args[2])
fps = int(args[3])
frames_totales = int(args[4])

# Limpiar la escena por defecto
bpy.ops.wm.read_factory_settings(use_empty=True)

# Crear Cámara
bpy.ops.object.camera_add(location=(0, -5, 2), rotation=(math.radians(70), 0, 0))
camera = bpy.context.object
bpy.context.scene.camera = camera

# Crear Luz
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))

# Crear Objeto 3D (ejemplo: Cubo)
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
cubo = bpy.context.object

# Aplicar Material y Color
mat = bpy.data.materials.new(name="MaterialCubo")
mat.use_nodes = True
nodes = mat.node_tree.nodes
bsdf = nodes.get("Principled BSDF")
bsdf.inputs['Base Color'].default_value = (color_r, color_g, color_b, 1.0)
cubo.data.materials.append(mat)

# Configurar Animación (Rotación de 360 grados)
cubo.rotation_euler = (0, 0, 0)
cubo.keyframe_insert(data_path="rotation_euler", frame=1)

cubo.rotation_euler = (0, 0, math.radians(360))
cubo.keyframe_insert(data_path="rotation_euler", frame=frames_totales)

# Ajustar configuración de Renderizado
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types, 'BLENDER_EEVEE_NEXT') else 'BLENDER_EEVEE'
scene.render.fps = fps
scene.frame_start = 1
scene.frame_end = frames_totales

# Ajustes de salida de Video MP4
scene.render.filepath = "/tmp/output_render.mp4"
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'

# Ejecutar Renderizado
bpy.ops.render.render(animation=True)
