import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
from matplotlib.widgets import Button
import numpy as np

# Laura Arteta
# Juan Acosta
# Jorge Ortega 

# Definición de la casa
puntosCasa = np.array([
  [0.0, 0.0], # A
  [0.0, 5.0], # B
  [2.5, 7.5], # C TECHO
  [5.0, 5.0], # D
  [5.0, 0.0], # E
])

# --- Gráfica con TextBox ---
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)

# --- Ángulo ---
axboxRotar = plt.axes([0.2, 0.05, 0.6, 0.05])    
text_boxRotar = TextBox(axboxRotar, 'Rotar | Ángulo:', initial="0")

# --- Escala ---
axboxEscalar = plt.axes([0.2, 0.0, 0.6, 0.05])  
text_boxEscalar = TextBox(axboxEscalar, 'Escalar | Valor:', initial="1")

# --- Botón "Derecha" ---
ax_boton_derecha = plt.axes([0.7, 0.12, 0.2, 0.075])  # [x, y, width, height]
buttonDerecha = Button(ax_boton_derecha, "Derecha ➡️")

# --- Botón "Izquierda" ---
ax_boton_izquierda = plt.axes([0.1, 0.12, 0.2, 0.075]) # [x, y, width, height]
buttonIzquierda = Button(ax_boton_izquierda, "⬅️ Izquierda")

# --- Botón "Arriba" ---
ax_boton_arriba = plt.axes([0.5, 0.12, 0.2, 0.075])  # [x, y, width, height]
buttonArriba = Button(ax_boton_arriba, "Arriba ⬆️")

# --- Botón "Abajo" ---
ax_boton_abajo = plt.axes([0.3, 0.12, 0.2, 0.075]) # [x, y, width, height]
buttonAbajo = Button(ax_boton_abajo, "⬇️ Abajo")

def mostrar_casa(ax, puntos):
    ax.clear()
    closed = np.vstack([puntos, puntos[0]])
    ax.plot(closed[:, 0], closed[:, 1], marker='o')
    ax.set_aspect('equal', 'box')
    ax.set_xlim(-30, 30)
    ax.set_ylim(-30, 30)
    ax.set_title('Casa (5 puntos)')
    ax.grid(True)

def rotar_manual(puntos, angulo):
  theta = np.radians(angulo)
  cosTheta = np.cos(theta)
  sinTheta = np.sin(theta)

  cx, cy = puntos.mean(axis=0)

  nuevos_puntos = []
  for x, y in puntos:
      x -= cx
      y -= cy

      xPrima = x * cosTheta - y * sinTheta
      yPrima = x * sinTheta + y * cosTheta

      nuevos_puntos.append([xPrima + cx, yPrima + cy])

  return np.array(nuevos_puntos)

def teclaDerecha(event):
  global puntosCasa
  puntosCasa = puntosCasa + np.array([1.0, 0.0])
  mostrar_casa(ax, puntosCasa)
  plt.draw()

def teclaIzquierda(event):
  global puntosCasa
  puntosCasa = puntosCasa + np.array([-1.0, 0.0])
  mostrar_casa(ax, puntosCasa)
  plt.draw()

def teclaArriba(event):
  global puntosCasa
  puntosCasa = puntosCasa + np.array([0.0, 1.0])
  mostrar_casa(ax, puntosCasa)
  plt.draw()

def teclaAbajo(event):
  global puntosCasa
  puntosCasa = puntosCasa + np.array([0.0, -1.0])
  mostrar_casa(ax, puntosCasa)
  plt.draw()

# Eventos cuando se escribe un valor en el input
def aplicar_rotacion(theta):
  global puntosCasa
  try:
    angulo = float(theta)
    puntosCasa = rotar_manual(puntosCasa, angulo)
    mostrar_casa(ax, puntosCasa)
    plt.draw()
  except ValueError:
      print("Por favor ingresa un número válido.")

def escalar(valorEscalar):
  global puntosCasa
  try:
    sx, sy = float(valorEscalar), float(valorEscalar)

    matrizEscalar = np.array([
      [sx, 0],
      [0, sy]
    ])
    cx, cy = np.mean(puntosCasa[:,0]), np.mean(puntosCasa[:,1])

    puntos_centrados = puntosCasa - np.array([cx, cy])

    # Escalar
    puntos_escalados = puntos_centrados.dot(matrizEscalar.T)

    puntos_finales = puntos_escalados + np.array([cx, cy])

    return puntos_finales
  except ValueError:
      print("Por favor ingresa un número válido.")

def aplicar_escalar(numEscalar):
  global puntosCasa
  try:
    valor = float(numEscalar)
    puntos = escalar(valor)
    mostrar_casa(ax, puntos)
    plt.draw()
  except ValueError:
    print("Por favor ingresa un número válido.")


mostrar_casa(ax, puntosCasa)

buttonDerecha.on_clicked(teclaDerecha)
buttonIzquierda.on_clicked(teclaIzquierda)
buttonAbajo.on_clicked(teclaAbajo)
buttonArriba.on_clicked(teclaArriba)

text_boxEscalar.on_submit(aplicar_escalar)
text_boxRotar.on_submit(aplicar_rotacion)
plt.show()
