# Ingestión de datos - Reporte de clusteres

# Construya un dataframe de Pandas a partir del archivo 'clusters_report.txt', teniendo en
# cuenta que los nombres de las columnas deben ser en minusculas, reemplazando los espacios
# por guiones bajos; y que las palabras clave deben estar separadas por coma y con un solo 
# espacio entre palabra y palabra.

import pandas as pd
import re

def ingest_data():

  with open('clusters_report.txt') as report:
    filas = report.readlines()

  # No me sirven las 4 primeras filas del txt
  filas = filas[4:]

  # Hacer una lista con los datos de cada cluster
  clusters = []
  cluster = [0, 0, 0, '']

  for fila in filas:
    # Es la primera fila, por tanto tiene numero del cluster,
    # cantidad de palabras clave, porcentaje de palabras clave
    # y algunas palabras clave
    if re.match('^ +[0-9]+ +', fila):
      numero, cantidad, porcentaje, *palabras = fila.split()
      
      # Importante convertirlos al tipo de dato correcto
      cluster[0] = int(numero)
      cluster[1] = int(cantidad)
      cluster[2] = float(porcentaje.replace(',','.')) # Se cambia el separador decimal

      # Se guardan las palabras clave de esta linea
      palabras.pop(0) # Se elimina el carácter '%'
      palabras = ' '.join(palabras)
      cluster[3] += palabras

    # Son las filas de un cluster que solo tienen palabras clave
    elif re.match('^ +[a-z]', fila):
      palabras = fila.split()
      palabras = ' '.join(palabras)
      cluster[3] += ' ' + palabras

    # Se llegó a un separador entre clusters, se guarda el cluster
    # anterior y se re-inicializa la lista para el siguiente
    elif re.match('^\n', fila) or re.match('^ +$', fila):
      cluster[3] = cluster[3].replace('.', '') # Se elimina el punto final
      clusters.append(cluster)
      cluster = [0, 0, 0, '']

  df = pd.DataFrame (clusters, columns = ['cluster', 'cantidad_de_palabras_clave', 'porcentaje_de_palabras_clave', 'principales_palabras_clave'])
  return df
