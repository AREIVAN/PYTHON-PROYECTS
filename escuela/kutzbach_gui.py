import tkinter as tk
from tkinter import ttk, messagebox
from kutzbach import MecanismoKutzbach


class KutzbachGUI:
    """Interfaz gráfica para el calculador de Kutzbach"""

    def __init__(self, root):
        self.root = root
        self.root.title("Calculador de Kutzbach - Grados de Libertad")
        self.root.geometry("900x1000")
        self.root.resizable(True, True)

        # Variable para almacenar pares ingresados
        self.pares_ingresados = {}
        self.mecanismo = None

        self.crear_interfaz()

    def crear_interfaz(self):
        """Construye la interfaz gráfica"""
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')

        # Frame principal con scrollbar
        main_canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(
            self.root, orient="vertical", command=main_canvas.yview)
        scrollable_frame = ttk.Frame(main_canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(
                scrollregion=main_canvas.bbox("all"))
        )

        main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)

        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        main_frame = scrollable_frame

        # ===== TÍTULO =====
        titulo = ttk.Label(
            main_frame,
            text="📊 CALCULADOR DE KUTZBACH",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=(15, 20), padx=20)

        # ===== SECCIÓN 1: DIMENSIÓN =====
        dim_frame = ttk.LabelFrame(
            main_frame, text="1. Tipo de Mecanismo", padding="12")
        dim_frame.pack(fill=tk.X, pady=10, padx=20)

        self.dimension_var = tk.StringVar(value="2D")
        ttk.Radiobutton(
            dim_frame,
            text="Mecanismo 2D (Planar)",
            variable=self.dimension_var,
            value="2D"
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            dim_frame,
            text="Mecanismo 3D (Espacial)",
            variable=self.dimension_var,
            value="3D"
        ).pack(anchor=tk.W)

        # ===== SECCIÓN 2: ESLABONES =====
        eslab_frame = ttk.LabelFrame(
            main_frame, text="2. Número de Eslabones", padding="12")
        eslab_frame.pack(fill=tk.X, pady=10, padx=20)

        ttk.Label(eslab_frame, text="Cantidad de eslabones:").pack(
            side=tk.LEFT, padx=5)
        self.eslabones_var = tk.IntVar(value=4)
        eslab_spinbox = ttk.Spinbox(
            eslab_frame,
            from_=1,
            to=20,
            textvariable=self.eslabones_var,
            width=10
        )
        eslab_spinbox.pack(side=tk.LEFT, padx=5)

        # ===== SECCIÓN 3: PARES CINEMÁTICOS =====
        pares_frame = ttk.LabelFrame(
            main_frame, text="3. Pares Cinemáticos", padding="12")
        pares_frame.pack(fill=tk.X, pady=10, padx=20)

        # Frame para entrada de pares
        entrada_frame = ttk.Frame(pares_frame)
        entrada_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(entrada_frame, text="Tipo:").pack(side=tk.LEFT, padx=5)
        self.tipo_var = tk.IntVar(value=1)
        tipo_spinbox = ttk.Spinbox(
            entrada_frame,
            from_=1,
            to=5,
            textvariable=self.tipo_var,
            width=5
        )
        tipo_spinbox.pack(side=tk.LEFT, padx=5)

        ttk.Label(entrada_frame, text="Cantidad:").pack(side=tk.LEFT, padx=5)
        self.cantidad_var = tk.IntVar(value=1)
        cantidad_spinbox = ttk.Spinbox(
            entrada_frame,
            from_=1,
            to=50,
            textvariable=self.cantidad_var,
            width=5
        )
        cantidad_spinbox.pack(side=tk.LEFT, padx=5)

        agregar_btn = ttk.Button(
            entrada_frame,
            text="➕ Agregar Par",
            command=self.agregar_par
        )
        agregar_btn.pack(side=tk.LEFT, padx=5)

        # Frame para mostrar pares ingresados
        self.pares_text = tk.Text(pares_frame, height=7, width=80)
        self.pares_text.pack(fill=tk.BOTH, pady=10)
        self.pares_text.config(state=tk.DISABLED, font=(
            "Arial", 10), bg="#1e1e1e", fg="#ffffff")

        # Botón para limpiar pares
        limpiar_btn = ttk.Button(
            pares_frame,
            text="🗑️  Limpiar Pares",
            command=self.limpiar_pares
        )
        limpiar_btn.pack()

        # ===== SECCIÓN 4: INFORMACIÓN =====
        info_frame = ttk.LabelFrame(
            main_frame, text="📚 Información Útil", padding="12")
        info_frame.pack(fill=tk.X, pady=10, padx=20)

        info_text = tk.Text(info_frame, height=8, width=80)
        info_text.pack(fill=tk.BOTH)

        info_content = """TIPOS DE PARES (2D):
  • Tipo 1: REVOLUCIÓN (bisagra) → 1 grado de libertad
  • Tipo 2: PRISMÁTICO (deslizador) → 1 grado de libertad

TIPOS DE PARES (3D):
  • Tipo 1: REVOLUCIÓN → 1 DOF
  • Tipo 2: CILÍNDRICA → 2 DOF
  • Tipo 3: ESFÉRICA → 3 DOF
  • Tipo 4: TORNILLO → 4 DOF
  • Tipo 5: PLANAR → 5 DOF"""

        info_text.insert(tk.END, info_content)
        info_text.config(state=tk.DISABLED, font=("Arial", 9))

        # ===== SECCIÓN 5: BOTONES DE ACCIÓN =====
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=20, padx=20)

        calcular_btn = ttk.Button(
            btn_frame,
            text="🧮 CALCULAR",
            command=self.calcular
        )
        calcular_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        limpiar_todo_btn = ttk.Button(
            btn_frame,
            text="🔄 Limpiar Todo",
            command=self.limpiar_todo
        )
        limpiar_todo_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # ===== SECCIÓN 6: RESULTADOS =====
        resultado_frame = ttk.LabelFrame(
            main_frame, text="📊 Resultados", padding="15")
        resultado_frame.pack(fill=tk.BOTH, expand=True, pady=15, padx=20)

        self.resultado_text = tk.Text(
            resultado_frame, height=20, width=80, wrap=tk.WORD, font=("Courier", 11))
        self.resultado_text.pack(fill=tk.BOTH, expand=True)
        self.resultado_text.config(
            state=tk.DISABLED, bg="#1e1e1e", fg="#ffffff")

    def agregar_par(self):
        """Agrega un par cinemático a la lista"""
        try:
            tipo = self.tipo_var.get()
            cantidad = self.cantidad_var.get()

            if tipo < 1 or tipo > 5:
                messagebox.showerror("Error", "El tipo debe estar entre 1 y 5")
                return

            if cantidad < 1:
                messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                return

            self.pares_ingresados[tipo] = self.pares_ingresados.get(
                tipo, 0) + cantidad
            self.actualizar_lista_pares()
            messagebox.showinfo(
                "✓ Éxito", f"Par tipo {tipo} con cantidad {cantidad} agregado")

        except tk.TclError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos")

    def actualizar_lista_pares(self):
        """Actualiza la visualización de pares ingresados"""
        self.pares_text.config(state=tk.NORMAL)
        self.pares_text.delete(1.0, tk.END)

        if not self.pares_ingresados:
            self.pares_text.insert(tk.END, "No hay pares ingresados aún...")
        else:
            self.pares_text.insert(tk.END, "PARES INGRESADOS:\n\n")
            total = 0
            for tipo in sorted(self.pares_ingresados.keys()):
                cantidad = self.pares_ingresados[tipo]
                self.pares_text.insert(
                    tk.END, f"  • Tipo {tipo}: {cantidad} pares\n")
                total += cantidad
            self.pares_text.insert(
                tk.END, f"\nTOTAL: {total} pares cinemáticos")

        self.pares_text.config(state=tk.DISABLED)

    def limpiar_pares(self):
        """Limpia los pares ingresados"""
        self.pares_ingresados = {}
        self.actualizar_lista_pares()

    def limpiar_todo(self):
        """Limpia toda la interfaz"""
        self.eslabones_var.set(4)
        self.dimension_var.set("2D")
        self.tipo_var.set(1)
        self.cantidad_var.set(1)
        self.pares_ingresados = {}
        self.actualizar_lista_pares()

        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.config(state=tk.DISABLED)

    def calcular(self):
        """Realiza el cálculo de grados de libertad"""
        try:
            if not self.pares_ingresados:
                messagebox.showwarning(
                    "Advertencia", "Debe ingresar al menos un par cinemático")
                return

            # Crear mecanismo
            dimension = self.dimension_var.get()
            eslabones = self.eslabones_var.get()

            self.mecanismo = MecanismoKutzbach(dimension)
            self.mecanismo.establecer_eslabones(eslabones)

            for tipo, cantidad in self.pares_ingresados.items():
                self.mecanismo.agregar_pares(tipo, cantidad)

            # Calcular
            M = self.mecanismo.calcular()

            # Mostrar resultados
            self.mostrar_resultados(M)

        except Exception as e:
            messagebox.showerror("Error en el cálculo", str(e))

    def mostrar_resultados(self, M):
        """Muestra los resultados en la ventana de resultados"""
        self.resultado_text.config(state=tk.NORMAL)
        self.resultado_text.delete(1.0, tk.END)

        try:
            # Construir texto de resultados
            resultado = "=" * 55 + "\n"
            resultado += "ANÁLISIS DE MECANISMO - CRITERIO DE KUTZBACH\n"
            resultado += "=" * 55 + "\n\n"
            resultado += f"Dimensión: {self.mecanismo.dimension}\n"
            resultado += f"Número de eslabones (n): {self.mecanismo.eslabones}\n\n"
            resultado += "Pares cinemáticos:\n"

            if self.mecanismo.pares_cineticos:
                for tipo in sorted(self.mecanismo.pares_cineticos.keys()):
                    cantidad = self.mecanismo.pares_cineticos[tipo]
                    resultado += f"  • Tipo {tipo} (j{tipo}): {cantidad} pares\n"
            else:
                resultado += "  (No hay pares registrados)\n"

            resultado += f"\n{'=' * 55}\n"
            resultado += f"GRADOS DE LIBERTAD (M): {M}\n"
            resultado += f"{'=' * 55}\n\n"

            # Clasificación del mecanismo
            if M < 0:
                resultado += "⚠️  MECANISMO INDETERMINADO\n"
                resultado += "    (Estructura redundante - sobredeterminada)\n"
            elif M == 0:
                resultado += "✓ MECANISMO DETERMINADO\n"
                resultado += "    (Estructura rígida - sin movilidad)\n"
            elif M == 1:
                resultado += "✓ MECANISMO DESMODRÓMICO\n"
                resultado += "    (1 grado de libertad - movimiento controlado)\n"
            else:
                resultado += f"✓ MECANISMO CON MOVILIDAD\n"
                resultado += f"    ({M} grados de libertad)\n"

            self.resultado_text.insert(tk.END, resultado)
        except Exception as e:
            self.resultado_text.insert(
                tk.END, f"Error al mostrar resultados: {str(e)}")
        finally:
            self.resultado_text.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = KutzbachGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
