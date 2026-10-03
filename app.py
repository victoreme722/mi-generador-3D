import streamlit as st
import subprocess
import os

st.set_page_config(page_title="Renderizador 3D Cloud", page_icon="🎬", layout="centered")

st.title("🎬 Creador de Video 3D Animado")
st.write("Genera y renderiza animaciones 3D usando Blender directamente en la nube.")

# Controles de la animación
st.sidebar.header("Parámetros de la Escena")
color_hex = st.sidebar.color_picker("Color del Objeto", "#00FFAA")
fps = st.sidebar.slider("Cuadros por segundo (FPS)", 15, 60, 24)
duracion_seg = st.sidebar.slider("Duración (segundos)", 1, 5, 2)

frames_totales = fps * duracion_seg

# Convertir color Hex a RGB normalizado (0.0 a 1.0)
color_hex = color_hex.lstrip('#')
r, g, b = [int(color_hex[i:i+2], 16) / 255.0 for i in (0, 2, 4)]

if st.button("🚀 Renderizar Video 3D", use_container_width=True):
    with st.spinner("Procesando fotogramas 3D con Blender... esto puede tomar unos segundos."):        
        # Ejecutar Blender en modo Headless (-b)
        cmd = [
            "blender",
            "-b",
            "-P", "render_blender.py",
            "--",
            str(r), str(g), str(b),
            str(fps),
            str(frames_totales)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            video_path = "/tmp/output_render.mp4"
            
            if os.path.exists(video_path):
                st.success("¡Renderizado completado con éxito!")
                st.video(video_path)
                
                # Botón para descargar el archivo .mp4
                with open(video_path, "rb") as file:
                    st.download_button(
                        label="📥 Descargar Video MP4",
                        data=file,
                        file_name="animacion_3d.mp4",
                        mime="video/mp4"
                    )
            else:
                st.error("No se encontró el archivo de video generado.")
                
        except subprocess.CalledProcessError as e:
            st.error("Error durante el renderizado 3D.")
            st.code(e.stderr if e.stderr else e.stdout)
          
