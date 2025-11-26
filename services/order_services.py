from .user_services import criar_conexao


def criar_cliente(nome: str) -> int | None:
    """Cria um cliente só com nome e retorna o id."""
    conn = criar_conexao()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO clientes (nome) VALUES (%s) RETURNING id;"
        cursor.execute(sql, (nome,))
        cliente_id = cursor.fetchone()[0]
        conn.commit()
        return cliente_id
    except Exception as e:
        print(f"Erro ao criar cliente: {e}")
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()



def cardapio():
    print("\n=== Cadastro de Cardápio ===")
    print("Digite 'sair' no nome do item para encerrar.\n")

    while True:
        nome_item = input("Nome do item: ")

        if nome_item.strip().lower() == "sair":
            print("\nCadastro encerrado.")
            break

        try:
            preco_item = float(input("Valor do item (R$): ").replace(",", "."))
        except ValueError:
            print("Valor inválido, tente novamente.\n")
            continue

        try:
            conn = criar_conexao()
            cursor = conn.cursor()
            sql = "INSERT INTO cardapio (nome_item, preco_item) VALUES (%s, %s)"
            cursor.execute(sql, (nome_item, preco_item))
            conn.commit()
            print("Item adicionado!\n")
        except Exception as e:
            print(f"Erro ao cadastrar item: {e}")
        finally:
            cursor.close()
            conn.close()


def listar_cardapio():
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = "SELECT * FROM cardapio"
        cursor.execute(sql)
        itens = cursor.fetchall()
        
        print("\n--- CARDÀPIO ---")
        for item in itens:
            print(f"ID: {item[0]} | {item[1]} - R${item[2]:.2f}")

        return itens
    except Exception as e:
        print("Erro ao listar cardápio: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def buscar_item_por_id(item_id: int):
    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        sql = "SELECT id_item, nome_item, preco_item FROM cardapio WHERE id_item = %s"
        cursor.execute(sql, (item_id,))
        return cursor.fetchone()  # None se não existir
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def fazer_pedido():
    try:
        nome_cliente = input("Digite o nome do cliente: ").strip()
        if not nome_cliente:
            print("Nome não pode ser vazio.")
            return False

        cliente_id = criar_cliente(nome_cliente)
        if not cliente_id:
            print("Não foi possível criar o cliente.")
            return False

        listar_cardapio()

        print("\nDigite o ID dos itens que o cliente deseja.")
        print("Digite 0 para finalizar o pedido.\n")

        itens_escolhidos = []  # lista de tuplas (id_item, nome, preco, qtd)
        preco_total = 0.0

        while True:
            try:
                item_id = int(input("ID do item (0 para finalizar): "))
            except ValueError:
                print("Valor inválido, digite um número.")
                continue

            if item_id == 0:
                break

            item = buscar_item_por_id(item_id)
            if not item:
                print("Item não encontrado. Tente novamente.")
                continue

            try:
                qtd = int(input("Quantidade: "))
            except ValueError:
                print("Quantidade inválida, usando 1.")
                qtd = 1

            itens_escolhidos.append((item[0], item[1], float(item[2]), qtd))
            preco_total += float(item[2]) * qtd

            print(f"Adicionado: {item[1]} x{qtd} - R${float(item[2])*qtd:.2f}")
            print(f"Total parcial: R${preco_total:.2f}\n")

        if not itens_escolhidos:
            print("Nenhum item selecionado. Pedido cancelado.")
            return False

        print("\n--- RESUMO DO PEDIDO ---")
        for _, nome, preco, qtd in itens_escolhidos:
            print(f"{nome} x{qtd} - R${preco*qtd:.2f}")
        print(f"TOTAL: R${preco_total:.2f}")

        confirmar = input("Confirmar pedido? (s/n): ").strip().lower()
        if confirmar != "s":
            print("Pedido cancelado.")
            return False

        conn = criar_conexao()
        cursor = conn.cursor()

        sql_pedido = "INSERT INTO pedidos (id_cliente, preco_total) VALUES (%s, %s) RETURNING id;"
        cursor.execute(sql_pedido, (cliente_id, preco_total))
        id_pedido = cursor.fetchone()[0]

        sql_item = """
            INSERT INTO itens_pedido (id_pedido, id_item, quantidade)
            VALUES (%s, %s, %s)
        """
        for id_item, _, _, qtd in itens_escolhidos:
            cursor.execute(sql_item, (id_pedido, id_item, qtd))

        conn.commit()
        print("\nPedido realizado com sucesso!")
        return True

    except Exception as e:
        print(f"Erro ao realizar pedido: {e}")
        return False

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


def listar_pedidos_com_cliente():
    conn = criar_conexao()
    cursor = conn.cursor()
    try:
        sql = """
            SELECT
                p.id,
                c.nome,
                p.preco_total,
                p.created_at
            FROM pedidos p
            INNER JOIN clientes c
                ON p.id_cliente = c.id
            ORDER BY p.created_at DESC;
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar pedidos: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def mostrar_pedidos():
    pedidos = listar_pedidos_com_cliente()
    print("\n=== PEDIDOS ===")
    for p in pedidos:
        id_pedido, nome_cliente, total, data = p
        print(f"Pedido #{id_pedido} | Cliente: {nome_cliente} "
              f"| Total: R${total:.2f} | Data: {data}")
        

def remover_pedido():
    try:
        id_pedido = int(input("Digite o ID do pedido que deseja remover: "))
    except ValueError:
        print("ID inválido.")
        return

    conn = criar_conexao()
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM pedidos WHERE id = %s"
        cursor.execute(sql, (id_pedido,))
        if cursor.rowcount == 0:
            print("Pedido não encontrado.")
        else:
            conn.commit()
            print("Pedido removido com sucesso.")
    except Exception as e:
        print(f"Erro ao remover pedido: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def atualizar_pedido():
    try:
        mostrar_pedidos()
        id_pedido = int(input("Digite o ID do pedido: "))
    except ValueError:
        print("ID inválido.")
        return

    conn = criar_conexao()
    cursor = conn.cursor()
    try:
        # conferir se existe
        cursor.execute("SELECT id_cliente, preco_total FROM pedidos WHERE id = %s", (id_pedido,))
        pedido = cursor.fetchone()
        if not pedido:
            print("Pedido não encontrado.")
            return

        # mostrar itens atuais
        sql_itens = """
            SELECT ip.id, c.nome_item, c.preco_item, ip.quantidade, c.id_item
            FROM itens_pedido ip
            INNER JOIN cardapio c ON ip.id_item = c.id_item
            WHERE ip.id_pedido = %s
        """
        cursor.execute(sql_itens, (id_pedido,))
        itens = cursor.fetchall()

        print("\n--- ITENS ATUAIS ---")
        for ip_id, nome, preco, qtd, _ in itens:
            print(f"ItemPedidoID: {ip_id} | {nome} x{qtd} - R${preco*qtd:.2f}")

        print("\n1 - Adicionar item")
        print("2 - Remover item")
        opc = input("Escolha uma opção: ")

        if opc == "1":
            # adicionar item
            listar_cardapio()
            try:
                novo_id_item = int(input("ID do item para adicionar: "))
                nova_qtd = int(input("Quantidade: "))
            except ValueError:
                print("Valores inválidos.")
                return

            # buscar preço
            item = buscar_item_por_id(novo_id_item)
            if not item:
                print("Item não encontrado.")
                return

            # inserir novo item_pedido
            cursor.execute(
                "INSERT INTO itens_pedido (id_pedido, id_item, quantidade) VALUES (%s, %s, %s)",
                (id_pedido, novo_id_item, nova_qtd)
            )
            novo_valor = float(item[2]) * nova_qtd
            novo_total = float(pedido[1]) + novo_valor

        elif opc == "2":
            try:
                id_item_pedido = int(input("Digite o ItemPedidoID que deseja remover: "))
            except ValueError:
                print("ID inválido.")
                return

            # pegar valor desse item pra descontar
            cursor.execute(
                """
                SELECT c.preco_item, ip.quantidade
                FROM itens_pedido ip
                INNER JOIN cardapio c ON ip.id_item = c.id_item
                WHERE ip.id = %s AND ip.id_pedido = %s
                """,
                (id_item_pedido, id_pedido)
            )
            row = cursor.fetchone()
            if not row:
                print("Item do pedido não encontrado.")
                return

            preco_item, qtd = row
            valor_remover = float(preco_item) * qtd

            # remover item
            cursor.execute("DELETE FROM itens_pedido WHERE id = %s", (id_item_pedido,))
            novo_total = float(pedido[1]) - valor_remover
            if novo_total < 0:
                novo_total = 0.0

        else:
            print("Opção inválida.")
            return

        # atualizar total do pedido
        cursor.execute(
            "UPDATE pedidos SET preco_total = %s WHERE id = %s",
            (novo_total, id_pedido)
        )

        conn.commit()
        print(f"Pedido atualizado. Novo total: R${novo_total:.2f}")

    except Exception as e:
        print(f"Erro ao atualizar pedido: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()