# Requirements Document

## Introduction

Este proyecto implementa un validador de contraseñas que evalúa la seguridad de contraseñas proporcionadas por el usuario. El sistema analizará diferentes aspectos de la contraseña (longitud, complejidad, patrones comunes) y proporcionará retroalimentación sobre su nivel de seguridad, ayudando a los usuarios a crear contraseñas más robustas.

## Requirements

### Requirement 1: Validación de Longitud de Contraseña

**User Story:** Como usuario, quiero que el sistema valide la longitud de mi contraseña, para que pueda asegurarme de que cumple con los estándares mínimos de seguridad.

#### Acceptance Criteria

1. WHEN el usuario ingresa una contraseña THEN el sistema SHALL verificar que tenga al menos 8 caracteres
2. IF la contraseña tiene menos de 8 caracteres THEN el sistema SHALL indicar que es "Débil"
3. IF la contraseña tiene entre 8 y 12 caracteres THEN el sistema SHALL considerarla de longitud "Aceptable"
4. IF la contraseña tiene más de 12 caracteres THEN el sistema SHALL considerarla de longitud "Fuerte"

### Requirement 2: Validación de Complejidad de Caracteres

**User Story:** Como usuario, quiero que el sistema evalúe la variedad de caracteres en mi contraseña, para que pueda crear contraseñas más difíciles de adivinar.

#### Acceptance Criteria

1. WHEN el usuario ingresa una contraseña THEN el sistema SHALL verificar la presencia de letras minúsculas
2. WHEN el usuario ingresa una contraseña THEN el sistema SHALL verificar la presencia de letras mayúsculas
3. WHEN el usuario ingresa una contraseña THEN el sistema SHALL verificar la presencia de números
4. WHEN el usuario ingresa una contraseña THEN el sistema SHALL verificar la presencia de caracteres especiales (!@#$%^&*()_+-=[]{}|;:,.<>?)
5. IF la contraseña contiene al menos 3 de los 4 tipos de caracteres THEN el sistema SHALL considerarla "Compleja"
6. IF la contraseña contiene menos de 3 tipos de caracteres THEN el sistema SHALL considerarla "Simple"

### Requirement 3: Detección de Patrones Comunes

**User Story:** Como usuario, quiero que el sistema detecte patrones comunes y predecibles en mi contraseña, para que pueda evitar contraseñas fáciles de adivinar.

#### Acceptance Criteria

1. WHEN el usuario ingresa una contraseña THEN el sistema SHALL verificar si contiene secuencias numéricas comunes (123, 1234, etc.)
2. WHEN el usuario ingresa una contraseña THEN el sistema SHALL verificar si contiene secuencias alfabéticas comunes (abc, abcd, etc.)
3. WHEN el usuario ingresa una contraseña THEN el sistema SHALL verificar si contiene repeticiones de caracteres (aaa, 111, etc.)
4. IF la contraseña contiene patrones comunes THEN el sistema SHALL reducir su puntuación de seguridad
5. IF la contraseña contiene patrones comunes THEN el sistema SHALL informar al usuario sobre los patrones detectados

### Requirement 4: Verificación contra Contraseñas Comunes

**User Story:** Como usuario, quiero que el sistema verifique si mi contraseña está en una lista de contraseñas comúnmente usadas, para que pueda evitar contraseñas vulnerables.

#### Acceptance Criteria

1. WHEN el usuario ingresa una contraseña THEN el sistema SHALL compararla con una lista de contraseñas comunes
2. IF la contraseña coincide con una contraseña común THEN el sistema SHALL clasificarla como "Muy Débil"
3. IF la contraseña coincide con una contraseña común THEN el sistema SHALL advertir al usuario específicamente sobre este problema

### Requirement 5: Verificación de Contraseñas Filtradas (Have I Been Pwned)

**User Story:** Como usuario, quiero que el sistema verifique si mi contraseña ha sido expuesta en filtraciones de datos conocidas, para que pueda evitar usar contraseñas comprometidas.

#### Acceptance Criteria

1. WHEN el usuario ingresa una contraseña THEN el sistema SHALL verificar si ha sido filtrada usando la API de Have I Been Pwned
2. WHEN el sistema consulta la API THEN el sistema SHALL usar el método k-anonymity para proteger la privacidad (solo enviar los primeros 5 caracteres del hash SHA-1)
3. IF la contraseña ha sido encontrada en filtraciones THEN el sistema SHALL clasificarla como "Comprometida"
4. IF la contraseña ha sido encontrada en filtraciones THEN el sistema SHALL mostrar cuántas veces ha sido vista en filtraciones
5. IF la contraseña ha sido encontrada en filtraciones THEN el sistema SHALL recomendar encarecidamente cambiarla
6. IF hay un error de conexión con la API THEN el sistema SHALL continuar con la validación local y notificar que no se pudo verificar filtraciones

### Requirement 6: Documentación y Comentarios en Español

**User Story:** Como desarrollador hispanohablante, quiero que todo el código y comentarios estén en español, para que pueda entender y mantener el código fácilmente.

#### Acceptance Criteria

1. WHEN se escribe código THEN todos los comentarios SHALL estar en español
2. WHEN se escriben docstrings THEN todos los docstrings SHALL estar en español
3. WHEN se definen variables y funciones THEN los nombres SHOULD ser descriptivos y en español cuando sea apropiado
4. WHEN se muestran mensajes al usuario THEN todos los mensajes SHALL estar en español

### Requirement 7: Cálculo de Puntuación y Nivel de Seguridad

**User Story:** Como usuario, quiero recibir una puntuación y clasificación clara de la seguridad de mi contraseña, para que pueda entender fácilmente qué tan segura es.

#### Acceptance Criteria

1. WHEN el sistema evalúa una contraseña THEN el sistema SHALL calcular una puntuación numérica basada en todos los criterios
2. WHEN el sistema calcula la puntuación THEN el sistema SHALL asignar un nivel de seguridad: "Muy Débil", "Débil", "Aceptable", "Fuerte", o "Muy Fuerte"
3. WHEN el sistema presenta los resultados THEN el sistema SHALL mostrar la puntuación, el nivel de seguridad y los criterios cumplidos
4. WHEN el sistema presenta los resultados THEN el sistema SHALL proporcionar sugerencias específicas para mejorar la contraseña

### Requirement 8: Interfaz de Usuario por Línea de Comandos

**User Story:** Como usuario, quiero una interfaz simple de línea de comandos para probar mis contraseñas, para que pueda usar la herramienta fácilmente.

#### Acceptance Criteria

1. WHEN el usuario ejecuta el programa THEN el sistema SHALL solicitar que ingrese una contraseña
2. WHEN el usuario ingresa una contraseña THEN el sistema SHALL ocultar la entrada por seguridad
3. WHEN el sistema completa el análisis THEN el sistema SHALL mostrar los resultados de forma clara y organizada
4. WHEN el sistema muestra los resultados THEN el sistema SHALL preguntar si el usuario desea probar otra contraseña
5. IF el usuario desea continuar THEN el sistema SHALL permitir validar múltiples contraseñas en la misma sesión
