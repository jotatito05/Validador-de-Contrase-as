# Validador de Contraseñas Seguras 🔐

Un validador de contraseñas en Python que evalúa la seguridad de tus contraseñas mediante múltiples criterios y verifica si han sido comprometidas en filtraciones de datos.

## Características

✅ **Validación de Longitud**: Evalúa si tu contraseña tiene la longitud adecuada

✅ **Análisis de Complejidad**: Verifica el uso de mayúsculas, minúsculas, números y caracteres especiales

✅ **Detección de Patrones**: Identifica secuencias comunes y repeticiones

✅ **Verificación de Contraseñas Comunes**: Compara contra una lista de 1000 contraseñas más usadas

✅ **Detección de Filtraciones**: Consulta la API de Have I Been Pwned para verificar si tu contraseña ha sido comprometida

✅ **Privacidad Garantizada**: Usa k-anonymity para proteger tu contraseña al consultar APIs externas

## Requisitos

- Python 3.7 o superior
- Conexión a internet (opcional, para verificación de filtraciones)

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/Jotatito05/password-validator.git
cd password-validator
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

Ejecuta el programa desde la línea de comandos:

```bash
python password_checker.py
```

El programa te solicitará que ingreses una contraseña (la entrada estará oculta por seguridad) y te mostrará:

- Puntuación de seguridad (0-100)
- Nivel de seguridad (Muy Débil, Débil, Aceptable, Fuerte, Muy Fuerte)
- Criterios evaluados
- Sugerencias para mejorar tu contraseña

### Ejemplo de Salida

```
==================================================
  VALIDADOR DE CONTRASEÑAS SEGURAS
==================================================

Ingresa la contraseña a validar: ********

⏳ Analizando contraseña...

==================================================
--- RESULTADOS DEL ANÁLISIS ---
==================================================

📊 Puntuación: 85/100
🔒 Nivel de Seguridad: FUERTE

--- CRITERIOS EVALUADOS ---

✓ Longitud: 14 caracteres (20 puntos)
✓ Complejidad: 4 tipos de caracteres (30 puntos)
  - Mayúsculas: Sí
  - Minúsculas: Sí
  - Números: Sí
  - Especiales: Sí
✓ Patrones: Sin patrones detectados (20 puntos)
✓ Contraseña común: No (15 puntos)
✓ Filtrada: No (10 puntos)

==================================================
--- SUGERENCIAS ---
==================================================

✅ ¡Excelente! Tu contraseña cumple con todos los criterios de seguridad.

==================================================
¿Deseas validar otra contraseña? (s/n):
```

## Cómo Funciona

### Sistema de Puntuación

El validador asigna puntos basándose en diferentes criterios:

- **Longitud** (máximo 25 puntos)
  - < 8 caracteres: 0 puntos
  - 8-10 caracteres: 10 puntos
  - 11-12 caracteres: 15 puntos
  - 13-15 caracteres: 20 puntos
  - \> 15 caracteres: 25 puntos

- **Complejidad de caracteres** (máximo 30 puntos)
  - 1 tipo de carácter: 5 puntos
  - 2 tipos de caracteres: 15 puntos
  - 3 tipos de caracteres: 25 puntos
  - 4 tipos de caracteres: 30 puntos

- **Ausencia de patrones comunes** (máximo 20 puntos)
  - Sin patrones: 20 puntos
  - 1 patrón detectado: 10 puntos
  - 2+ patrones detectados: 0 puntos

- **No es contraseña común** (máximo 15 puntos)
  - No está en lista: 15 puntos
  - Está en lista: 0 puntos

- **No ha sido filtrada** (máximo 10 puntos)
  - No filtrada: 10 puntos
  - Filtrada: 0 puntos

### Niveles de Seguridad

- **Muy Débil** (0-30 puntos): Contraseña muy vulnerable
- **Débil** (31-50 puntos): Necesita mejoras significativas
- **Aceptable** (51-70 puntos): Cumple requisitos básicos
- **Fuerte** (71-85 puntos): Buena seguridad
- **Muy Fuerte** (86-100 puntos): Excelente seguridad
- **Comprometida**: Cualquier puntuación si está filtrada

### Privacidad y Seguridad

- Las contraseñas nunca se almacenan
- La verificación de filtraciones usa k-anonymity (solo se envían los primeros 5 caracteres del hash SHA-1)
- Todas las comunicaciones con APIs externas usan HTTPS
- La entrada de contraseñas está oculta en la terminal

## Estructura del Proyecto

```
password-validator/
├── password_checker.py      # Interfaz de línea de comandos
├── validator.py             # Lógica principal de validación
├── hibp_api.py             # Cliente para API de Have I Been Pwned
├── utils.py                # Funciones auxiliares
├── requirements.txt        # Dependencias
├── README.md              # Este archivo
├── LICENSE                # Licencia MIT
├── .gitignore            # Archivos a ignorar en Git
└── resources/
    └── passwords_common.txt # Lista de contraseñas comunes
```

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Agradecimientos

- [Have I Been Pwned](https://haveibeenpwned.com/) por su API de verificación de contraseñas filtradas
- Comunidad de seguridad informática por las mejores prácticas

## Autor

Creado por **Jotatito05** como proyecto educativo para demostrar buenas conocimientos en Python y ciberseguridad.

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub
