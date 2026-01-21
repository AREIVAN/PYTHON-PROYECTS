"""
Programa para resolver problemas del Criterio de Kutzbach
Calcula los grados de libertad (DOF) de un mecanismo
"""


class MecanismoKutzbach:
    """
    Clase para calcular grados de libertad usando el criterio de Kutzbach

    Fórmula 2D (planar):
    M = 3(n - 1) - 2j1 - j2

    Fórmula 3D (espacial):
    M = 6(n - 1) - 5j1 - 4j2 - 3j3 - 2j4 - j5

    Donde:
    - M = grados de libertad
    - n = número de eslabones
    - j1, j2, ... = pares cinemáticos por tipo
    """

    def __init__(self, dimension="2D"):
        """
        Inicializa el mecanismo
        dimension: "2D" para planar o "3D" para espacial
        """
        self.dimension = dimension
        self.eslabones = 0
        self.pares_cineticos = {}

    def establecer_eslabones(self, n):
        """Establece el número de eslabones"""
        if n < 1:
            raise ValueError("El número de eslabones debe ser al menos 1")
        self.eslabones = n

    def agregar_pares(self, tipo, cantidad):
        """
        Agrega pares cinemáticos
        tipo: número de grados de libertad del par (1, 2, 3, 4, 5)
        cantidad: cantidad de pares de ese tipo
        """
        if tipo < 1 or tipo > 5:
            raise ValueError("El tipo de par debe estar entre 1 y 5")
        self.pares_cineticos[tipo] = cantidad

    def calcular_grados_libertad_2D(self):
        """Calcula DOF para mecanismo planar (2D)"""
        if self.eslabones == 0:
            raise ValueError("Debe establecer el número de eslabones")

        j1 = self.pares_cineticos.get(1, 0)
        j2 = self.pares_cineticos.get(2, 0)

        M = 3 * (self.eslabones - 1) - 2 * j1 - j2
        return M

    def calcular_grados_libertad_3D(self):
        """Calcula DOF para mecanismo espacial (3D)"""
        if self.eslabones == 0:
            raise ValueError("Debe establecer el número de eslabones")

        j1 = self.pares_cineticos.get(1, 0)
        j2 = self.pares_cineticos.get(2, 0)
        j3 = self.pares_cineticos.get(3, 0)
        j4 = self.pares_cineticos.get(4, 0)
        j5 = self.pares_cineticos.get(5, 0)

        M = 6 * (self.eslabones - 1) - 5 * j1 - 4 * j2 - 3 * j3 - 2 * j4 - j5
        return M

    def calcular(self):
        """Calcula los grados de libertad según la dimensión"""
        if self.dimension == "2D":
            return self.calcular_grados_libertad_2D()
        elif self.dimension == "3D":
            return self.calcular_grados_libertad_3D()
        else:
            raise ValueError("Dimensión debe ser '2D' o '3D'")

    def mostrar_resultados(self):
        """Muestra un resumen del cálculo"""
        print("\n" + "="*50)
        print("ANÁLISIS DE MECANISMO - CRITERIO DE KUTZBACH")
        print("="*50)
        print(f"Dimensión: {self.dimension}")
        print(f"Número de eslabones (n): {self.eslabones}")
        print(f"\nPares cinemáticos:")
        for tipo in sorted(self.pares_cineticos.keys()):
            print(f"  Tipo {tipo} (j{tipo}): {self.pares_cineticos[tipo]}")

        M = self.calcular()
        print(f"\nGrados de libertad (M): {M}")

        if M < 0:
            print("⚠️  Mecanismo INDETERMINADO (estructura redundante)")
        elif M == 0:
            print("✓ Mecanismo DETERMINADO (estructura rígida)")
        elif M == 1:
            print("✓ Mecanismo DESMODRÓMICO (1 grado de libertad)")
        else:
            print(f"✓ Mecanismo con {M} grados de libertad")
        print("="*50 + "\n")

        return M


def resolver_problema(problema):
    """
    Resuelve un problema específico de Kutzbach
    problema: diccionario con los parámetros
    """
    mec = MecanismoKutzbach(problema.get("dimension", "2D"))
    mec.establecer_eslabones(problema["eslabones"])

    for tipo, cantidad in problema.get("pares", {}).items():
        mec.agregar_pares(tipo, cantidad)

    return mec


# ============= EJEMPLOS DE USO =============

if __name__ == "__main__":

    # EJEMPLO 1: Mecanismo de 4 barras (planar)
    print("\n📋 EJEMPLO 1: Mecanismo de 4 barras")
    problema1 = {
        "dimension": "2D",
        "eslabones": 4,
        "pares": {
            1: 4  # 4 pares de revolución (1 DOF cada uno)
        }
    }
    mec1 = resolver_problema(problema1)
    mec1.mostrar_resultados()

    # EJEMPLO 2: Mecanismo de 5 barras (planar)
    print("📋 EJEMPLO 2: Mecanismo de 5 barras")
    problema2 = {
        "dimension": "2D",
        "eslabones": 5,
        "pares": {
            1: 5  # 5 pares de revolución
        }
    }
    mec2 = resolver_problema(problema2)
    mec2.mostrar_resultados()

    # EJEMPLO 3: Mecanismo con pares de diferente tipo
    print("📋 EJEMPLO 3: Mecanismo mixto")
    problema3 = {
        "dimension": "2D",
        "eslabones": 6,
        "pares": {
            1: 4,  # 4 pares de revolución
            2: 2   # 2 pares de deslizamiento
        }
    }
    mec3 = resolver_problema(problema3)
    mec3.mostrar_resultados()

    # EJEMPLO 4: Mecanismo 3D
    print("📋 EJEMPLO 4: Mecanismo espacial (3D)")
    problema4 = {
        "dimension": "3D",
        "eslabones": 5,
        "pares": {
            1: 3,  # 3 pares cinemáticos de 1 DOF
            2: 2   # 2 pares cinemáticos de 2 DOF
        }
    }
    mec4 = resolver_problema(problema4)
    mec4.mostrar_resultados()

    # ============= INTERFAZ INTERACTIVA =============
    print("\n🎯 MODO INTERACTIVO - CALCULADORA DE KUTZBACH")
    print("=" * 60)
    print("\n📚 INFORMACIÓN ÚTIL:")
    print("-" * 60)
    print("\n¿QUÉ ES UN ESLABÓN?")
    print("  → Es cada pieza/barra del mecanismo")
    print("  → Ejemplo: en un mecanismo de 4 barras hay 4 eslabones\n")

    print("¿QUÉ ES UN PAR CINEMÁTICO?")
    print("  → Es la conexión/unión entre dos eslabones\n")

    print("TIPOS DE PARES (según grados de libertad que permite):\n")
    print("  Para MECANISMOS 2D (Planar):")
    print("    Tipo 1: REVOLUCIÓN (bisagra)          → Permite 1 rotación")
    print("    Tipo 2: PRISMÁTICO (deslizador)       → Permite 1 traslación\n")
    print("  Para MECANISMOS 3D (Espacial):")
    print("    Tipo 1: REVOLUCIÓN                    → 1 DOF (rotación)")
    print("    Tipo 2: CILÍNDRICA                    → 2 DOF (rotación+traslación)")
    print("    Tipo 3: ESFÉRICA                      → 3 DOF (3 rotaciones)")
    print("    Tipo 4: TORNILLO                      → 4 DOF")
    print("    Tipo 5: PLANAR                        → 5 DOF\n")

    print("EJEMPLO DE MECANISMO DE 4 BARRAS:")
    print("    🔵━━━━━━🔵")
    print("    ⟳      ⟳")
    print("    ⟳      ⟳")
    print("    🔵━━━━━━🔵")
    print("  • Número de eslabones: 4")
    print("  • Pares cinemáticos: 4 articulaciones de tipo 1")
    print("  • Ingresarías: Tipo=1, Cantidad=4\n")

    print("=" * 60)

    try:
        # Solicitar datos del usuario
        print("\n📝 INGRESE LOS DATOS DE SU MECANISMO:\n")

        dim = input("1️⃣  ¿Es mecanismo 2D o 3D? (2D/3D): ").upper()
        if dim not in ["2D", "3D"]:
            dim = "2D"
            print(f"   ✓ Se asumirá: {dim}")

        n = int(input("\n2️⃣  ¿Cuántos ESLABONES tiene el mecanismo? (número): "))

        print("\n3️⃣  INGRESE LOS PARES CINEMÁTICOS:")
        print("   (Ud. irá indicando cada TIPO y su CANTIDAD)\n")
        print("   ⚠️  ACLARACIÓN:")
        print("   Si tiene 6 pares de diferentes tipos, lo hará así:\n")
        print("      • Primero ingresa: Tipo 1 → Cantidad 4")
        print("      • Luego ingresa:   Tipo 2 → Cantidad 2")
        print("      • TOTAL: 4+2 = 6 pares cinemáticos ✓\n")
        print("   El programa sumará automáticamente.\n")

        mec = MecanismoKutzbach(dim)
        mec.establecer_eslabones(n)

        continuar = True
        contador = 1
        pares_ingresados = {}

        while continuar:
            try:
                print(f"\n   INGRESO #{contador}:")
                tipo = int(
                    input("   → ¿De qué TIPO son estos pares? (1-5, ó 0 para terminar): "))

                if tipo == 0:
                    continuar = False
                    print("\n   ✓ Cálculo completado\n")
                    print("   📊 RESUMEN DE PARES INGRESADOS:")
                    total_pares = 0
                    for t in sorted(pares_ingresados.keys()):
                        print(f"      • Tipo {t}: {pares_ingresados[t]} pares")
                        total_pares += pares_ingresados[t]
                    print(f"      TOTAL: {total_pares} pares\n")

                elif 1 <= tipo <= 5:
                    cantidad = int(
                        input(f"   → ¿Cuántos pares de TIPO {tipo}? (cantidad): "))
                    if cantidad > 0:
                        mec.agregar_pares(tipo, cantidad)
                        pares_ingresados[tipo] = cantidad
                        print(f"   ✓ Agregados {cantidad} pares tipo {tipo}")
                        contador += 1
                    else:
                        print("   ❌ La cantidad debe ser mayor a 0")
                else:
                    print("   ❌ El tipo debe estar entre 1 y 5")

            except ValueError:
                print("   ❌ Entrada inválida. Ingrese números enteros.")

        print("\n" + "=" * 60)
        mec.mostrar_resultados()

    except ValueError as e:
        print(f"❌ Error en la entrada: {e}")
        print("   Asegúrese de ingresar números válidos")
    except Exception as e:
        print(f"❌ Error: {e}")
