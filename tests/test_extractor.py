import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys
import os

# Asegúrate de que Python pueda encontrar tu script extractor.py
# Agrega la ruta de la carpeta 'src' al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa la función que quieres testear desde tu script principal
from extractor import extraer_contenido_noticia 

# URL de ejemplo que usaremos en la simulación
URL_DE_PRUEBA = "https://www.prueba.com/articulo-mock"

# Datos que *esperamos* que extraiga el mock
TITULO_ESPERADO = "Título de Noticia Testeada y Correcta"
AUTOR_ESPERADO = ["Mariana la Analista", "Juan el Reportero"]
FECHA_ESPERADA_OBJETO = datetime(2025, 11, 10, 10, 30, 0)
FECHA_ESPERADA_STRING = "2025-11-10 10:30:00" # Formato de salida de nuestro extractor
CONTENIDO_ESPERADO = "Este es el contenido principal del artículo. Debe estar limpio sin anuncios ni menús."


class TestExtraccionNoticias(unittest.TestCase):
    """Clase para testear la función extraer_contenido_noticia."""

    # Usamos el decorador @patch para simular la biblioteca newspaper.Article
    @patch('newspaper.Article')
    def test_extraccion_metadatos_correcta(self, MockArticle):
        """Testea que el título, autor y fecha se extraigan correctamente."""
        
        # 1. Configuración de la Simulación (Mocking)
        # Creamos una instancia de la clase simulada
        mock_instance = MockArticle.return_value
        
        # Asignamos los valores que la instancia simulada debería 'extraer'
        mock_instance.title = TITULO_ESPERADO
        mock_instance.authors = AUTOR_ESPERADO
        mock_instance.publish_date = FECHA_ESPERADA_OBJETO
        mock_instance.text = CONTENIDO_ESPERADO
        mock_instance.summary = "Resumen de prueba"
        
        # Seteamos los métodos que no hacen nada (descarga, parseo, nlp)
        mock_instance.download = MagicMock()
        mock_instance.parse = MagicMock()
        mock_instance.nlp = MagicMock()

        # 2. Ejecución de la Función a Testear
        resultado = extraer_contenido_noticia(URL_DE_PRUEBA)
        
        # 3. Verificación de los Criterios de Aceptación
        
        # Criterio 1: El Título debe ser correcto
        self.assertEqual(resultado['Título'], TITULO_ESPERADO, 
                         "El título extraído no coincide con el esperado.")
        
        # Criterio 2: El Autor debe ser correcto y formateado
        # Nota: La salida es un string con los autores separados por ', '
        self.assertEqual(resultado['Autor'], "Mariana la Analista, Juan el Reportero", 
                         "Los autores extraídos o su formato no coinciden con el esperado.")
        
        # Criterio 3: La Fecha debe ser correcta y formateada
        self.assertEqual(resultado['Fecha'], FECHA_ESPERADA_STRING, 
                         "La fecha de publicación extraída no coincide con el esperado.")

        # Criterio 4: El Contenido debe ser el correcto (limpieza)
        self.assertEqual(resultado['Contenido'], CONTENIDO_ESPERADO, 
                         "El contenido principal extraído no coincide con el esperado (falla la limpieza).")


if __name__ == '__main__':
    # Ejecuta todos los tests definidos en esta clase
    unittest.main()