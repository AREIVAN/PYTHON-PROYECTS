import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import threading
import time


def procesar_video(video_path, progress_bar, ventana):
    """Llama al script de procesamiento con el video seleccionado."""

    def run():
        try:
            output_path = "output_video.mp4"

            # Simula progreso mientras se ejecuta el procesamiento
            for i in range(1, 101):
                time.sleep(0.05)
                progress_bar["value"] = i
                ventana.update_idletasks()

            subprocess.run(
                ["python3", "pruebavideo.py", "--input",
                    video_path, "--output", output_path],
                check=True,
            )
            messagebox.showinfo(
                "Éxito", f"El video se procesó correctamente.\nGuardado en: {output_path}"
            )
        except subprocess.CalledProcessError as exc:
            messagebox.showerror(
                "Error", f"Hubo un error al procesar el video.\n{exc}"
            )
        except Exception as exc:
            messagebox.showerror(
                "Error", f"Ocurrió un error inesperado.\n{exc}")
        finally:
            progress_bar["value"] = 0

    hilo = threading.Thread(target=run, daemon=True)
    hilo.start()


def seleccionar_video(progress_bar, ventana):
    """Abre un cuadro de diálogo para seleccionar el archivo de video."""
    video_path = filedialog.askopenfilename(
        title="Seleccionar video",
        filetypes=[("Archivos de video", "*.mp4 *.avi *.mov *.mkv")],
    )
    if video_path:
        procesar_video(video_path, progress_bar, ventana)


def main():
    ventana = tk.Tk()
    ventana.title("Procesador de Videos")
    ventana.geometry("400x250")

    etiqueta = tk.Label(
        ventana, text="Selecciona un video para procesar", font=("Arial", 14)
    )
    etiqueta.pack(pady=20)

    progress_bar = ttk.Progressbar(
        ventana, orient="horizontal", length=300, mode="determinate"
    )
    progress_bar.pack(pady=20)

    boton_seleccionar = tk.Button(
        ventana,
        text="Seleccionar Video",
        command=lambda: seleccionar_video(progress_bar, ventana),
        font=("Arial", 12),
    )
    boton_seleccionar.pack(pady=10)

    ventana.mainloop()


if __name__ == "__main__":
    main()
