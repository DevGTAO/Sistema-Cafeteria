import getpass
import os

from services.user_services import insert_user, email_valido, login, input_senha, delete_user, pause
from view.admin_view import panel_admin

while True:
    print("###    PÁGINA INICIAL    ###")
    print("\n1 - Cadastrar conta\n2 - Entrar\n3 - Remover conta\n0 - Sair do sistema")
    opcao = int(input("\nDigite a opção: "))

    if opcao == 1:
        nome = input("\nDigite seu nome: ")
        email = input("Digite seu email: ")
        
        if not email_valido(email):
            print("\nE-mail em formato inválido!")
            pause()
            continue

        password = input("Digite sua senha: ")  

        if insert_user(nome, email, password):
            print("\nUsuário cadastrado com sucesso!")
        else:
            print("Esse e-mail já está sendo usado.")
        pause()

    elif opcao == 2:
        email = input("\nDigite seu email: ")
        password = input_senha()
        user_auth = login(email, password)
        if user_auth:
            print("\nUsuário logado!")
            pause()
            panel_admin(user_auth)
        else:
            print("\nUsuário ou senha incorretos!")
            pause()

    elif opcao == 3:
        email = input("\nDigite o email da conta que deseja excluir: ")
        password = getpass.getpass("Digite a senha da conta que deseja excluir: ")
        
        user_auth = login(email, password)
        
        if user_auth:
            if delete_user(email):
                print("\nUsuário excluído com sucesso!")
            else:
                print("\nNão foi possível excluir o usuário.")
            pause()
        else:
            print("Usuário ou senha incorretos!")
            pause()

    elif opcao == 0:
        os.system("cls")
        break
    else:
        print("Digite uma opção válida!")
