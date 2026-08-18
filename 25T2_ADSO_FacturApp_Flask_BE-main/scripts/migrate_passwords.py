"""
SCRIPT DE MIGRACIÓN DE CONTRASEÑAS
====================================

Este script convierte las contraseñas existentes en texto plano
a hashes seguros utilizando werkzeug.security (pbkdf2:sha256).

IMPORTANTE:
- Ejecutar UNA SOLA VEZ antes de activar la autenticación JWT.
- Hacer respaldo de la tabla 'usuarios' antes de ejecutar.
- El script es idempotente: si una password ya tiene hash, la omite.

CÓMO EJECUTAR:
    cd 25T2_ADSO_FacturApp_Flask_BE-main
    python -m scripts.migrate_passwords

ANTES DE EJECUTAR:
    1. Respaldar la tabla:
       mysqldump -u root FacturApp_25T2_PY usuarios > backup_usuarios.sql

    2. Verificar contraseñas actuales:
       python -c "from src.models import session; from src.models.usuarios import Usuarios; [print(f'{u.usuario}: {u.password}') for u in session.query(Usuarios).all()]"

    3. Ejecutar el script:
       python -m scripts.migrate_passwords

    4. Verificar después de ejecutar:
       python -c "from src.models import session; from src.models.usuarios import Usuarios; [print(f'{u.usuario}: {u.password[:40]}...') for u in session.query(Usuarios).all()]"
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import session
from src.models.usuarios import Usuarios
from werkzeug.security import generate_password_hash, check_password_hash


HASH_PREFIXES = ("scrypt:", "pbkdf2:", "argon2:", "plaintext:")


def _is_hashed(password: str) -> bool:
    return any(password.startswith(p) for p in HASH_PREFIXES)


def migrate_passwords():
    usuarios = session.query(Usuarios).all()

    migrados = 0
    omitidos = 0
    errores = 0

    print(f"Total de usuarios encontrados: {len(usuarios)}")
    print("-" * 50)

    for usuario in usuarios:
        try:
            if _is_hashed(usuario.password):
                print(f"  OMITIDO  | {usuario.usuario} | Ya tiene hash")
                omitidos += 1
                continue

            password_plano = usuario.password
            usuario.password = generate_password_hash(password_plano)
            session.commit()

            print(f"  MIGRADO  | {usuario.usuario} | Texto plano -> Hash")
            migrados += 1

        except Exception as e:
            session.rollback()
            print(f"  ERROR    | {usuario.usuario} | {str(e)}")
            errores += 1

    print("-" * 50)
    print(f"Resultado: {migrados} migrados, {omitidos} omitidos, {errores} errores")

    if errores > 0:
        print("\nADVERTENCIA: Hubo errores. Revisar la base de datos.")
        return False

    if migrados > 0:
        print("\nMigración completada. Ahora puedes iniciar el servidor con JWT.")
    else:
        print("\nNo hubo cambios. Todas las contraseñas ya estaban hasheadas.")

    return True


if __name__ == '__main__':
    print("========================================")
    print(" MIGRACIÓN DE CONTRASEÑAS A HASH")
    print("========================================")
    print()

    respuesta = input("¿Deseas continuar? (s/n): ")
    if respuesta.lower() != 's':
        print("Migración cancelada.")
        sys.exit(0)

    print()
    success = migrate_passwords()
    sys.exit(0 if success else 1)
