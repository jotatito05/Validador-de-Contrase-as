# -*- coding: utf-8 -*-
"""
Módulo de utilidades para validación de contraseñas.
Contiene funciones auxiliares para detectar tipos de caracteres y patrones comunes.
"""

import re
import os


def tiene_mayusculas(texto):
    """
    Verifica si el texto contiene al menos una letra mayúscula.
    
    Args:
        texto (str): El texto a verificar
        
    Returns:
        bool: True si contiene mayúsculas, False en caso contrario
    """
    return any(c.isupper() for c in texto)


def tiene_minusculas(texto):
    """
    Verifica si el texto contiene al menos una letra minúscula.
    
    Args:
        texto (str): El texto a verificar
        
    Returns:
        bool: True si contiene minúsculas, False en caso contrario
    """
    return any(c.islower() for c in texto)


def tiene_numeros(texto):
    """
    Verifica si el texto contiene al menos un número.
    
    Args:
        texto (str): El texto a verificar
        
    Returns:
        bool: True si contiene números, False en caso contrario
    """
    return any(c.isdigit() for c in texto)


def tiene_caracteres_especiales(texto):
    """
    Verifica si el texto contiene al menos un carácter especial.
    Caracteres especiales considerados: !@#$%^&*()_+-=[]{}|;:,.<>?
    
    Args:
        texto (str): El texto a verificar
        
    Returns:
        bool: True si contiene caracteres especiales, False en caso contrario
    """
    caracteres_especiales = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    return any(c in caracteres_especiales for c in texto)


def detectar_secuencia_numerica(texto):
    """
    Detecta secuencias numéricas comunes en el texto (ej: 123, 1234, 456).
    
    Args:
        texto (str): El texto a verificar
        
    Returns:
        bool: True si se detecta una secuencia numérica, False en caso contrario
    """
    # Buscar secuencias ascendentes de 3 o más dígitos consecutivos
    for i in range(len(texto) - 2):
        if texto[i:i+3].isdigit():
            nums = [int(texto[i+j]) for j in range(3)]
            if nums[1] == nums[0] + 1 and nums[2] == nums[1] + 1:
                return True
    
    # Buscar secuencias descendentes
    for i in range(len(texto) - 2):
        if texto[i:i+3].isdigit():
            nums = [int(texto[i+j]) for j in range(3)]
            if nums[1] == nums[0] - 1 and nums[2] == nums[1] - 1:
                return True
    
    return False


def detectar_secuencia_alfabetica(texto):
    """
    Detecta secuencias alfabéticas comunes en el texto (ej: abc, xyz, def).
    
    Args:
        texto (str): El texto a verificar
        
    Returns:
        bool: True si se detecta una secuencia alfabética, False en caso contrario
    """
    texto_lower = texto.lower()
    
    # Buscar secuencias ascendentes de 3 o más letras consecutivas
    for i in range(len(texto_lower) - 2):
        if texto_lower[i:i+3].isalpha():
            chars = [ord(texto_lower[i+j]) for j in range(3)]
            if chars[1] == chars[0] + 1 and chars[2] == chars[1] + 1:
                return True
    
    # Buscar secuencias descendentes
    for i in range(len(texto_lower) - 2):
        if texto_lower[i:i+3].isalpha():
            chars = [ord(texto_lower[i+j]) for j in range(3)]
            if chars[1] == chars[0] - 1 and chars[2] == chars[1] - 1:
                return True
    
    return False


def detectar_repeticiones(texto):
    """
    Detecta repeticiones de caracteres en el texto (ej: aaa, 111, !!!).
    
    Args:
        texto (str): El texto a verificar
        
    Returns:
        bool: True si se detecta una repetición de 3 o más caracteres, False en caso contrario
    """
    # Buscar 3 o más caracteres idénticos consecutivos
    for i in range(len(texto) - 2):
        if texto[i] == texto[i+1] == texto[i+2]:
            return True
    
    return False


def cargar_contrasenas_comunes():
    """
    Carga la lista de contraseñas comunes desde el archivo resources/passwords_common.txt.
    
    Returns:
        set: Conjunto de contraseñas comunes (en minúsculas para comparación case-insensitive)
        
    Raises:
        FileNotFoundError: Si el archivo no existe
        IOError: Si hay un error al leer el archivo
    """
    ruta_archivo = os.path.join('resources', 'passwords_common.txt')
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            # Leer todas las líneas, eliminar espacios en blanco y convertir a minúsculas
            contrasenas = {linea.strip().lower() for linea in archivo if linea.strip()}
        return contrasenas
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo de contraseñas comunes: {ruta_archivo}")
    except IOError as e:
        raise IOError(f"Error al leer el archivo de contraseñas comunes: {e}")
