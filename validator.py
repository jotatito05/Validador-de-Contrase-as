# -*- coding: utf-8 -*-
"""
Módulo principal de validación de contraseñas.
Coordina todas las validaciones y calcula la puntuación final de seguridad.
"""

from hibp_api import HIBPChecker
import utils


class ValidadorContrasena:
    """
    Coordina todas las validaciones de contraseña y calcula la puntuación final.
    """
    
    def __init__(self):
        """
        Inicializa el validador de contraseñas.
        """
        self.hibp_checker = HIBPChecker()
        self.contrasenas_comunes = None
        
        # Intentar cargar la lista de contraseñas comunes
        try:
            self.contrasenas_comunes = utils.cargar_contrasenas_comunes()
        except (FileNotFoundError, IOError):
            # Si no se puede cargar, continuar sin esta validación
            self.contrasenas_comunes = set()
    
    def validar(self, contrasena):
        """
        Valida una contraseña contra todos los criterios de seguridad.
        
        Args:
            contrasena (str): La contraseña a validar
            
        Returns:
            dict: Diccionario con la estructura:
                {
                    'puntuacion': int (0-100),
                    'nivel': str,
                    'criterios': {
                        'longitud': dict,
                        'complejidad': dict,
                        'patrones': dict,
                        'comun': bool,
                        'filtrada': dict
                    },
                    'sugerencias': list[str]
                }
        """
        # Validar cada criterio
        criterios = {
            'longitud': self._validar_longitud(contrasena),
            'complejidad': self._validar_complejidad(contrasena),
            'patrones': self._detectar_patrones(contrasena),
            'comun': self._verificar_contrasena_comun(contrasena),
            'filtrada': self._verificar_filtrada(contrasena)
        }
        
        # Calcular puntuación total
        puntuacion = self._calcular_puntuacion(criterios)
        
        # Determinar nivel de seguridad
        nivel = self._determinar_nivel(puntuacion, criterios)
        
        # Generar sugerencias
        sugerencias = self._generar_sugerencias(criterios)
        
        return {
            'puntuacion': puntuacion,
            'nivel': nivel,
            'criterios': criterios,
            'sugerencias': sugerencias
        }
    
    def _validar_longitud(self, contrasena):
        """
        Valida la longitud de la contraseña.
        
        Args:
            contrasena (str): La contraseña a validar
            
        Returns:
            dict: Información sobre la longitud y puntos asignados
        """
        longitud = len(contrasena)
        
        # Asignar puntos según la longitud
        if longitud < 8:
            puntos = 0
            cumple = False
        elif longitud <= 10:
            puntos = 10
            cumple = True
        elif longitud <= 12:
            puntos = 15
            cumple = True
        elif longitud <= 15:
            puntos = 20
            cumple = True
        else:
            puntos = 25
            cumple = True
        
        return {
            'valor': longitud,
            'cumple': cumple,
            'puntos': puntos
        }

    def _validar_complejidad(self, contrasena):
        """
        Valida la complejidad de caracteres de la contraseña.
        Verifica la presencia de mayúsculas, minúsculas, números y caracteres especiales.
        
        Args:
            contrasena (str): La contraseña a validar
            
        Returns:
            dict: Información sobre los tipos de caracteres y puntos asignados
        """
        # Verificar cada tipo de carácter
        tiene_mayus = utils.tiene_mayusculas(contrasena)
        tiene_minus = utils.tiene_minusculas(contrasena)
        tiene_nums = utils.tiene_numeros(contrasena)
        tiene_especiales = utils.tiene_caracteres_especiales(contrasena)
        
        # Contar cuántos tipos de caracteres se usan
        tipos_usados = sum([tiene_mayus, tiene_minus, tiene_nums, tiene_especiales])
        
        # Asignar puntos según la cantidad de tipos
        if tipos_usados == 1:
            puntos = 5
            cumple = False
        elif tipos_usados == 2:
            puntos = 15
            cumple = False
        elif tipos_usados == 3:
            puntos = 25
            cumple = True
        else:  # 4 tipos
            puntos = 30
            cumple = True
        
        return {
            'mayusculas': tiene_mayus,
            'minusculas': tiene_minus,
            'numeros': tiene_nums,
            'especiales': tiene_especiales,
            'tipos_usados': tipos_usados,
            'cumple': cumple,
            'puntos': puntos
        }

    def _detectar_patrones(self, contrasena):
        """
        Detecta patrones comunes en la contraseña.
        Busca secuencias numéricas, alfabéticas y repeticiones de caracteres.
        
        Args:
            contrasena (str): La contraseña a validar
            
        Returns:
            dict: Información sobre los patrones detectados y puntos asignados
        """
        # Detectar cada tipo de patrón
        tiene_sec_numerica = utils.detectar_secuencia_numerica(contrasena)
        tiene_sec_alfabetica = utils.detectar_secuencia_alfabetica(contrasena)
        tiene_repeticiones = utils.detectar_repeticiones(contrasena)
        
        # Contar cuántos patrones se detectaron
        patrones_detectados = sum([tiene_sec_numerica, tiene_sec_alfabetica, tiene_repeticiones])
        
        # Asignar puntos según los patrones detectados
        if patrones_detectados == 0:
            puntos = 20
            cumple = True
        elif patrones_detectados == 1:
            puntos = 10
            cumple = False
        else:  # 2 o más patrones
            puntos = 0
            cumple = False
        
        return {
            'secuencias_numericas': tiene_sec_numerica,
            'secuencias_alfabeticas': tiene_sec_alfabetica,
            'repeticiones': tiene_repeticiones,
            'cumple': cumple,
            'puntos': puntos
        }

    def _verificar_contrasena_comun(self, contrasena):
        """
        Verifica si la contraseña está en la lista de contraseñas comunes.
        
        Args:
            contrasena (str): La contraseña a validar
            
        Returns:
            bool: True si la contraseña es común, False en caso contrario
        """
        # Comparar en minúsculas para hacer la comparación case-insensitive
        return contrasena.lower() in self.contrasenas_comunes

    def _verificar_filtrada(self, contrasena):
        """
        Verifica si la contraseña ha sido filtrada usando la API de Have I Been Pwned.
        
        Args:
            contrasena (str): La contraseña a validar
            
        Returns:
            dict: Información sobre si la contraseña ha sido filtrada
        """
        try:
            resultado = self.hibp_checker.verificar_contrasena(contrasena)
            return resultado
        except Exception as e:
            # Si hay cualquier error, continuar sin esta validación
            return {
                'filtrada': False,
                'veces_vista': 0,
                'error': f'No se pudo verificar filtraciones: {str(e)}'
            }

    def _calcular_puntuacion(self, criterios):
        """
        Calcula la puntuación total de la contraseña.
        
        Args:
            criterios (dict): Diccionario con todos los criterios evaluados
            
        Returns:
            int: Puntuación total (0-100)
        """
        puntuacion = 0
        
        # Sumar puntos de longitud
        puntuacion += criterios['longitud']['puntos']
        
        # Sumar puntos de complejidad
        puntuacion += criterios['complejidad']['puntos']
        
        # Sumar puntos de patrones
        puntuacion += criterios['patrones']['puntos']
        
        # Sumar puntos si no es contraseña común
        if not criterios['comun']:
            puntuacion += 15
        
        # Sumar puntos si no está filtrada
        if not criterios['filtrada']['filtrada']:
            puntuacion += 10
        
        return puntuacion
    
    def _determinar_nivel(self, puntuacion, criterios):
        """
        Determina el nivel de seguridad basado en la puntuación y criterios especiales.
        
        Args:
            puntuacion (int): Puntuación total
            criterios (dict): Diccionario con todos los criterios evaluados
            
        Returns:
            str: Nivel de seguridad
        """
        # Casos especiales que anulan la puntuación
        if criterios['filtrada']['filtrada']:
            veces = criterios['filtrada']['veces_vista']
            if veces >= 100:
                return 'Muy Comprometida'
            else:
                return 'Comprometida'
        
        if criterios['comun']:
            return 'Muy Débil'
        
        # Niveles normales basados en puntuación
        if puntuacion <= 30:
            return 'Muy Débil'
        elif puntuacion <= 50:
            return 'Débil'
        elif puntuacion <= 70:
            return 'Aceptable'
        elif puntuacion <= 85:
            return 'Fuerte'
        else:
            return 'Muy Fuerte'

    def _generar_sugerencias(self, criterios):
        """
        Genera sugerencias específicas para mejorar la contraseña.
        
        Args:
            criterios (dict): Diccionario con todos los criterios evaluados
            
        Returns:
            list: Lista de sugerencias en español
        """
        sugerencias = []
        
        # Advertencias críticas primero
        if criterios['filtrada']['filtrada']:
            veces = criterios['filtrada']['veces_vista']
            sugerencias.append(
                f'⚠️ CRÍTICO: Esta contraseña ha sido encontrada en {veces} filtraciones de datos. '
                'NUNCA uses esta contraseña. Cámbiala inmediatamente.'
            )
        
        if criterios['comun']:
            sugerencias.append(
                '⚠️ Esta contraseña está en la lista de contraseñas más comunes. '
                'Es extremadamente vulnerable a ataques.'
            )
        
        # Sugerencias sobre longitud
        longitud = criterios['longitud']['valor']
        if longitud < 8:
            sugerencias.append('❌ Tu contraseña es demasiado corta. Usa al menos 8 caracteres.')
        elif longitud < 12:
            sugerencias.append('⚡ Considera usar al menos 12 caracteres para mayor seguridad.')
        
        # Sugerencias sobre complejidad
        comp = criterios['complejidad']
        if not comp['mayusculas']:
            sugerencias.append('💡 Agrega letras MAYÚSCULAS para aumentar la complejidad.')
        if not comp['minusculas']:
            sugerencias.append('💡 Agrega letras minúsculas para aumentar la complejidad.')
        if not comp['numeros']:
            sugerencias.append('💡 Agrega números para aumentar la complejidad.')
        if not comp['especiales']:
            sugerencias.append('💡 Agrega caracteres especiales (!@#$%^&*) para mayor seguridad.')
        
        # Sugerencias sobre patrones
        pat = criterios['patrones']
        if pat['secuencias_numericas']:
            sugerencias.append('⚠️ Evita secuencias numéricas como 123 o 456.')
        if pat['secuencias_alfabeticas']:
            sugerencias.append('⚠️ Evita secuencias alfabéticas como abc o xyz.')
        if pat['repeticiones']:
            sugerencias.append('⚠️ Evita repetir el mismo carácter varias veces seguidas.')
        
        # Mensaje positivo si no hay sugerencias
        if not sugerencias:
            sugerencias.append('✅ ¡Excelente! Tu contraseña cumple con todos los criterios de seguridad.')
        
        # Advertencia sobre error de API si existe
        if criterios['filtrada']['error']:
            sugerencias.append(
                f'ℹ️ Nota: {criterios["filtrada"]["error"]}'
            )
        
        return sugerencias
