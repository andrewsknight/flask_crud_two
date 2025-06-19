import os

def crear_estructura_proyecto():
    """Crear la estructura de directorios y archivos __init__.py"""
    
    # Directorios a crear
    directorios = [
        'config',
        'models', 
        'controllers',
        'routes',
        'services',
        'ddbb'
    ]
    
    print("📁 Creando estructura de directorios...")
    
    for directorio in directorios:
        # Crear directorio si no existe
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"✅ Directorio creado: {directorio}/")
        
        # Crear archivo __init__.py
        init_file = os.path.join(directorio, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write(f'"""\n{directorio.title()} module\n"""\n')
            print(f"✅ Archivo creado: {init_file}")
    
    print("\n🎉 Estructura de proyecto creada correctamente!")

if __name__ == "__main__":
    crear_estructura_proyecto()