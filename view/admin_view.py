import os

from services.order_services import fazer_pedido, cardapio
from services.user_services import pause

def panel_admin(user_auth):
    while True:
        # os.system("cls")
        print("###    MENU    ###")
        print(f"\nBem-vindo: {user_auth[1]}\n")
        print("1 - Fazer pedido\n2 - Listar pedido\n3 - Remover pedido\n4 - Atualizar pedido\n5 - Deslogar")
        opcao = int(input("\nDigite uma opção: "))
        os.system("cls")

        if opcao == 1:
            cardapio()
            pause()
        elif opcao == 2:
            pass
        elif opcao == 3:
            pass
        elif opcao == 4:
            pass
        elif opcao == 5:
            break
        else:
            print("Digite uma opção válida!")