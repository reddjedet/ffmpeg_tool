import subprocess
import os

# --- 1. Definir la ruta de la carpeta de trabajo ---
# Usa una "raw string" (r'...') para evitar problemas con las barras invertidas.
CARPETA_PROYECTO = r' INGRESA AQUÍ LA RUTA DE TU CARPETA '

def check_ffmpeg():
    """Verifica si FFmpeg está instalado y es accesible."""
    try:
        subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_input_file_path():
    """Pide al usuario que ingrese el nombre del archivo y construye la ruta completa."""
    while True:
        input_filename = input(f"Ingresa el nombre del archivo de video (ej: mi_video.mp4): ")
        # 2. Construir la ruta completa del archivo de entrada
        input_file_path = os.path.join(CARPETA_PROYECTO, input_filename)
        
        if os.path.exists(input_file_path):
            return input_file_path, input_filename
        else:
            print(f"❌ Error: El archivo '{input_file_path}' no se encontró. Asegúrate de que el nombre sea correcto.")

def run_ffmpeg_command(command, output_file_path):
    """Ejecuta un comando de FFmpeg y maneja la salida y los errores."""
    print(f"\n🚀 Ejecutando el comando: {' '.join(command)}")
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"✅ ¡Proceso completado! El archivo se ha guardado en '{output_file_path}'")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar FFmpeg: {e}")
        print("Salida de error de FFmpeg:")
        print(e.stderr)

def main_menu():
    """Muestra el menú principal y maneja la selección del usuario."""
    if not check_ffmpeg():
        print("❌ FFmpeg no está instalado o no se encuentra en tu PATH.")
        print("Para usar este script, por favor, instala FFmpeg desde https://ffmpeg.org/download.html")
        return

    while True:
        print("\n--- MENÚ DE PROCESAMIENTO DE VIDEO ---")
        print(f"La carpeta de trabajo es: {CARPETA_PROYECTO}")
        print("1. Redimensionar video a 1366x768")
        print("2. Comprimir video (bitrate 1M)")
        print("3. Extraer solo el audio (a MP3)")
        print("4. Salir")
        
        choice = input("Elige una opción (1-4): ")
        
        if choice == '4':
            print("👋 Saliendo del programa...")
            break

        input_file_path, input_filename = get_input_file_path()
        filename, file_extension = os.path.splitext(input_filename)
        
        if choice == '1':
            output_file_name = f"{filename}_redimensionado.mp4"
            output_file_path = os.path.join(CARPETA_PROYECTO, output_file_name)
            command = [
                'ffmpeg', '-i', input_file_path, 
                '-vf', 'scale=1366:768', 
                '-y', output_file_path
            ]
            run_ffmpeg_command(command, output_file_path)

        elif choice == '2':
            output_file_name = f"{filename}_comprimido.mp4"
            output_file_path = os.path.join(CARPETA_PROYECTO, output_file_name)
            command = [
                'ffmpeg', '-i', input_file_path, 
                '-b:v', '1M',
                '-y', output_file_path
            ]
            run_ffmpeg_command(command, output_file_path)

        elif choice == '3':
            output_file_name = f"{filename}_audio.mp3"
            output_file_path = os.path.join(CARPETA_PROYECTO, output_file_name)
            command = [
                'ffmpeg', '-i', input_file_path, 
                '-q:a', '0', '-map', 'a', 
                '-y', output_file_path
            ]
            run_ffmpeg_command(command, output_file_path)

        else:
            print("⚠️ Opción no válida. Por favor, elige un número del 1 al 4.")

if __name__ == "__main__":
    main_menu()
