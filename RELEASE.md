# Generación de Releases

Este proyecto usa GitHub Actions para generar automáticamente paquetes de instalación multiplataforma.

## Formatos generados

- **Linux**:
  - `.deb` - Paquete Debian/Ubuntu
  - `.rpm` - Paquete Red Hat/Fedora/CentOS
  - `.tar.gz` - Archivo genérico para cualquier distribución

- **Windows**:
  - `.exe` - Instalador con Inno Setup

- **macOS**:
  - `.dmg` - Imagen de disco para macOS

## Cómo crear un release

### Método automático (recomendado)

1. Actualiza la versión en `src/version.txt`
2. Commit y push de los cambios
3. Crea y publica un tag de versión:
   ```bash
   git tag v2.0
   git push origin v2.0
   ```
4. GitHub Actions generará automáticamente todos los paquetes y creará un release

### Método manual

Ejecuta el workflow manualmente desde GitHub:
1. Ve a la pestaña "Actions" en GitHub
2. Selecciona "Build Release"
3. Haz clic en "Run workflow"
4. Los artefactos estarán disponibles en la ejecución del workflow

## Build local

### Requisitos

```bash
pip install pyinstaller
```

### Linux

```bash
# Generar ejecutable
pyinstaller betcon.spec

# El ejecutable estará en dist/betcon/betcon
./dist/betcon/betcon

# Generar .tar.gz
cd dist
tar -czf betcon-$(cat ../src/version.txt)-linux-x86_64.tar.gz betcon/
```

### Windows

```powershell
# Generar ejecutable
pyinstaller betcon.spec

# El ejecutable estará en dist\betcon\betcon.exe
.\dist\betcon\betcon.exe
```

### macOS

```bash
# Generar app bundle
pyinstaller betcon.spec

# La aplicación estará en dist/betcon.app
open dist/betcon.app
```

## Estructura del paquete

Los paquetes incluyen:
- Ejecutable de la aplicación
- Assets (iconos, hojas de estilo)
- Traducciones
- Archivos UI
- Base de datos SQL por defecto
- Recursos (imágenes de deportes y casas de apuestas)

## Notas técnicas

- **PyInstaller**: Se usa para empaquetar Python + PySide6 en un ejecutable standalone
- **Inno Setup** (Windows): Crea instaladores con asistente gráfico
- **dmgbuild** (macOS): Genera imágenes de disco .dmg
- **dpkg-deb** (Linux): Crea paquetes .deb
- **rpmbuild** (Linux): Crea paquetes .rpm

## Solución de problemas

### Error: "module not found"
Asegúrate de que todas las dependencias están en `hiddenimports` en `betcon.spec`

### Error: "file not found" en runtime
Verifica que todos los archivos necesarios estén en `datas` en `betcon.spec`

### El ejecutable es muy grande
PyInstaller incluye todo el intérprete de Python. Para reducir el tamaño:
- Revisa `excludes` en `betcon.spec` para excluir módulos innecesarios
- Activa UPX compression (ya activado por defecto)
