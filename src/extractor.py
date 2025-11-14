import newspaper
import sys
import pandas as pd
from datetime import datetime
import time 

URL_DE_PRUEBA = "https://www.lanacion.com.ar/economia/dolar/valores-de-enero-el-riesgo-pais-perfora-la-barrera-de-los-600-puntos-basicos-nid10112025" 


def extraer_contenido_noticia(url, max_retries=3):
    """
    Extrae el contenido principal y los metadatos de un artículo, con reintentos.
    """
    for attempt in range(max_retries):
        try:
            # 1. Construir el objeto Artículo
            article = newspaper.Article(url)
            
            # 2. Descargar el contenido de la URL
            article.download()
            
            # 3. Analizar (parsear) el contenido para extraer texto principal, título, etc.
            article.parse()
            
            # 4. (Opcional) Análisis de Lenguaje Natural para mejorar la limpieza
            article.nlp()

            # 5. Estructurar la salida
            titulo = article.title
            autor = ", ".join(article.authors) if article.authors else "No disponible"
            
            # Formatear la fecha si está disponible
            fecha_pub = "No disponible"
            if article.publish_date:
                try:
                    # Esto hace que sea fácil de guardar en un CSV o DB.
                    fecha_pub = article.publish_date.strftime('%Y-%m-%d %H:%M:%S')
                except AttributeError:
                    # Si no es un objeto datetime (raro), lo deja como string.
                    fecha_pub = str(article.publish_date)
            
            contenido = article.text
            return {
                "URL": url,
                "Título": titulo,
                "Autor": autor,
                "Fecha": fecha_pub,
                "Contenido": contenido,
                "Resumen": article.summary
            }
        
        except newspaper.article.ArticleException as e:
            # Si falla la descarga, intentamos de nuevo (salvo en el último intento)
            if attempt < max_retries - 1:
                print(f"Intento {attempt + 1} fallido. Reintentando en 2 segundos...")
                time.sleep(2)
            else:
                return {"Error": f"No se pudo descargar o analizar la URL después de {max_retries} intentos. Error: {e}", "URL": url}
        
        except Exception as e:
            return {"Error": f"Ocurrió un error inesperado: {e}", "URL": url}
    
    # Esto solo se alcanza si el bucle termina sin éxito
    return {"Error": "La extracción falló por un motivo desconocido después de reintentos.", "URL": url}


def main():
    """
    Función principal que maneja la entrada de la URL y guarda en CSV.
    """
    # Determinar la URL de entrada
    if len(sys.argv) > 1:
        # Si se proporciona una URL como argumento al script
        url_a_procesar = sys.argv[1]
    else:
        # Si no se proporciona, usa la URL de prueba
        print(f"⚠️ Usando URL de prueba: {URL_DE_PRUEBA}. Para usar otra, ejecuta: python extractor.py <URL>")
        url_a_procesar = URL_DE_PRUEBA
    
    print(f"\n✨ Procesando URL: {url_a_procesar}...")
    
    # Extraer el contenido
    datos_extraidos = extraer_contenido_noticia(url_a_procesar)
    
    # Imprimir la salida según el Criterio de Aceptación
    if "Error" in datos_extraidos:
        print("\n--- ❌ ERROR ---")
        print(datos_extraidos["Error"])
    else:
        print("\n--- ✅ Contenido Extraído (Listo para Análisis) ---")
        print(f"Título: {datos_extraidos['Título']}")
        print(f"Autor: {datos_extraidos['Autor']}")
        print(f"Fecha: {datos_extraidos['Fecha']}")
        print("Contenido (Extracto):")
        print("--------------------------------------------------")
        # Imprimir solo un extracto para que no sea muy largo en la terminal
        print(datos_extraidos['Contenido'][:500] + "..." if len(datos_extraidos['Contenido']) > 500 else datos_extraidos['Contenido'])
        print("--------------------------------------------------")
    
        # Crear un DataFrame de Pandas con los resultados
        # Usamos una lista de diccionarios para crear el DataFrame.
        df = pd.DataFrame([datos_extraidos])
        
        # Generar un nombre de archivo único con la fecha y hora
        nombre_archivo = f"noticia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(nombre_archivo, index=False, encoding='utf-8')
        
        print(f"\n✅ Datos guardados exitosamente en: {nombre_archivo}")


if __name__ == "__main__":
    main()
