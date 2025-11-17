# Plan de Implementación - Validador de Contraseñas

- [x] 1. Configurar estructura del proyecto y archivos base


  - Crear estructura de directorios (resources/, tests/)
  - Crear archivo requirements.txt con dependencias
  - Crear archivo README.md con descripción del proyecto e instrucciones de uso
  - Crear archivo .gitignore para Python
  - _Requirements: 6.1, 6.2, 6.3, 6.4_


- [x] 2. Implementar módulo de utilidades (utils.py)

  - Crear funciones para detectar tipos de caracteres (mayúsculas, minúsculas, números, especiales)
  - Implementar funciones para detectar patrones (secuencias numéricas, alfabéticas, repeticiones)
  - Implementar función para cargar lista de contraseñas comunes desde archivo
  - Todos los comentarios y docstrings deben estar en español
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 6.1, 6.2_

- [ ]* 2.1 Escribir pruebas unitarias para utils.py
  - Crear test_utils.py con casos de prueba para cada función
  - Incluir casos de borde y casos especiales
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3_

- [x] 3. Crear lista de contraseñas comunes


  - Crear archivo resources/passwords_common.txt con las 1000 contraseñas más comunes
  - Incluir contraseñas como: password, 123456, qwerty, admin, letmein, etc.
  - Una contraseña por línea
  - _Requirements: 4.1, 4.2_

- [x] 4. Implementar cliente de API Have I Been Pwned (hibp_api.py)


  - Crear clase HIBPChecker con método para generar hash SHA-1
  - Implementar método para consultar API usando k-anonymity (solo primeros 5 caracteres del hash)
  - Implementar método para buscar sufijo del hash en la respuesta
  - Implementar manejo de errores (timeout, errores de red)
  - Todos los comentarios y docstrings deben estar en español
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6.1, 6.2_

- [ ]* 4.1 Escribir pruebas unitarias para hibp_api.py
  - Crear test_hibp_api.py con mocks para evitar llamadas reales a la API
  - Probar generación de hash, parsing de respuesta, manejo de errores
  - _Requirements: 5.1, 5.2, 5.6_

- [x] 5. Implementar validador principal (validator.py)


- [x] 5.1 Crear clase ValidadorContrasena con método de validación de longitud


  - Implementar _validar_longitud() que evalúe la longitud según criterios
  - Asignar puntos según la longitud (< 8: 0pts, 8-10: 10pts, 11-12: 15pts, 13-15: 20pts, >15: 25pts)
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 6.1, 6.2_

- [x] 5.2 Implementar validación de complejidad de caracteres


  - Crear método _validar_complejidad() que use funciones de utils.py
  - Verificar presencia de mayúsculas, minúsculas, números y caracteres especiales
  - Asignar puntos según tipos de caracteres (1 tipo: 5pts, 2 tipos: 15pts, 3 tipos: 25pts, 4 tipos: 30pts)
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 6.1, 6.2_

- [x] 5.3 Implementar detección de patrones comunes


  - Crear método _detectar_patrones() que use funciones de utils.py
  - Detectar secuencias numéricas, alfabéticas y repeticiones
  - Reducir puntuación según patrones detectados (sin patrones: 20pts, 1 patrón: 10pts, 2+: 0pts)
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 6.1, 6.2_

- [x] 5.4 Implementar verificación contra contraseñas comunes


  - Crear método _verificar_contrasena_comun() que compare con la lista cargada
  - Si la contraseña está en la lista, clasificarla como "Muy Débil"
  - _Requirements: 4.1, 4.2, 4.3, 6.1, 6.2_

- [x] 5.5 Integrar verificación de contraseñas filtradas


  - Instanciar HIBPChecker en ValidadorContrasena
  - Llamar a verificar_contrasena() y manejar el resultado
  - Implementar manejo de errores para continuar si la API no está disponible
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6.1, 6.2_

- [x] 5.6 Implementar cálculo de puntuación y nivel de seguridad


  - Crear método _calcular_puntuacion() que sume puntos de todos los criterios
  - Crear método _determinar_nivel() que asigne nivel según puntuación
  - Niveles: Muy Débil (0-30), Débil (31-50), Aceptable (51-70), Fuerte (71-85), Muy Fuerte (86-100)
  - Manejar casos especiales: contraseña común = "Muy Débil", filtrada = "Comprometida"
  - _Requirements: 7.1, 7.2, 6.1, 6.2_

- [x] 5.7 Implementar generación de sugerencias


  - Crear método _generar_sugerencias() que analice los criterios no cumplidos
  - Generar sugerencias específicas para mejorar la contraseña
  - Incluir advertencias sobre contraseñas comunes o filtradas
  - Todas las sugerencias deben estar en español
  - _Requirements: 7.3, 7.4, 6.1, 6.2, 6.4_

- [x] 5.8 Integrar todos los métodos en el método principal validar()


  - Coordinar todas las validaciones en el método validar()
  - Retornar diccionario con estructura completa de resultados
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 6.1, 6.2_

- [ ]* 5.9 Escribir pruebas unitarias para validator.py
  - Crear test_validator.py con casos de prueba para cada método
  - Probar cálculo de puntuación, generación de sugerencias, casos de borde
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.2, 4.3, 7.1, 7.2, 7.3, 7.4_

- [x] 6. Implementar interfaz de línea de comandos (password_checker.py)


- [x] 6.1 Crear función para solicitar contraseña de forma segura


  - Implementar solicitar_contrasena() usando getpass para ocultar entrada
  - Validar que la contraseña no esté vacía
  - _Requirements: 8.1, 8.2, 6.1, 6.2, 6.4_

- [x] 6.2 Crear función para mostrar resultados


  - Implementar mostrar_resultados() que presente puntuación, nivel y criterios
  - Formatear salida de forma clara y organizada
  - Usar colores o símbolos para mejorar legibilidad (opcional)
  - Todos los mensajes deben estar en español
  - _Requirements: 8.3, 7.3, 6.1, 6.2, 6.4_

- [x] 6.3 Crear función para mostrar sugerencias


  - Implementar mostrar_sugerencias() que presente recomendaciones
  - Formatear sugerencias de forma clara
  - _Requirements: 8.3, 7.4, 6.1, 6.2, 6.4_

- [x] 6.4 Implementar bucle principal de la aplicación


  - Crear función main() que coordine el flujo de la aplicación
  - Solicitar contraseña, validar, mostrar resultados y sugerencias
  - Preguntar si el usuario desea validar otra contraseña
  - Permitir salir del programa de forma elegante
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 6.1, 6.2, 6.4_

- [ ]* 6.5 Escribir pruebas de integración
  - Crear test_integration.py que pruebe el flujo completo
  - Probar con contraseñas conocidas (débiles y fuertes)
  - Verificar que todos los módulos se integran correctamente
  - _Requirements: 1.1, 2.1, 3.1, 4.1, 5.1, 7.1, 8.1_

- [x] 7. Documentación final y pulido



  - Actualizar README.md con ejemplos de uso y capturas de pantalla
  - Verificar que todos los comentarios estén en español
  - Agregar sección de instalación y requisitos en README
  - Agregar ejemplos de salida del programa
  - Agregar licencia (MIT recomendada para proyectos de GitHub)
  - _Requirements: 6.1, 6.2, 6.3, 6.4_
