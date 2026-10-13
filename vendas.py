"""Montagem de carrinhos de venda em memória."""

from estoque import consultar_saldo
from produtos import buscar_produto, formatar_reais


def calcular_total(itens):
    """Soma os subtotais dos itens em centavos."""
    return sum(item["subtotal_centavos"] for item in itens)


def adicionar_item_carrinho(carrinho, produtos, codigo, quantidade):
    """Inclui ou acumula um produto sem alterar as listas compartilhadas."""
    if type(codigo) is not str:
        return False, "Produto não encontrado."
    if type(quantidade) is not int or quantidade <= 0:
        return False, "A quantidade deve ser um número inteiro positivo."

    produto = buscar_produto(produtos, codigo)
    if produto is None:
        return False, "Produto não encontrado."

    item_existente = None
    for item in carrinho:
        if item["codigo_produto"] == produto["codigo"]:
            item_existente = item
            break

    quantidade_no_carrinho = 0
    if item_existente is not None:
        quantidade_no_carrinho = item_existente["quantidade"]

    saldo = consultar_saldo(produtos, produto["codigo"])
    if quantidade_no_carrinho + quantidade > saldo:
        return False, "Quantidade solicitada maior que o saldo disponível."

    if item_existente is None:
        carrinho.append(
            {
                "codigo_produto": produto["codigo"],
                "nome": produto["nome"],
                "quantidade": quantidade,
                "preco_unitario_centavos": produto["preco_centavos"],
                "subtotal_centavos": quantidade * produto["preco_centavos"],
            }
        )
    else:
        item_existente["quantidade"] += quantidade
        item_existente["subtotal_centavos"] = (
            item_existente["quantidade"]
            * item_existente["preco_unitario_centavos"]
        )

    return True, "Item incluído no carrinho."


def remover_item_carrinho(carrinho, codigo):
    """Remove um item inteiro do carrinho."""
    if type(codigo) is not str:
        return False, "Item não encontrado no carrinho."

    codigo_normalizado = codigo.strip().upper()
    for indice, item in enumerate(carrinho):
        if item["codigo_produto"] == codigo_normalizado:
            del carrinho[indice]
            return True, "Item removido do carrinho."

    return False, "Item não encontrado no carrinho."


def exibir_carrinho(carrinho):
    """Exibe quantidades, subtotais e o total atual do carrinho."""
    print("\n--- CARRINHO ---")
    if not carrinho:
        print("Carrinho vazio.")
        return

    for item in carrinho:
        print(
            f"{item['codigo_produto']} - {item['nome']} | "
            f"Quantidade: {item['quantidade']} | "
            f"Unitário: {formatar_reais(item['preco_unitario_centavos'])} | "
            f"Subtotal: {formatar_reais(item['subtotal_centavos'])}"
        )
    print(f"Total: {formatar_reais(calcular_total(carrinho))}")


def montar_venda(produtos):
    """Interage com um carrinho e retorna-o ou descarta-o ao cancelar."""
    carrinho = []
    while True:
        print("\n--- MONTAR VENDA ---")
        print("1 - Adicionar produto")
        print("2 - Remover produto")
        print("3 - Visualizar carrinho")
        print("0 - Cancelar montagem")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            codigo = input("Código do produto: ").strip()
            texto_quantidade = input("Quantidade: ").strip()
            try:
                quantidade = int(texto_quantidade)
            except ValueError:
                quantidade = 0
            sucesso, mensagem = adicionar_item_carrinho(
                carrinho, produtos, codigo, quantidade
            )
            print(mensagem)
        elif opcao == "2":
            codigo = input("Código do produto: ").strip()
            sucesso, mensagem = remover_item_carrinho(carrinho, codigo)
            print(mensagem)
        elif opcao == "3":
            exibir_carrinho(carrinho)
        elif opcao == "0":
            print("Montagem cancelada.")
            return None
        else:
            print("Opção inválida. Tente novamente.")


def iniciar_venda(produtos, movimentacoes, vendas):
    """Inicia a montagem sem finalizar ou registrar a venda."""
    return montar_venda(produtos)


def exibir_menu_vendas():
    """Exibe as operações disponíveis para a etapa de montagem."""
    print("\n=== VENDAS ===")
    print("1 - Montar venda")
    print("0 - Voltar")


def menu_vendas(produtos, movimentacoes, vendas):
    """Mantém o submenu de montagem de vendas em execução."""
    while True:
        exibir_menu_vendas()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            iniciar_venda(produtos, movimentacoes, vendas)
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")
