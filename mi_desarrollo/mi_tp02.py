# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Nombre y apellido:  Jonathan Gamboa
#  Comision:           582477
# =====================================================================

from robot import ErrorDeSeguridad, Robot

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO


# #####################################################################
#  >>> INSTRUCCIONES PARA EL ROBOT <<<
# #####################################################################
MI_MISION = [

    # 1) Avanzar 3 metros
    ("avanzar", 0.2, 5.0),
    ("avanzar", 0.2, 5.0),
    ("avanzar", 0.2, 5.0),

    # 2) Girar 180 grados para quedar mirandote
    ("girar", 0.5, 6.2832),

    # 3) Saludar de frente
    ("saludar",),

    # 4) Girar -90 grados, hacia la derecha
    ("girar", -0.5, 3.1416),

    # 5) Avanzar 1 metro hacia el costado
    ("avanzar", 0.2, 5.0),

    # 6) Girar +90 grados, hacia la izquierda, para volver a mirarte
    ("girar", 0.5, 3.1416),

    # 7) Volver avanzando 3 metros
    ("avanzar", 0.2, 5.0),
    ("avanzar", 0.2, 5.0),
    ("avanzar", 0.2, 5.0),

    ("detenerse",),
]

# Que mision ejecutar: MI_MISION, MISION_BASICA, MISION_CUADRADO
# o MISION_CON_ERRORES
MISION_A_EJECUTAR = MI_MISION
# #####################################################################


COMANDOS_CON_DATOS = ("avanzar", "girar")
COMANDOS_SIN_DATOS = ("detenerse", "saludar")


def es_numero(valor):
    """True si es int o float (bool no cuenta como numero)."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def motivo_invalido(comando):
    """Devuelve el motivo por el que el comando es invalido, o None si esta bien."""
    if not isinstance(comando, tuple) or len(comando) == 0:
        return "comando vacio o mal formado"

    nombre = comando[0]

    if nombre in COMANDOS_SIN_DATOS:
        if len(comando) != 1:
            return f"'{nombre}' no lleva datos"
        return None

    if nombre in COMANDOS_CON_DATOS:
        if len(comando) != 3:
            return f"'{nombre}' necesita velocidad y tiempo"
        velocidad, tiempo = comando[1], comando[2]
        if not es_numero(velocidad):
            return f"la velocidad debe ser un numero (llego {velocidad!r})"
        if not es_numero(tiempo):
            return f"el tiempo debe ser un numero (llego {tiempo!r})"
        if tiempo < 0:
            return "el tiempo no puede ser negativo"
        return None

    return f"el comando '{nombre}' no existe"


# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comando_es_valido(comando):
    return motivo_invalido(comando) is None


# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    nombre = comando[0]
    try:
        if nombre == "avanzar":
            robot.avanzar(velocidad=comando[1], tiempo=comando[2])
        elif nombre == "girar":
            robot.girar(velocidad=comando[1], tiempo=comando[2])
        elif nombre == "detenerse":
            robot.detenerse()
        elif nombre == "saludar":
            robot.saludar()
        return f"OK: {comando}"
    except ErrorDeSeguridad as error:
        return f"ERROR DE SEGURIDAD: {error}"


# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================
def ejecutar_mision(robot, mision, historial):
    for numero, comando in enumerate(mision, start=1):
        motivo = motivo_invalido(comando)

        if motivo is not None:
            print(f"[{numero}] RECHAZADO {comando} -> {motivo}")
            historial.append({"numero": numero, "comando": comando,
                              "ok": False, "motivo": motivo})
            continue

        resultado = ejecutar_comando(robot, comando)
        ok = resultado.startswith("OK")
        print(f"[{numero}] {resultado}")
        historial.append({"numero": numero, "comando": comando, "ok": ok,
                          "motivo": None if ok else resultado})


# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    ejecutados = [h for h in historial if h["ok"]]
    rechazados = [h for h in historial if not h["ok"]]

    print()
    print("=" * 50)
    print("  REPORTE DE LA MISION")
    print("=" * 50)
    print(f"  Comandos totales:    {len(historial)}")
    print(f"  Ejecutados bien:     {len(ejecutados)}")
    print(f"  Rechazados:          {len(rechazados)}")

    if rechazados:
        print()
        print("  Motivos de rechazo:")
        for h in rechazados:
            print(f"   - #{h['numero']} {h['comando']}: {h['motivo']}")
    print("=" * 50)


# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    robot = Robot()
    robot.conectar()

    historial = []

    try:
        ejecutar_mision(robot, MISION_A_EJECUTAR, historial)
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()
