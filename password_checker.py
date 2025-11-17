# -*- coding: utf-8 -*-
"""
Validador de Contraseñas Seguras - Interfaz de Línea de Comandos
Aplicación para evaluar la seguridad de contraseñas.
"""

import getpass
from validator import ValidadorContrasena


def solicitar_contrasena():
    """
    Solicita una contraseña al usuario de forma segura (sin mostrarla en pantalla).
    
    Returns:
        str: La contraseña ingresada por el usuario
        
    Raises:
        ValueError: Si la contraseña está vacía
    """
    contrasena = getpass.getpass('Ingresa la contraseña a validar: ')
    
    if not contrasena or contrasena.strip() == '':
        raise ValueError('La contraseña no puede estar vacía')
    
    return contrasena


def mostrar_resultados(resultado):
    """
    Muestra los resultados del análisis de la contraseña de forma clara y organizada.
    
    Args:
        resultado (dict): Diccionario con los resultados de la validación
    """
    print('\n' + '='*50)
    print('--- RESULTADOS DEL ANÁLISIS ---')
    print('='*50)
    
    # Mostrar puntuación y nivel
    print(f'\n📊 Puntuación: {resultado["puntuacion"]}/100')
    print(f'🔒 Nivel de Seguridad: {resultado["nivel"].upper()}')
    
    # Mostrar criterios evaluados
    print('\n--- CRITERIOS EVALUADOS ---\n')
    
    # Longitud
    longitud = resultado['criterios']['longitud']
    simbolo = '✓' if longitud['cumple'] else '✗'
    print(f'{simbolo} Longitud: {longitud["valor"]} caracteres ({longitud["puntos"]} puntos)')
    
    # Complejidad
    comp = resultado['criterios']['complejidad']
    simbolo = '✓' if comp['cumple'] else '✗'
    print(f'{simbolo} Complejidad: {comp["tipos_usados"]} tipos de caracteres ({comp["puntos"]} puntos)')
    print(f'  - Mayúsculas: {"Sí" if comp["mayusculas"] else "No"}')
    print(f'  - Minúsculas: {"Sí" if comp["minusculas"] else "No"}')
    print(f'  - Números: {"Sí" if comp["numeros"] else "No"}')
    print(f'  - Especiales: {"Sí" if comp["especiales"] else "No"}')
    
    # Patrones
    pat = resultado['criterios']['patrones']
    simbolo = '✓' if pat['cumple'] else '✗'
    print(f'{simbolo} Patrones: {"Sin patrones detectados" if pat["cumple"] else "Patrones detectados"} ({pat["puntos"]} puntos)')
    if pat['secuencias_numericas']:
        print('  - Secuencias numéricas detectadas')
    if pat['secuencias_alfabeticas']:
        print('  - Secuencias alfabéticas detectadas')
    if pat['repeticiones']:
        print('  - Repeticiones detectadas')
    
    # Contraseña común
    es_comun = resultado['criterios']['comun']
    simbolo = '✗' if es_comun else '✓'
    print(f'{simbolo} Contraseña común: {"Sí (0 puntos)" if es_comun else "No (15 puntos)"}')
    
    # Filtrada
    filtrada = resultado['criterios']['filtrada']
    if filtrada['filtrada']:
        print(f'✗ Filtrada: Sí - Vista {filtrada["veces_vista"]} veces (0 puntos)')
    else:
        print(f'✓ Filtrada: No (10 puntos)')


def mostrar_sugerencias(resultado):
    """
    Muestra las sugerencias para mejorar la contraseña.
    
    Args:
        resultado (dict): Diccionario con los resultados de la validación
    """
    print('\n' + '='*50)
    print('--- SUGERENCIAS ---')
    print('='*50 + '\n')
    
    for sugerencia in resultado['sugerencias']:
        print(f'{sugerencia}')
        print()


def main():
    """
    Función principal de la aplicación.
    Coordina el flujo de solicitud, validación y presentación de resultados.
    """
    print('='*50)
    print('  VALIDADOR DE CONTRASEÑAS SEGURAS')
    print('='*50)
    print('\nEste programa evalúa la seguridad de tu contraseña')
    print('y te proporciona sugerencias para mejorarla.\n')
    
    # Crear instancia del validador
    validador = ValidadorContrasena()
    
    # Bucle principal
    while True:
        try:
            # Solicitar contraseña
            contrasena = solicitar_contrasena()
            
            # Validar contraseña
            print('\n⏳ Analizando contraseña...')
            resultado = validador.validar(contrasena)
            
            # Mostrar resultados
            mostrar_resultados(resultado)
            
            # Mostrar sugerencias
            mostrar_sugerencias(resultado)
            
        except ValueError as e:
            print(f'\n❌ Error: {e}')
        except KeyboardInterrupt:
            print('\n\n👋 Programa interrumpido por el usuario.')
            break
        except Exception as e:
            print(f'\n❌ Error inesperado: {e}')
        
        # Preguntar si desea continuar
        print('='*50)
        respuesta = input('¿Deseas validar otra contraseña? (s/n): ').strip().lower()
        
        if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
            print('\n👋 ¡Gracias por usar el Validador de Contraseñas!')
            print('Recuerda: Una contraseña fuerte es tu primera línea de defensa.\n')
            break


if __name__ == '__main__':
    main()
