from .user_services import criar_conexao


def fazer_pedido(cliente_id, preco_total):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = "INSERT INTO pedidos (id_cliente, preco_total) VALUES (%s, %s)"
        cursor.execute(sql, [cliente_id, preco_total])
        conn.commit()
        print("Pedido realizado!")
    except Exception as e:
        print(f"Erro ao realizar pedido: {e}")
        return False
    finally:
        cursor.close()
        conn.close()


def cardapio():
    print("###    CARDÁPIO    ###")
    print("\nSalgados\n1 - Croissant(Frango) - R$12,00\n2 - Diplomata(Misto) - R$8,00\n3 - Coxinha(Frango c/catupiry) - R$7,50")
    print("\nDoces\n4 - Tortelete - R$4,00\n5 - Brigadeiro - R$2,50\n6 - Torta(Maçã) - R$6,00")
    print("\nBebidas\n7 - Água - R$3,00\n8 - Capuccino - R$6,50\n9 - Xícara de Café - R$5,00")