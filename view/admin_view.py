import os

from services.order_services import fazer_pedido, listar_cardapio, cardapio, mostrar_pedidos, remover_pedido, atualizar_pedido
from services.user_services import pause

def panel_admin(user_auth):
    while True:
        # os.system("cls")
        print("###    MENU ADMIN    ###")
        print(f"\nBem-vindo: {user_auth[1]}\n")
        print("1 - Fazer pedido\n2 - Listar pedido\n3 - Remover pedido\n4 - Atualizar pedido\n5 - Adicionar itens ao cardápio\n6 - Listar cardápio\n0 - Deslogar")
        opcao = int(input("\nDigite uma opção: "))
        os.system("cls")

        if opcao == 1:
            fazer_pedido()
            pause()
        elif opcao == 2:
            mostrar_pedidos()
            pause()
        elif opcao == 3:
            remover_pedido()
            pause()
        elif opcao == 4:
            atualizar_pedido()
            pause()
        elif opcao == 5:
            cardapio()
            pause()
        elif opcao == 6:
            listar_cardapio()
            pause()
        elif opcao == 0:
            break
        else:
            print("Digite uma opção válida!")