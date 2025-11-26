import os
import re
import msvcrt

from config.db import criar_conexao
from config.crypt import criptografar, checar_password


def insert_user(nome: str, email: str, password: str):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        password = criptografar(password)
        sql = "INSERT INTO funcionarios (nome, email, password) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, email, password))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao inserir usuário: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


email_regex = re.compile(r"^[\w\.\+-]+@[\w\.-]+\.[a-zA-Z]{2,}$")

def email_valido(email: str):
    return email_regex.match(email) is not None


def login(email: str, password: str):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = "SELECT * FROM funcionarios WHERE email=%s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()
        if user and checar_password(password, bytes(user[3])):
            return user
        else:
            return None
    except Exception as e:
        print(f"\nErro ao logar no sistema: {e}\n")
    finally:
        cursor.close()
        conn.close()

def input_senha(prompt="Senha: "):
    print(prompt, end="", flush=True)
    password = ""
    while True:
        char = msvcrt.getch()
        if char in {b"\r", b"\n"}:  # Enter
            print()
            break
        elif char == b"\x08":  # Backspace
            if len(password) > 0:
                password = password[:-1]
                print("\b \b", end="", flush=True)
        else:
            password += char.decode("utf-8")
            print("*", end="", flush=True)
    return password


def delete_user(email):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()     
        sql = "DELETE FROM funcionarios WHERE email=%s"
        cursor.execute(sql, (email,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao deletar usuário: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def pause():
    input("\nAperte ENTER para continuar.")
    os.system("cls")

