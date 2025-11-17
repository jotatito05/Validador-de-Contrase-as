# -*- coding: utf-8 -*-
"""
Cliente para la API de Have I Been Pwned (HIBP).
Verifica si una contraseña ha sido comprometida en filtraciones de datos usando k-anonymity.
"""

import hashlib
import requests


class HIBPChecker:
    """
    Cliente para verificar contraseñas contra la base de datos de Have I Been Pwned.
    Utiliza el método k-anonymity para proteger la privacidad de las contraseñas.
    """
    
    API_URL = "https://api.pwnedpasswords.com/range/"
    
    def __init__(self, timeout=5):
        """
        Inicializa el cliente HIBP.
        
        Args:
            timeout (int): Tiempo máximo de espera para las peticiones HTTP en segundos
        """
        self.timeout = timeout
    
    def verificar_contrasena(self, contrasena):
        """
        Verifica si una contraseña ha sido filtrada en bases de datos comprometidas.
        
        Utiliza k-anonymity: solo envía los primeros 5 caracteres del hash SHA-1
        de la contraseña a la API, protegiendo así la privacidad del usuario.
        
        Args:
            contrasena (str): La contraseña a verificar
            
        Returns:
            dict: Diccionario con la estructura:
                {
                    'filtrada': bool,
                    'veces_vista': int,
                    'error': str | None
                }
        """
        try:
            # Generar hash SHA-1 de la contraseña
            hash_completo = self._generar_hash_sha1(contrasena)
            
            # Separar en prefijo (primeros 5 caracteres) y sufijo (resto)
            prefijo = hash_completo[:5]
            sufijo = hash_completo[5:]
            
            # Consultar la API con el prefijo
            respuesta = self._consultar_api(prefijo)
            
            if respuesta is None:
                return {
                    'filtrada': False,
                    'veces_vista': 0,
                    'error': 'No se pudo conectar con la API'
                }
            
            # Buscar el sufijo en la respuesta
            veces_vista = self._buscar_sufijo(sufijo, respuesta)
            
            return {
                'filtrada': veces_vista > 0,
                'veces_vista': veces_vista,
                'error': None
            }
            
        except Exception as e:
            return {
                'filtrada': False,
                'veces_vista': 0,
                'error': f'Error inesperado: {str(e)}'
            }
    
    def _generar_hash_sha1(self, contrasena):
        """
        Genera el hash SHA-1 de una contraseña.
        
        Args:
            contrasena (str): La contraseña a hashear
            
        Returns:
            str: Hash SHA-1 en mayúsculas
        """
        # Convertir la contraseña a bytes y generar el hash
        hash_objeto = hashlib.sha1(contrasena.encode('utf-8'))
        # Retornar el hash en formato hexadecimal en mayúsculas
        return hash_objeto.hexdigest().upper()
    
    def _consultar_api(self, prefijo_hash):
        """
        Consulta la API de HIBP con el prefijo del hash.
        
        Args:
            prefijo_hash (str): Los primeros 5 caracteres del hash SHA-1
            
        Returns:
            str | None: Respuesta de la API o None si hay error
        """
        try:
            url = f"{self.API_URL}{prefijo_hash}"
            
            # Realizar la petición GET con timeout
            response = requests.get(url, timeout=self.timeout)
            
            # Verificar que la respuesta sea exitosa
            response.raise_for_status()
            
            return response.text
            
        except requests.Timeout:
            # Timeout al esperar respuesta
            return None
            
        except requests.RequestException:
            # Cualquier otro error de red
            return None
    
    def _buscar_sufijo(self, sufijo, respuesta):
        """
        Busca el sufijo del hash en la respuesta de la API.
        
        La API retorna una lista de sufijos de hash con el número de veces
        que cada uno ha sido visto en filtraciones, en el formato:
        SUFIJO:CANTIDAD
        
        Args:
            sufijo (str): El sufijo del hash a buscar
            respuesta (str): La respuesta de la API
            
        Returns:
            int: Número de veces que la contraseña ha sido vista (0 si no se encuentra)
        """
        # Dividir la respuesta en líneas
        lineas = respuesta.split('\n')
        
        # Buscar el sufijo en cada línea
        for linea in lineas:
            if ':' in linea:
                # Separar el sufijo y la cantidad
                hash_sufijo, cantidad = linea.split(':')
                
                # Comparar el sufijo (case-insensitive)
                if hash_sufijo.strip().upper() == sufijo.upper():
                    return int(cantidad.strip())
        
        # Si no se encuentra, la contraseña no ha sido filtrada
        return 0
