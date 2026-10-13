"""Montagem, confirmação e consulta de vendas em memória."""

from estoque import consultar_saldo, registrar_movimentacao
from produtos import buscar_produto, formatar_reais


_proximo_id_venda = 1


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


def validar_carrinho(produtos, carrinho):
    """Revalida a estrutura, os produtos e os saldos antes da confirmação."""
    if not carrinho:
        return False, "Não é possível confirmar um carrinho vazio."

    quantidades = {}
    for item in carrinho:
        if type(item) is not dict:
            return False, "O carrinho contém um item inválido."

        codigo = item.get("codigo_produto")
        nome = item.get("nome")
        quantidade = item.get("quantidade")
        preco = item.get("preco_unitario_centavos")
        subtotal = item.get("subtotal_centavos")
        if type(codigo) is not str:
            return False, "O código de um item do carrinho é inválido."
        if type(nome) is not str or not nome.strip():
            return False, "O nome de um item do carrinho é inválido."
        if type(quantidade) is not int or quantidade <= 0:
            return False, "A quantidade deve ser um número inteiro positivo."
        if type(preco) is not int or preco <= 0:
            return False, "O preço do item é inválido."
        if type(subtotal) is not int or subtotal != quantidade * preco:
            return False, "O subtotal do item é inválido."

        produto = buscar_produto(produtos, codigo)
        if produto is None:
            return False, f"Produto {codigo} não encontrado."

        codigo_normalizado = produto["codigo"]
        quantidades[codigo_normalizado] = (
            quantidades.get(codigo_normalizado, 0) + quantidade
        )

    for codigo, quantidade in quantidades.items():
        saldo = consultar_saldo(produtos, codigo)
        if type(saldo) is not int or quantidade > saldo:
            return False, f"Saldo insuficiente para o produto {codigo}."

    return True, ""


def _copiar_itens(carrinho):
    """Cria cópias independentes dos itens que irão para o histórico."""
    itens = []
    for item in carrinho:
        itens.append(
            {
                "codigo_produto": item["codigo_produto"],
                "nome": item["nome"],
                "quantidade": item["quantidade"],
                "preco_unitario_centavos": item["preco_unitario_centavos"],
                "subtotal_centavos": item["subtotal_centavos"],
            }
        )
    return itens


def _novo_id_venda(vendas):
    """Gera um identificador único durante a execução atual."""
    global _proximo_id_venda
    venda_id = _proximo_id_venda
    ids_existentes = []
    for venda in vendas:
        if type(venda) is dict and type(venda.get("id")) is int:
            ids_existentes.append(venda["id"])

    while venda_id in ids_existentes:
        venda_id += 1

    _proximo_id_venda = venda_id + 1
    return venda_id


def _restaurar_tentativa(produtos, movimentacoes, saldos_originais, indice_inicial):
    """Restaura saldos e remove apenas movimentações desta tentativa."""
    for codigo, saldo in saldos_originais.items():
        produto = buscar_produto(produtos, codigo)
        if produto is not None:
            produto["quantidade"] = saldo
    del movimentacoes[indice_inicial:]


def confirmar_venda(produtos, movimentacoes, vendas, carrinho):
    """Confirma o carrinho de forma integral ou desfaz toda a tentativa."""
    valido, mensagem = validar_carrinho(produtos, carrinho)
    if not valido:
        return False, mensagem

    saldos_originais = {}
    for item in carrinho:
        codigo = item["codigo_produto"]
        if codigo not in saldos_originais:
            saldo = consultar_saldo(produtos, codigo)
            saldos_originais[codigo] = saldo

    indice_movimentacoes = len(movimentacoes)
    indice_vendas = len(vendas)
    venda_id = _novo_id_venda(vendas)
    motivo = f"Venda {venda_id}"

    try:
        for item in carrinho:
            sucesso, mensagem = registrar_movimentacao(
                produtos,
                movimentacoes,
                item["codigo_produto"],
                "saida",
                item["quantidade"],
                motivo,
            )
            if not sucesso:
                _restaurar_tentativa(
                    produtos,
                    movimentacoes,
                    saldos_originais,
                    indice_movimentacoes,
                )
                return False, f"Venda não confirmada: {mensagem}"

        itens = _copiar_itens(carrinho)
        vendas.append(
            {
                "id": venda_id,
                "itens": itens,
                "total_centavos": calcular_total(itens),
            }
        )
    except Exception as erro:
        _restaurar_tentativa(
            produtos,
            movimentacoes,
            saldos_originais,
            indice_movimentacoes,
        )
        del vendas[indice_vendas:]
        return False, f"Venda não confirmada: falha inesperada ({erro})."

    carrinho.clear()
    return True, f"Venda {venda_id} registrada com sucesso."


def montar_venda(produtos, movimentacoes, vendas):
    """Interage com o carrinho até confirmar ou cancelar."""
    carrinho = []
    while True:
        print("\n--- MONTAR VENDA ---")
        print("1 - Adicionar produto")
        print("2 - Remover produto")
        print("3 - Visualizar carrinho")
        print("4 - Confirmar venda")
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
        elif opcao == "4":
            sucesso, mensagem = confirmar_venda(
                produtos, movimentacoes, vendas, carrinho
            )
            print(mensagem)
            if sucesso:
                return
        elif opcao == "0":
            print("Montagem cancelada.")
            return None
        else:
            print("Opção inválida. Tente novamente.")


def iniciar_venda(produtos, movimentacoes, vendas):
    """Inicia a montagem e permite confirmar a venda."""
    return montar_venda(produtos, movimentacoes, vendas)


def exibir_historico_vendas(vendas):
    """Exibe as vendas confirmadas ou informa quando não há histórico."""
    print("\n--- HISTÓRICO DE VENDAS ---")
    if not vendas:
        print("Nenhuma venda registrada.")
        return

    for venda in vendas:
        print(
            f"Venda {venda['id']} | "
            f"Total: {formatar_reais(venda['total_centavos'])}"
        )
        for item in venda["itens"]:
            print(
                f"  {item['codigo_produto']} - {item['nome']} | "
                f"Quantidade: {item['quantidade']} | "
                f"Unitário: "
                f"{formatar_reais(item['preco_unitario_centavos'])} | "
                f"Subtotal: {formatar_reais(item['subtotal_centavos'])}"
            )


def exibir_faturamento(vendas):
    """Exibe somente a soma das vendas confirmadas."""
    total = 0
    for venda in vendas:
        total += venda["total_centavos"]
    print("\n--- FATURAMENTO ---")
    print(f"Faturamento acumulado: {formatar_reais(total)}")


def exibir_menu_vendas():
    """Exibe as operações disponíveis para vendas."""
    print("\n=== VENDAS ===")
    print("1 - Montar e confirmar venda")
    print("2 - Consultar histórico de vendas")
    print("3 - Consultar faturamento")
    print("0 - Voltar")


def menu_vendas(produtos, movimentacoes, vendas):
    """Mantém o submenu de vendas em execução."""
    while True:
        exibir_menu_vendas()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            iniciar_venda(produtos, movimentacoes, vendas)
        elif opcao == "2":
            exibir_historico_vendas(vendas)
        elif opcao == "3":
            exibir_faturamento(vendas)
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")
