# Documento de Diseño - Validador de Contraseñas Seguras

## Overview

El validador de contraseñas es una aplicación de línea de comandos en Python que evalúa la seguridad de contraseñas mediante múltiples criterios: longitud, complejidad de caracteres, detección de patrones comunes, verificación contra listas de contraseñas comunes, y consulta a la API de Have I Been Pwned para detectar contraseñas comprometidas en filtraciones de datos.

El sistema está diseñado para ser modular, extensible y fácil de usar, proporcionando retroalimentación clara y accionable al usuario.

## Architecture

### Arquitectura de Capas

```
┌─────────────────────────────────────┐
│     Capa de Presentación (CLI)     │
│         password_checker.py         │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│      Capa de Lógica de Negocio     │
│         validator.py                │
└─────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌──────────────┐  ┌──────────────────┐
│   Validadores │  │  Servicios       │
│   Específicos │  │  Externos        │
│               │  │                  │
│ - Longitud    │  │ - API HIBP       │
│ - Complejidad │  │ - HTTP Client    │
│ - Patrones    │  │                  │
│ - Comunes     │  │                  │
└──────────────┘  └──────────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │   Recursos   │
                  │              │
                  │ - passwords  │
                  │   _common.txt│
                  └──────────────┘
```

### Principios de Diseño

1. **Separación de Responsabilidades**: Cada módulo tiene una responsabilidad clara y única
2. **Modularidad**: Los validadores son independientes y pueden ser extendidos fácilmente
3. **Privacidad**: Uso de k-anonymity para proteger las contraseñas al consultar APIs externas
4. **Manejo de Errores**: Degradación elegante cuando servicios externos no están disponibles
5. **Internacionalización**: Todo el código, comentarios y mensajes en español

## Components and Interfaces

### 1. Módulo Principal: `password_checker.py`

**Responsabilidad**: Interfaz de usuario por línea de comandos

**Funciones Principales**:
- `main()`: Punto de entrada de la aplicación
- `solicitar_contrasena()`: Obtiene la contraseña del usuario de forma segura
- `mostrar_resultados(resultado)`: Presenta los resultados del análisis
- `mostrar_sugerencias(resultado)`: Muestra recomendaciones de mejora

**Dependencias**:
- `getpass`: Para entrada segura de contraseñas
- `validator.ValidadorContrasena`: Para realizar el análisis

### 2. Módulo de Validación: `validator.py`

**Responsabilidad**: Coordinar todas las validaciones y calcular la puntuación final

**Clase Principal**: `ValidadorContrasena`

```python
class ValidadorContrasena:
    """
    Coordina todas las validaciones de contraseña y calcula la puntuación final.
    """
    
    def validar(self, contrasena: str) -> dict:
        """
        Valida una contraseña contra todos los criterios.
        
        Args:
            contrasena: La contraseña a validar
            
        Returns:
            dict con estructura:
            {
                'puntuacion': int (0-100),
                'nivel': str ('Muy Débil', 'Débil', 'Aceptable', 'Fuerte', 'Muy Fuerte'),
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
```

**Métodos Privados**:
- `_validar_longitud(contrasena)`: Valida la longitud
- `_validar_complejidad(contrasena)`: Valida tipos de caracteres
- `_detectar_patrones(contrasena)`: Detecta patrones comunes
- `_verificar_contrasena_comun(contrasena)`: Verifica contra lista local
- `_calcular_puntuacion(criterios)`: Calcula puntuación final
- `_determinar_nivel(puntuacion)`: Determina el nivel de seguridad
- `_generar_sugerencias(criterios)`: Genera recomendaciones

### 3. Módulo de API: `hibp_api.py`

**Responsabilidad**: Interactuar con la API de Have I Been Pwned

**Clase Principal**: `HIBPChecker`

```python
class HIBPChecker:
    """
    Cliente para la API de Have I Been Pwned usando k-anonymity.
    """
    
    API_URL = "https://api.pwnedpasswords.com/range/"
    
    def verificar_contrasena(self, contrasena: str) -> dict:
        """
        Verifica si una contraseña ha sido filtrada.
        
        Args:
            contrasena: La contraseña a verificar
            
        Returns:
            dict con estructura:
            {
                'filtrada': bool,
                'veces_vista': int,
                'error': str | None
            }
        """
```

**Métodos Privados**:
- `_generar_hash_sha1(contrasena)`: Genera hash SHA-1
- `_consultar_api(prefijo_hash)`: Consulta la API con los primeros 5 caracteres
- `_buscar_sufijo(sufijo, respuesta)`: Busca el sufijo en la respuesta

### 4. Módulo de Utilidades: `utils.py`

**Responsabilidad**: Funciones auxiliares reutilizables

**Funciones**:
- `cargar_contrasenas_comunes()`: Carga la lista de contraseñas comunes
- `tiene_mayusculas(texto)`: Verifica presencia de mayúsculas
- `tiene_minusculas(texto)`: Verifica presencia de minúsculas
- `tiene_numeros(texto)`: Verifica presencia de números
- `tiene_caracteres_especiales(texto)`: Verifica presencia de caracteres especiales
- `detectar_secuencia_numerica(texto)`: Detecta secuencias como 123, 1234
- `detectar_secuencia_alfabetica(texto)`: Detecta secuencias como abc, abcd
- `detectar_repeticiones(texto)`: Detecta repeticiones como aaa, 111

## Data Models

### Resultado de Validación

```python
{
    'puntuacion': 75,  # 0-100
    'nivel': 'Fuerte',  # 'Muy Débil' | 'Débil' | 'Aceptable' | 'Fuerte' | 'Muy Fuerte'
    'criterios': {
        'longitud': {
            'valor': 14,
            'cumple': True,
            'puntos': 20
        },
        'complejidad': {
            'mayusculas': True,
            'minusculas': True,
            'numeros': True,
            'especiales': True,
            'tipos_usados': 4,
            'cumple': True,
            'puntos': 25
        },
        'patrones': {
            'secuencias_numericas': False,
            'secuencias_alfabeticas': False,
            'repeticiones': False,
            'cumple': True,
            'puntos': 15
        },
        'comun': False,  # True si está en lista de contraseñas comunes
        'filtrada': {
            'encontrada': False,
            'veces_vista': 0,
            'error': None
        }
    },
    'sugerencias': [
        'Excelente: Tu contraseña cumple con todos los criterios de seguridad'
    ]
}
```

### Sistema de Puntuación

- **Longitud** (máximo 25 puntos):
  - < 8 caracteres: 0 puntos
  - 8-10 caracteres: 10 puntos
  - 11-12 caracteres: 15 puntos
  - 13-15 caracteres: 20 puntos
  - > 15 caracteres: 25 puntos

- **Complejidad** (máximo 30 puntos):
  - 1 tipo de carácter: 5 puntos
  - 2 tipos de caracteres: 15 puntos
  - 3 tipos de caracteres: 25 puntos
  - 4 tipos de caracteres: 30 puntos

- **Sin Patrones Comunes** (máximo 20 puntos):
  - Sin patrones: 20 puntos
  - 1 patrón detectado: 10 puntos
  - 2+ patrones detectados: 0 puntos

- **No es Contraseña Común** (máximo 15 puntos):
  - No está en lista: 15 puntos
  - Está en lista: 0 puntos (y nivel automático "Muy Débil")

- **No Filtrada** (máximo 10 puntos):
  - No filtrada: 10 puntos
  - Filtrada 1-100 veces: 0 puntos (nivel "Comprometida")
  - Filtrada 100+ veces: 0 puntos (nivel "Muy Comprometida")

### Niveles de Seguridad

- **Muy Débil**: 0-30 puntos o contraseña común
- **Débil**: 31-50 puntos
- **Aceptable**: 51-70 puntos
- **Fuerte**: 71-85 puntos
- **Muy Fuerte**: 86-100 puntos
- **Comprometida**: Cualquier puntuación si está filtrada

## Error Handling

### Estrategia General

1. **Errores de Red**: Si la API de HIBP no está disponible, continuar con validación local
2. **Errores de Entrada**: Validar que la contraseña no esté vacía
3. **Errores de Archivo**: Si no se puede cargar la lista de contraseñas comunes, continuar sin esa validación
4. **Timeouts**: Establecer timeout de 5 segundos para llamadas a API

### Manejo Específico por Módulo

**validator.py**:
```python
try:
    resultado_hibp = self.hibp_checker.verificar_contrasena(contrasena)
except Exception as e:
    # Continuar sin verificación de filtraciones
    resultado_hibp = {
        'filtrada': False,
        'veces_vista': 0,
        'error': f'No se pudo verificar filtraciones: {str(e)}'
    }
```

**hibp_api.py**:
```python
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
except requests.Timeout:
    return {'filtrada': False, 'veces_vista': 0, 'error': 'Timeout al consultar API'}
except requests.RequestException as e:
    return {'filtrada': False, 'veces_vista': 0, 'error': str(e)}
```

## Testing Strategy

### Pruebas Unitarias

**test_validator.py**:
- Probar cada método de validación individualmente
- Casos de borde: contraseñas vacías, muy largas, caracteres especiales
- Verificar cálculo correcto de puntuación
- Verificar generación de sugerencias apropiadas

**test_hibp_api.py**:
- Probar generación correcta de hash SHA-1
- Probar parsing de respuesta de API
- Probar manejo de errores de red
- Usar mocks para evitar llamadas reales a la API

**test_utils.py**:
- Probar cada función de detección de patrones
- Casos de borde para secuencias y repeticiones
- Verificar detección correcta de tipos de caracteres

### Pruebas de Integración

**test_integration.py**:
- Probar flujo completo de validación
- Verificar que todos los módulos se integran correctamente
- Probar con contraseñas reales conocidas (débiles y fuertes)

### Pruebas Manuales

- Probar la interfaz CLI con diferentes entradas
- Verificar que la entrada de contraseña esté oculta
- Verificar formato y claridad de los mensajes de salida
- Probar el flujo de múltiples validaciones consecutivas

## Implementation Notes

### Dependencias Externas

```
requests>=2.31.0  # Para llamadas HTTP a la API
```

### Estructura de Archivos

```
password-validator/
├── README.md
├── requirements.txt
├── password_checker.py      # Punto de entrada
├── validator.py             # Lógica principal de validación
├── hibp_api.py             # Cliente API HIBP
├── utils.py                # Funciones auxiliares
├── resources/
│   └── passwords_common.txt # Lista de contraseñas comunes
└── tests/
    ├── test_validator.py
    ├── test_hibp_api.py
    ├── test_utils.py
    └── test_integration.py
```

### Lista de Contraseñas Comunes

Incluir las 1000 contraseñas más comunes (basadas en listas públicas como RockYou). Ejemplos:
- password
- 123456
- qwerty
- admin
- letmein
- etc.

### Consideraciones de Seguridad

1. **No almacenar contraseñas**: Las contraseñas solo existen en memoria durante la validación
2. **K-anonymity**: Solo enviar los primeros 5 caracteres del hash a HIBP
3. **HTTPS**: Todas las llamadas a API deben usar HTTPS
4. **Entrada oculta**: Usar `getpass` para ocultar la contraseña al escribirla

### Mejoras Futuras

1. Soporte para verificación de múltiples contraseñas desde archivo
2. Generador de contraseñas seguras
3. Exportación de resultados a JSON/CSV
4. Interfaz gráfica (GUI)
5. API REST para integración con otros sistemas
