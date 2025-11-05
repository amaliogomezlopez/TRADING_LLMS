"""
Script para gestionar logs del trading bot
Permite hacer backup, archivar y limpiar logs
"""
import os
import shutil
from datetime import datetime

LOG_FILE = 'trading_log.csv'
BACKUP_DIR = 'logs_backup'

def create_backup(archive=False):
    """Crea un backup del log actual."""
    if not os.path.exists(LOG_FILE):
        print(f"❌ No se encontró {LOG_FILE}")
        return None
    
    # Crear directorio de backup si no existe
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"✓ Creado directorio {BACKUP_DIR}/")
    
    # Nombre del archivo de backup con timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(BACKUP_DIR, f'trading_log_{timestamp}.csv')
    
    # Copiar el archivo
    shutil.copy2(LOG_FILE, backup_file)
    print(f"✅ Backup creado: {backup_file}")
    
    # Obtener tamaño del archivo
    size = os.path.getsize(backup_file)
    print(f"   Tamaño: {size:,} bytes ({size/1024:.2f} KB)")
    
    # Contar líneas
    with open(backup_file, 'r') as f:
        lines = sum(1 for _ in f) - 1  # -1 para el header
    print(f"   Registros: {lines:,}")
    
    if archive:
        # Vaciar el log actual (mantener solo el header)
        with open(LOG_FILE, 'r') as f:
            header = f.readline()
        
        with open(LOG_FILE, 'w') as f:
            f.write(header)
        
        print(f"✅ Log actual limpiado (backup guardado)")
    
    return backup_file

def list_backups():
    """Lista todos los backups disponibles."""
    if not os.path.exists(BACKUP_DIR):
        print(f"❌ No hay backups todavía")
        return []
    
    backups = [f for f in os.listdir(BACKUP_DIR) if f.endswith('.csv')]
    
    if not backups:
        print(f"❌ No hay backups en {BACKUP_DIR}/")
        return []
    
    print(f"\n📁 BACKUPS DISPONIBLES ({len(backups)}):")
    print("=" * 70)
    
    backup_info = []
    for backup in sorted(backups, reverse=True):
        path = os.path.join(BACKUP_DIR, backup)
        size = os.path.getsize(path)
        mod_time = datetime.fromtimestamp(os.path.getmtime(path))
        
        with open(path, 'r') as f:
            lines = sum(1 for _ in f) - 1
        
        print(f"📄 {backup}")
        print(f"   Fecha: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Tamaño: {size:,} bytes ({size/1024:.2f} KB)")
        print(f"   Registros: {lines:,}")
        print()
        
        backup_info.append({
            'file': backup,
            'path': path,
            'size': size,
            'records': lines,
            'date': mod_time
        })
    
    return backup_info

def restore_backup(backup_file):
    """Restaura un backup específico."""
    backup_path = os.path.join(BACKUP_DIR, backup_file)
    
    if not os.path.exists(backup_path):
        print(f"❌ Backup no encontrado: {backup_file}")
        return False
    
    # Hacer backup del actual antes de restaurar
    if os.path.exists(LOG_FILE):
        temp_backup = create_backup()
        print(f"⚠️ Log actual guardado como backup de seguridad")
    
    # Restaurar
    shutil.copy2(backup_path, LOG_FILE)
    print(f"✅ Log restaurado desde: {backup_file}")
    
    return True

def clean_log(confirm=False):
    """Limpia el log actual (hace backup primero)."""
    if not os.path.exists(LOG_FILE):
        print(f"❌ No se encontró {LOG_FILE}")
        return
    
    if not confirm:
        print("⚠️ ADVERTENCIA: Esto creará un backup y limpiará el log actual.")
        response = input("¿Continuar? (sí/no): ").strip().lower()
        if response not in ['sí', 'si', 's', 'yes', 'y']:
            print("❌ Operación cancelada")
            return
    
    # Crear backup antes de limpiar
    backup_file = create_backup(archive=True)
    print(f"\n✅ Log limpiado exitosamente")
    print(f"   Backup guardado en: {backup_file}")

def show_current_log_info():
    """Muestra información del log actual."""
    if not os.path.exists(LOG_FILE):
        print(f"❌ No se encontró {LOG_FILE}")
        return
    
    size = os.path.getsize(LOG_FILE)
    mod_time = datetime.fromtimestamp(os.path.getmtime(LOG_FILE))
    
    with open(LOG_FILE, 'r') as f:
        lines = sum(1 for _ in f) - 1
    
    print(f"\n📊 LOG ACTUAL:")
    print("=" * 70)
    print(f"📄 Archivo: {LOG_FILE}")
    print(f"📅 Última modificación: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📦 Tamaño: {size:,} bytes ({size/1024:.2f} KB)")
    print(f"📝 Registros: {lines:,}")
    
    if lines > 0:
        # Leer primera y última línea de datos
        import pandas as pd
        df = pd.read_csv(LOG_FILE)
        
        if len(df) > 0:
            print(f"🕐 Primer registro: {df['Timestamp'].iloc[0]}")
            print(f"🕐 Último registro: {df['Timestamp'].iloc[-1]}")
            
            if 'Total_PNL' in df.columns:
                latest_pnl = df['Total_PNL'].iloc[-1]
                if pd.notna(latest_pnl):
                    print(f"💰 P&L Total: ${latest_pnl:.2f}")

def main():
    """Menú interactivo."""
    print("=" * 70)
    print("🗂️  GESTOR DE LOGS - TRADING BOT")
    print("=" * 70)
    
    while True:
        print("\n📋 OPCIONES:")
        print("1. Ver información del log actual")
        print("2. Crear backup del log actual")
        print("3. Crear backup y limpiar log (empezar nuevo ciclo)")
        print("4. Listar todos los backups")
        print("5. Restaurar un backup")
        print("0. Salir")
        
        choice = input("\nSelecciona una opción (0-5): ").strip()
        
        if choice == '0':
            print("👋 Adiós!")
            break
        elif choice == '1':
            show_current_log_info()
        elif choice == '2':
            create_backup(archive=False)
        elif choice == '3':
            clean_log(confirm=False)
        elif choice == '4':
            list_backups()
        elif choice == '5':
            backups = list_backups()
            if backups:
                backup_name = input("\nNombre del backup a restaurar: ").strip()
                restore_backup(backup_name)
        else:
            print("❌ Opción inválida")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'info':
            show_current_log_info()
        elif command == 'backup':
            create_backup(archive=False)
        elif command == 'clean':
            clean_log(confirm=True)
        elif command == 'list':
            list_backups()
        else:
            print(f"❌ Comando desconocido: {command}")
            print("\nComandos disponibles:")
            print("  python manage_logs.py info    - Info del log actual")
            print("  python manage_logs.py backup  - Crear backup")
            print("  python manage_logs.py clean   - Backup y limpiar")
            print("  python manage_logs.py list    - Listar backups")
    else:
        main()
