import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys
import os


# Importa la función que quieres testear desde tu script principal
# (Asumimos que test_extractor.py y extractor.py están en la misma carpeta)
# Nota: Si el import falla, puede que necesites configurar tu PYTHONPATH o mover los archivos.
try:
    from extractor import extraer_contenido_noticia
except ImportError:
    # Intento de ajuste de ruta en caso de estructura de carpeta (como el ejemplo original)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
    from extractor import extraer_contenido_noticia


# --- Configuración de Datos Mock (Simulados) ---
# Usamos estas variables para configurar nuestros "datos falsos"
URL_MOCK = "https://www.prueba.com/articulo-mock"
TITULO_MOCK = "El Último Trimestre Supera las Expectativas del Mercado"
AUTORES_MOCK = ["Mariana La Analista", "J. T. Smith"]
FECHA_MOCK_OBJETO = datetime(2025, 12, 25, 10, 30, 0)
FECHA_MOCK_STRING_FORMATO = "2025-12-25 10:30:00" # Formato de salida esperado de nuestro extractor
CONTENIDO_MOCK = "Este es el contenido de prueba. Es largo, limpio y listo para ser analizado..."


def configurar_mock_article(MockArticle):
    """
    Función auxiliar para configurar la simulación de la librería newspaper.Article
    y evitar repetir código en cada test.
    """
    mock_instance = MockArticle.return_value
    
    # Asignamos los valores que la instancia simulada debería 'extraer'
    mock_instance.title = TITULO_MOCK
    mock_instance.authors = AUTORES_MOCK
    mock_instance.publish_date = FECHA_MOCK_OBJETO
    mock_instance.text = CONTENIDO_MOCK
    mock_instance.summary = "Resumen de prueba"
    
    # Configuramos los métodos que el código principal llamará
    mock_instance.download = MagicMock()
    mock_instance.parse = MagicMock()
    mock_instance.nlp = MagicMock()

    return mock_instance


class TestExtraccionNoticias(unittest.TestCase):
    """
    Clase para testear la función extraer_contenido_noticia, con cada criterio en un test separado.
    """

    # Usamos @patch en cada test, es más simple para la explicación inicial
    # y asegura que cada test es independiente.
    
    @patch('newspaper.Article')
    def test_01_extraccion_titulo(self, MockArticle):
        """Testea que el TÍTULO del artículo se extraiga correctamente."""
        
        # 1. Configuración de la Simulación
        configurar_mock_article(MockArticle)

        # 2. Ejecución de la Función
        resultado = extraer_contenido_noticia(URL_MOCK)
        
        # 3. Verificación (Solo el Título)
        self.assertEqual(resultado['Título'], TITULO_MOCK,
                         "El Título extraído no coincide con el Título esperado.")


    @patch('newspaper.Article')
    def test_02_extraccion_autores(self, MockArticle):
        """Testea que los AUTORES del artículo se extraigan y formateen correctamente."""
        
        # 1. Configuración de la Simulación
        configurar_mock_article(MockArticle)

        # 2. Ejecución de la Función
        resultado = extraer_contenido_noticia(URL_MOCK)
        
        # 3. Verificación (Solo los Autores)
        autores_esperados_formato = "Mariana La Analista, J. T. Smith"
        self.assertEqual(resultado['Autor'], autores_esperados_formato,
                         "El formato de los Autores extraídos (separados por ', ') es incorrecto.")


    @patch('newspaper.Article')
    def test_03_extraccion_fecha_publicacion(self, MockArticle):
        """Testea que la FECHA de publicación se extraiga y formateee correctamente."""
        
        # 1. Configuración de la Simulación
        configurar_mock_article(MockArticle)

        # 2. Ejecución de la Función
        resultado = extraer_contenido_noticia(URL_MOCK)
        
        # 3. Verificación (Solo la Fecha)
        self.assertEqual(resultado['Fecha'], FECHA_MOCK_STRING_FORMATO,
                         "La Fecha de Publicación extraída no coincide con el formato 'YYYY-MM-DD HH:MM:SS' esperado.")


if __name__ == '__main__':
    # Ejecuta todos los tests definidos en esta clase
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
