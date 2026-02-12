# Changelog

All notable changes to this project will be documented in this file. / Todos los cambios notables en este proyecto serán documentados en este archivo.

## [1.0.0] - 2026-02-12

### English

#### Added
- **Architecture**: Reorganized codebase into logical subpackages (`core`, `io`, `validation`, `analysis`, `internals`, `tooling`) to improve maintainability and navigation.
- **Tooling**: Added `simuci.envcheck` (via `python -m simuci.envcheck`) for verifying environment health, dependencies, and optional security auditing (via `pip-audit`).
- **Security**: Added `security` optional dependency group in `pyproject.toml`.
- **Documentation**: Added `ARCHITECTURE.md` (and ES variant) to explain the new modular structure. Added `README.es.md` for Spanish documentation.
- **Documentation Directory**: Created `docs/` with index and moved architecture docs there for better organization.
- **GitHub Configuration**: Added Copilot instructions and Skills definitions for better AI assistance.

#### Changed
- **Internal API**: Moved modules from root `simuci.*` to specific subpackages (e.g., `simuci.stats` → `simuci.analysis.stats`).
- **Imports**: Updated all internal imports to reflect the new structure.
- **Stats**: Made `scipy.stats.PermutationMethod` import conditional to support older SciPy versions without crashing.
- **Version**: Bumped to 1.0.0 as stable release.

#### Fixed
- **Import Issues**: Resolved potential crashes from missing SciPy features.
- **Type Hints**: Added missing docstrings in `envcheck.py`.

### Español

#### Agregado
- **Arquitectura**: Reorganizado el código base en subpaquetes lógicos (`core`, `io`, `validation`, `analysis`, `internals`, `tooling`) para mejorar la mantenibilidad y navegación.
- **Herramientas**: Agregado `simuci.envcheck` (via `python -m simuci.envcheck`) para verificar la salud del entorno, dependencias y auditoría de seguridad opcional (via `pip-audit`).
- **Seguridad**: Agregado grupo de dependencias opcionales `security` en `pyproject.toml`.
- **Documentación**: Agregado `ARCHITECTURE.md` (y variante ES) para explicar la nueva estructura modular. Agregado `README.es.md` para documentación en español.
- **Directorio de Documentación**: Creado `docs/` con índice y movidos documentos de arquitectura allí para mejor organización.
- **Configuración de GitHub**: Agregadas instrucciones de Copilot y definiciones de Skills para mejor asistencia de IA.

#### Cambiado
- **API Interna**: Movidos módulos desde raíz `simuci.*` a subpaquetes específicos (e.g., `simuci.stats` → `simuci.analysis.stats`).
- **Importaciones**: Actualizadas todas las importaciones internas para reflejar la nueva estructura.
- **Estadísticas**: Hecho condicional la importación de `scipy.stats.PermutationMethod` para soportar versiones antiguas de SciPy sin fallar.
- **Versión**: Incrementada a 1.0.0 como lanzamiento estable.

#### Corregido
- **Problemas de Importación**: Resueltos posibles fallos por características faltantes en SciPy.
- **Indicaciones de Tipo**: Agregadas docstrings faltantes en `envcheck.py`.

## [Unreleased]
- **Compatibility**: Ensure `anderson_ksamp` works gracefully even if `PermutationMethod` is unavailable in the installed SciPy version.

---

### Español

#### Agregado
- **Arquitectura**: Reorganización del código base en subpaquetes lógicos (`core`, `io`, `validation`, `analysis`, `internals`, `tooling`) para mejorar mantenibilidad y navegación.
- **Herramientas**: Añadido `simuci.envcheck` (vía `python -m simuci.envcheck`) para verificar salud del entorno, dependencias y auditoría de seguridad opcional (vía `pip-audit`).
- **Seguridad**: Añadido grupo de dependencias opcional `security` en `pyproject.toml`.
- **Documentación**: Añadido `ARCHITECTURE.md` (y variante ES) para explicar la nueva estructura modular. Añadido `README.es.md` con documentación en español.

#### Cambiado
- **API Interna**: Módulos movidos desde la raíz `simuci.*` a subpaquetes específicos (ej. `simuci.stats` → `simuci.analysis.stats`).
- **Imports**: Actualizados todos los imports internos para reflejar la nueva estructura.
- **Stats**: La importación de `scipy.stats.PermutationMethod` ahora es condicional para soportar versiones antiguas de SciPy sin errores.

#### Arreglado
- **Compatibilidad**: Asegurado que `anderson_ksamp` funcione correctamente incluso si `PermutationMethod` no está disponible en la versión instalada de SciPy.
