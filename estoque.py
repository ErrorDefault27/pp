"""Consulta de saldos e registro de movimentações de estoque."""

from produtos import buscar_produto


def consultar_saldo(produtos, codigo):
    """Retorna o saldo inteiro do produto ou None quando ele não existe."""
    if type(codigo) is not str:
        return None

    produto = buscar_produto(produtos, codigo)
    if produto is None:
        return None

    return produto["quantidade"]


def registrar_movimentacao(
    produtos, movimentacoes, codigo, tipo, quantidade, motivo
):
    """Valida, altera o saldo e registra uma entrada ou saída."""
    if type(codigo) is not str:
        return False, "Produto não encontrado."

    produto = buscar_produto(produtos, codigo)
    if produto is None:
        return False, "Produto não encontrado."

    if type(tipo) is not str:
        return False, "Tipo inválido. Use 'entrada' ou 'saida'."

    tipo_normalizado = tipo.strip().lower()
    if tipo_normalizado not in ("entrada", "saida"):
        return False, "Tipo inválido. Use 'entrada' ou 'saida'."

    if type(quantidade) is not int or quantidade <= 0:
        return False, "A quantidade deve ser um número inteiro positivo."

    if type(motivo) is not str or not motivo.strip():
        return False, "O motivo não pode ficar vazio."

    if tipo_normalizado == "saida" and quantidade > produto["quantidade"]:
        return False, "Saldo insuficiente para realizar a saída."

    if tipo_normalizado == "entrada":
        novo_saldo = produto["quantidade"] + quantidade
    else:
        novo_saldo = produto["quantidade"] - quantidade

    movimentacao = {
        "codigo_produto": produto["codigo"],
        "tipo": tipo_normalizado,
        "quantidade": quantidade,
        "motivo": motivo.strip(),
    }

    produto["quantidade"] = novo_saldo
    movimentacoes.append(movimentacao)
    return True, f"Movimentação registrada com sucesso. Saldo atual: {novo_saldo}."


def ler_quantidade_positiva(mensagem):
    """Lê uma quantidade inteira maior que zero."""
    while True:
        texto = input(mensagem).strip()
        try:
            quantidade = int(texto)
            if quantidade > 0:
                return quantidade
        except ValueError:
            pass
        print("Valor inválido. Digite um número inteiro maior que zero.")


def ler_motivo(mensagem):
    """Lê um motivo textual não vazio."""
    while True:
        motivo = input(mensagem).strip()
        if motivo:
            return motivo
        print("O motivo não pode ficar vazio.")


def movimentar_estoque(produtos, movimentacoes, tipo):
    """Solicita os dados de uma entrada ou saída e apresenta o resultado."""
    titulo = "ENTRADA DE ESTOQUE" if tipo == "entrada" else "SAÍDA DE ESTOQUE"
    print(f"\n--- {titulo} ---")
    codigo = input("Código do produto: ").strip()
    quantidade = ler_quantidade_positiva("Quantidade: ")
    motivo = ler_motivo("Motivo: ")

    sucesso, mensagem = registrar_movimentacao(
        produtos, movimentacoes, codigo, tipo, quantidade, motivo
    )
    print(mensagem)


def consultar_saldo_no_menu(produtos):
    """Solicita um código e exibe seu saldo."""
    print("\n--- CONSULTAR SALDO ---")
    codigo = input("Código do produto: ").strip()
    saldo = consultar_saldo(produtos, codigo)

    if saldo is None:
        print("Produto não encontrado.")
        return

    produto = buscar_produto(produtos, codigo)
    print(f"{produto['codigo']} - {produto['nome']} | Saldo: {saldo}")


def exibir_menu_estoque():
    """Exibe as operações disponíveis para estoque."""
    print("\n=== ESTOQUE ===")
    print("1 - Registrar entrada")
    print("2 - Registrar saída")
    print("3 - Consultar saldo")
    print("0 - Voltar")


def menu_estoque(produtos, movimentacoes):
    """Mantém o submenu de estoque em execução."""
    while True:
        exibir_menu_estoque()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            movimentar_estoque(produtos, movimentacoes, "entrada")
        elif opcao == "2":
            movimentar_estoque(produtos, movimentacoes, "saida")
        elif opcao == "3":
            consultar_saldo_no_menu(produtos)
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")
