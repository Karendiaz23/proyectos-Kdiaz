import newspaper
import sys
import pandas as pd
from datetime import datetime

# --- Configuración ---
# Puedes cambiar esta URL si quieres probar con otra
URL_DE_PRUEBA = "https://www.example.com/noticia-importante-de-ejemplo"
# NOTA: newspaper3k necesita URLs reales para funcionar bien.
# Reemplaza la URL de prueba de arriba por una URL de una noticia real para las pruebas.

def extraer_contenido_noticia(url):
    """
    Extrae el contenido principal y los metadatos de un artículo.
    """
    try:
        # 1. Construir el objeto Artículo
        article = newspaper.Article(url)
        
        # 2. Descargar el contenido de la URL
        article.download()
        
        # 3. Analizar (parsear) el contenido para extraer texto principal, título, etc.
        article.parse()
        
        # 4. (Opcional) Realizar la extracción de resumen o palabras clave (si es necesario)
        # Esto ayuda a "limpiar" más el texto.
        article.nlp()

        # 5. Estructurar la salida
        titulo = article.title
        autor = ", ".join(article.authors) if article.authors else "No disponible"
        
        # Formatear la fecha si está disponible
        fecha_pub = "No disponible"
        if article.publish_date:
            try:
                # Intenta formatear la fecha a un string ISO
                fecha_pub = article.publish_date.strftime('%Y-%m-%d %H:%M:%S')
            except AttributeError:
                # Si no es un objeto datetime, lo deja como está o lo convierte a string
                fecha_pub = str(article.publish_date)
        
        contenido = article.text
        
        # Devolver un diccionario con los resultados
        return {
            "URL": url,
            "Título": titulo,
            "Autor": autor,
            "Fecha": fecha_pub,
            "Contenido": contenido,
            "Resumen": article.summary
        }
    
    except newspaper.article.ArticleException as e:
        return {"Error": f"No se pudo descargar o analizar la URL. Asegúrate de que es una URL válida y accesible. Error: {e}", "URL": url}
    except Exception as e:
        return {"Error": f"Ocurrió un error inesperado: {e}", "URL": url}

def main():
    """
    Función principal que maneja la entrada de la URL (desde la terminal o usa la de prueba).
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
    
    # Imprimir la salida esperada (Criterio de Aceptación)
    if "Error" in datos_extraidos:
        print("\n--- ERROR ---")
        print(datos_extraidos["Error"])
    else:
        print("\n--- ✅ Contenido Extraído (Listo para Análisis) ---")
        print(f"Título: {datos_extraidos['Título']}")
        print(f"Autor: {datos_extraidos['Autor']}")
        print(f"Fecha: {datos_extraidos['Fecha']}")
        print("Contenido (Extracto):")
        # Imprimir solo un extracto del contenido para que no sea muy largo en la terminal
        print("--------------------------------------------------")
        print(datos_extraidos['Contenido'][:500] + "..." if len(datos_extraidos['Contenido']) > 500 else datos_extraidos['Contenido'])
        print("--------------------------------------------------")

        # --- Parte opcional: Guardar el contenido en un archivo CSV ---
        # Esto cumple con el flujo de guardar en CSV para su posterior análisis.
        
        # Crear un DataFrame de Pandas con los resultados
        df = pd.DataFrame([datos_extraidos])
        
        nombre_archivo = f"noticia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(nombre_archivo, index=False, encoding='utf-8')
        
        print(f"\n✅ Datos guardados exitosamente en: {nombre_archivo}")

if __name__ == "__main__":
    main()