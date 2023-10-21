import requests
from bs4 import BeautifulSoup
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Descargar el recurso 'punkt' de NLTK sin mostrar mensajes de descarga
nltk.download('punkt', quiet=True)

# Función para buscar y resumir información
def buscar_y_resumir_informacion():
    busqueda = input("¿Qué deseas buscar? ").strip()
    resultados = buscar_en_la_web(busqueda, num_resultados=5)
    
    if resultados:
        for i, resultado in enumerate(resultados, start=1):
            titulo, url, contenido = resultado
            print(f"Resultado {i}:")
            print(f"Título: {titulo}")
            print(f"URL: {url}")
            
            # Resumir el contenido de manera más breve
            parser = PlaintextParser.from_string(contenido, Tokenizer("english"))
            summarizer = LsaSummarizer()
            summary = summarizer(parser.document, 1)  # Resumir a 1 oración

            for sentence in summary:
                print(f"Resumen: {sentence}\n")

        opcion_ver = input("¿Desea ver uno de los resultados completos en pantalla? (Si­/No): ").strip().lower()
        if opcion_ver == "si" or opcion_ver == "sí­":
            num_resultado = int(input("Elija el número del resultado que desea ver (1-5): ").strip())
            if 1 <= num_resultado <= 5:
                titulo, url, contenido = resultados[num_resultado - 1]
                print(f"Resultado {num_resultado} - Tí­tulo: {titulo}")
                print(f"URL: {url}")
                print("Contenido completo:")
                print(contenido)

        guardar_resultados(resultados)
    else:
        print("No se encontraron resultados para la búsqueda.")

# Función para buscar en la web
def buscar_en_la_web(query, num_resultados=5):
    resultados = []
    try:
        # Realizar una búsqueda en Google
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            enlaces = soup.find_all('a')
            for enlace in enlaces:
                href = enlace.get('href')
                if href.startswith("/url?q="):
                    titulo = enlace.text
                    url = href[7:].split('&')[0]
                    contenido = extraer_contenido(url)
                    resultados.append((titulo, url, contenido))
                    if len(resultados) >= num_resultados:
                        break
        return resultados
    except Exception as e:
        print(f"Error en la búsqueda: {str(e)}")
        return resultados

# Función para extraer contenido de una URL
def extraer_contenido(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Aquí puedes ajustar qué parte del contenido deseas extraer de la página web.
            # En este caso, estamos extrayendo el texto dentro de las etiquetas 'p'.
            contenido = "\n".join([p.text for p in soup.find_all('p')])
            return contenido
        return ""
    except Exception as e:
        return ""

# Función para guardar resultados en un archivo de texto
def guardar_resultados(resultados):
    opcion = input("¿Desea guardar los resultados en un archivo de texto? (Sí­/No): ").strip().lower()
    if opcion == "si" or opcion == "sí":
        eleccion = input("¿Desea guardar todos los resultados o elegir uno? (Todos/Uno): ").strip().lower()
        if eleccion == "todos":
            nombre_archivo = input("Especifique un nombre para el archivo de texto (sin la extensión .txt): ").strip()
            if not nombre_archivo:
                nombre_archivo = "resultados_completos"
            nombre_archivo += ".txt"
            with open(nombre_archivo, "w") as archivo:
                for i, resultado in enumerate(resultados, start=1):
                    contenido = resultado[2]  # Obtenemos solo el contenido buscado
                    archivo.write(f"Resultado {i}:\n")
                    archivo.write(contenido)
                    archivo.write("\n\n")
            print(f"Resultados completos guardados en '{nombre_archivo}'.")
        elif eleccion == "uno":
            numero_resultado = int(input(f"Elija el número del resultado que desea guardar (1-5): ").strip())
            if 1 <= numero_resultado <= 5:
                nombre_archivo = input("Especifique un nombre para el archivo de texto (sin la extensión .txt): ").strip()
                if not nombre_archivo:
                    nombre_archivo = f"resultado_{numero_resultado}"
                nombre_archivo += ".txt"
                with open(nombre_archivo, "w") as archivo:
                    contenido = resultados[numero_resultado - 1][2]  # Obtenemos solo el contenido buscado
                    archivo.write(contenido)
                print(f"Resultado {numero_resultado} guardado en '{nombre_archivo}'.")
            else:
                print("Número de resultado no válido.")
        else:
            print("Opción no válida.")
    else:
        print("Resultados no guardados.")

# Ejecutar la búsqueda y resumen de información
buscar_y_resumir_informacion()
