import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import threading
from pathlib import Path
import os
import sys


def abrir_archivo(path: Path):
    """Abre un archivo con la app por defecto (Windows/Mac/Linux)."""
    try:
        if sys.platform.startswith("win"):
            os.startfile(str(path))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=False)
        else:
            subprocess.run(["xdg-open", str(path)], check=False)
    except Exception as exc:
        messagebox.showerror("Error", f"No se pudo abrir el archivo.\n{exc}")


def abrir_carpeta(path: Path):
    """Abre la carpeta que contiene el archivo."""
    folder = path.parent
    try:
        if sys.platform.startswith("win"):
            os.startfile(str(folder))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", str(folder)], check=False)
        else:
            subprocess.run(["xdg-open", str(folder)], check=False)
    except Exception as exc:
        messagebox.showerror("Error", f"No se pudo abrir la carpeta.\n{exc}")


def procesar_video(video_path: str, ventana: tk.Tk):
    input_p = Path(video_path)
    output_path = input_p.with_name(input_p.stem + "_processed.mp4")

    # UI refs
    progress_bar = ventana._progress_bar
    boton_seleccionar = ventana._boton_seleccionar
    boton_abrir = ventana._boton_abrir
    boton_carpeta = ventana._boton_carpeta
    salida_var = ventana._salida_var

    # Preparar UI
    boton_seleccionar.config(state="disabled")
    boton_abrir.config(state="disabled")
    boton_carpeta.config(state="disabled")
    salida_var.set(f"Procesando...\nSalida: {output_path.name}")

    progress_bar.configure(mode="indeterminate")
    progress_bar.start(12)

    def finish_ui():
        progress_bar.stop()
        progress_bar.configure(mode="determinate", value=0)
        boton_seleccionar.config(state="normal")

    def run_subprocess():
        try:
            subprocess.run(
                ["python3", "pruebavideo.py", "--input",
                    str(input_p), "--output", str(output_path)],
                check=True,
            )

            # Guardar última salida y habilitar botones (en hilo principal)
            def on_success():
                ventana._last_output_path = output_path
                salida_var.set(f"Listo.\nSalida: {output_path}")
                boton_abrir.config(state="normal")
                boton_carpeta.config(state="normal")
                messagebox.showinfo(
                    "Éxito", f"Video procesado.\nGuardado en:\n{output_path}")

            ventana.after(0, on_success)

        except subprocess.CalledProcessError as exc:
            ventana.after(0, lambda: messagebox.showerror(
                "Error", f"Error al procesar.\n{exc}"))
            ventana.after(0, lambda: salida_var.set(
                "Error al procesar. Revisa la consola/logs."))
        except Exception as exc:
            ventana.after(0, lambda: messagebox.showerror(
                "Error", f"Error inesperado.\n{exc}"))
            ventana.after(0, lambda: salida_var.set("Error inesperado."))
        finally:
            ventana.after(0, finish_ui)

    threading.Thread(target=run_subprocess, daemon=True).start()


def seleccionar_video(ventana: tk.Tk):
    video_path = filedialog.askopenfilename(
        title="Seleccionar video",
        filetypes=[("Archivos de video", "*.mp4 *.avi *.mov *.mkv")],
    )
    if video_path:
        procesar_video(video_path, ventana)


def main():
    ventana = tk.Tk()
    ventana.title("Procesador de Videos")
    ventana.geometry("520x320")
    ventana.resizable(False, False)

    ventana._last_output_path = None  # type: ignore[attr-defined]
    ventana._salida_var = tk.StringVar(
        value="Selecciona un video para procesar")  # type: ignore[attr-defined]

    etiqueta = tk.Label(
        ventana, text="Procesador de Videos", font=("Arial", 16))
    etiqueta.pack(pady=10)

    estado = tk.Label(ventana, textvariable=ventana._salida_var,
                      font=("Arial", 10), justify="left")
    estado.pack(pady=8)

    ventana._progress_bar = ttk.Progressbar(
        ventana, orient="horizontal", length=420, mode="determinate")  # type: ignore[attr-defined]
    ventana._progress_bar.pack(pady=10)

    frame_btns = tk.Frame(ventana)
    frame_btns.pack(pady=10)

    ventana._boton_seleccionar = tk.Button(  # type: ignore[attr-defined]
        frame_btns, text="Seleccionar Video", font=("Arial", 12), width=16,
        command=lambda: seleccionar_video(ventana)
    )
    ventana._boton_seleccionar.grid(row=0, column=0, padx=6)

    ventana._boton_abrir = tk.Button(  # type: ignore[attr-defined]
        frame_btns, text="Abrir resultado", font=("Arial", 12), width=16,
        state="disabled",
        command=lambda: abrir_archivo(
            ventana._last_output_path) if ventana._last_output_path else None
    )
    ventana._boton_abrir.grid(row=0, column=1, padx=6)

    ventana._boton_carpeta = tk.Button(  # type: ignore[attr-defined]
        frame_btns, text="Abrir carpeta", font=("Arial", 12), width=16,
        state="disabled",
        command=lambda: abrir_carpeta(
            ventana._last_output_path) if ventana._last_output_path else None
    )
    ventana._boton_carpeta.grid(row=0, column=2, padx=6)

    ventana.mainloop()


if __name__ == "__main__":
    main()
