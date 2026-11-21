ProyectoJuego — Dardos 301
Juego inicial de dardos en Python 3 con modo local y modo multijugador en red LAN. El servidor conserva el estado oficial de la partida; el cliente envía las jugadas del Jugador 2 y recibe el marcador actualizado.
Requisitos
Python 3.10 o posterior (usa anotaciones de tipos actuales).
En modo LAN, dos computadores/VM conectados a la misma red y un puerto TCP accesible (predeterminado: 5050).
No requiere paquetes externos: utiliza la biblioteca estándar de Python.
Ejecutar modo local
Bash
python3 juego.py
El modo local admite dos participantes en la misma terminal. Introduce la puntuación de cada dardo como entero entre 0 y 60.
Ejecutar modo LAN
En el computador del Jugador 1 (servidor), desde esta carpeta:
Bash
python3 server.py
Si se desea otro puerto, por ejemplo 6000: python3 server.py 6000.
Obtén la IP LAN del servidor y permite el puerto TCP en el firewall de la red privada. En el computador del Jugador 2 (cliente):
Bash
python3 client.py IP_DEL_SERVIDOR
Ejemplo: python3 client.py 192.168.1.25. Para un puerto alternativo: python3 client.py 192.168.1.25 6000. Inicia primero el servidor. No expongas el puerto a Internet; este prototipo no implementa autenticación ni cifrado.
Componentes
juego.py: interfaz de terminal y ciclo de partida local.
game_logic.py: reglas y modelo común de la partida.
server.py: servidor TCP, validación y estado autoritativo.
client.py: cliente TCP del segundo jugador.
diagrama_arquitectura.mmd: diagrama Mermaid del flujo.
LICENSE: licencia MIT.
Reglas iniciales
Cada jugador comienza con 301 puntos y dispone de hasta tres dardos por turno. Se gana al llegar exactamente a cero. Si el puntaje cae por debajo de cero o queda en uno, el tiro produce bust, se conserva el puntaje anterior al turno y el turno pasa al rival. Los puntos de cada tiro se introducen directamente; dibujar una diana y convertir coordenadas en puntuación queda fuera del alcance de este primer prototipo.
Protocolo de comunicación
Los mensajes son objetos JSON codificados en UTF-8 y terminados con salto de línea (\n). TCP es un flujo de bytes, por lo que el delimitador permite separar mensajes.
Cliente a servidor: {"tipo":"jugada","puntos":20}
Servidor a cliente: {"tipo":"estado","state":{...}}
Error: {"tipo":"error","mensaje":"...","state":{...}}
El servidor aplica las reglas y manda el estado completo. El cliente no altera directamente el marcador.
Pruebas rápidas
Bash
python3 -m py_compile juego.py game_logic.py server.py client.py
Para probar LAN, ejecuta servidor y cliente en dos terminales/máquinas distintas, inicia una partida, completa varios turnos y comprueba que ambos ven los mismos puntos. Prueba también una desconexión cerrando el cliente. La conexión entre VM requiere que su modo de red permita comunicación entre ellas (por ejemplo, red puente o una LAN configurada) y que el firewall permita el puerto.
Licencia
Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo LICENSE.
Declaración de autoría y créditos
El código original del proyecto fue preparado con asistencia de IA generativa (OpenAI/Manus) a petición del equipo/usuario. Debe revisarse, comprenderse, probarse y adaptarse por los integrantes antes de presentarlo como trabajo del equipo.
No se incorporaron fragmentos de código de terceros ni recursos visuales, sonoros o fuentes externas en esta versión inicial.
Se utiliza únicamente la biblioteca estándar incluida con Python; Python se distribuye bajo su propia licencia, descrita en https://docs.python.org/3/license.html.
Integrantes responsables de revisión, modificación y entrega: [completar nombres y aportes reales].
La asistencia de IA no sustituye la declaración individual de contribuciones del equipo ni las políticas académicas aplicables.
Bitácora de gestión de conflictos
La bitácora debe registrar un evento que haya ocurrido realmente. No se reportó un incidente real al preparar este esqueleto, así que no se atribuye al equipo un conflicto ficticio. Para completar el entregable, registren fecha, personas/roles, evidencia y resultado usando la plantilla BITACORA_CONFLICTOS.md. Si el equipo desea documentar un riesgo hipotético, identifíquenlo expresamente como simulación, no como incidente ocurrido.
