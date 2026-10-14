"""Gerenciamento de produtos armazenados em memória."""


def normalizar_codigo(codigo):
    """Remove espaços externos e converte o código para maiúsculas."""
    return codigo.strip().upper()


def buscar_produto(produtos, codigo):
    """Retorna o produto correspondente ao código normalizado ou None."""
    codigo_normalizado = normalizar_codigo(codigo)

    for produto in produtos:
        if produto["codigo"] == codigo_normalizado:
            return produto

    return None


def adicionar_produto(
    produtos, codigo, nome, preco_centavos, estoque_minimo
):
    """Valida os dados e adiciona um produto com quantidade inicial zero."""
    codigo_normalizado = normalizar_codigo(codigo)
    nome_normalizado = nome.strip()

    if not codigo_normalizado:
        return False, "O código não pode ficar vazio."
    if not nome_normalizado:
        return False, "O nome não pode ficar vazio."
    if buscar_produto(produtos, codigo_normalizado) is not None:
        return False, "Já existe um produto com esse código."
    if type(preco_centavos) is not int or preco_centavos <= 0:
        return False, "O preço deve ser um valor positivo em centavos."
    if type(estoque_minimo) is not int or estoque_minimo < 0:
        return False, "O estoque mínimo deve ser um número inteiro não negativo."

    produto = {
        "codigo": codigo_normalizado,
        "nome": nome_normalizado,
        "preco_centavos": preco_centavos,
        "quantidade": 0,
        "estoque_minimo": estoque_minimo,
    }
    produtos.append(produto)
    return True, "Produto cadastrado com sucesso. Quantidade inicial: 0."


def alterar_produto(
    produtos, codigo, novo_nome, novo_preco_centavos, novo_estoque_minimo
):
    """Valida e altera somente nome, preço e estoque mínimo."""
    produto = buscar_produto(produtos, codigo)
    nome_normalizado = novo_nome.strip()

    if produto is None:
        return False, "Produto não encontrado."
    if not nome_normalizado:
        return False, "O nome não pode ficar vazio."
    if type(novo_preco_centavos) is not int or novo_preco_centavos <= 0:
        return False, "O preço deve ser um valor positivo em centavos."
    if type(novo_estoque_minimo) is not int or novo_estoque_minimo < 0:
        return False, "O estoque mínimo deve ser um número inteiro não negativo."

    produto["nome"] = nome_normalizado
    produto["preco_centavos"] = novo_preco_centavos
    produto["estoque_minimo"] = novo_estoque_minimo
    return True, "Produto atualizado com sucesso."


def converter_preco_para_centavos(texto):
    """Converte reais para centavos sem usar float ou arredondamento."""
    valor = texto.strip()

    if not valor or ("," in valor and "." in valor):
        return None

    separador = None
    if "," in valor:
        separador = ","
    elif "." in valor:
        separador = "."

    if separador is None:
        if not valor.isdigit():
            return None
        parte_inteira = valor
        parte_decimal = ""
    else:
        partes = valor.split(separador)
        if len(partes) != 2:
            return None
        parte_inteira = partes[0]
        parte_decimal = partes[1]
        if (
            not parte_inteira.isdigit()
            or not parte_decimal.isdigit()
            or len(parte_decimal) > 2
        ):
            return None

    centavos = int(parte_inteira) * 100
    if len(parte_decimal) == 1:
        centavos += int(parte_decimal) * 10
    elif len(parte_decimal) == 2:
        centavos += int(parte_decimal)

    return centavos


def formatar_reais(valor_centavos):
    """Formata um valor inteiro em centavos para exibição em reais."""
    reais = valor_centavos // 100
    centavos = valor_centavos % 100
    return f"R$ {reais},{centavos:02d}"


def ler_codigo(mensagem):
    """Lê e normaliza um código textual não vazio."""
    while True:
        codigo = normalizar_codigo(input(mensagem))
        if codigo:
            return codigo
        print("O código não pode ficar vazio.")


def ler_nome(mensagem):
    """Lê um nome não vazio."""
    while True:
        nome = input(mensagem).strip()
        if nome:
            return nome
        print("O nome não pode ficar vazio.")


def ler_preco_centavos(mensagem):
    """Lê um preço positivo em reais e retorna centavos inteiros."""
    while True:
        preco_centavos = converter_preco_para_centavos(input(mensagem))
        if preco_centavos is not None and preco_centavos > 0:
            return preco_centavos
        print(
            "Preço inválido. Use um valor positivo, sem separador de milhar "
            "e com no máximo duas casas decimais."
        )


def ler_inteiro_nao_negativo(mensagem):
    """Lê um número inteiro maior ou igual a zero."""
    while True:
        texto = input(mensagem).strip()
        try:
            valor = int(texto)
            if valor >= 0:
                return valor
        except ValueError:
            pass
        print("Valor inválido. Digite um número inteiro maior ou igual a zero.")


def cadastrar_produto(produtos):
    """Solicita os dados de cadastro e apresenta o resultado."""
    print("\n--- CADASTRAR PRODUTO ---")

    while True:
        codigo = ler_codigo("Código: ")
        if buscar_produto(produtos, codigo) is None:
            break
        print("Já existe um produto com esse código. Informe outro código.")

    nome = ler_nome("Nome: ")
    preco_centavos = ler_preco_centavos("Preço: R$ ")
    estoque_minimo = ler_inteiro_nao_negativo("Estoque mínimo: ")

    sucesso, mensagem = adicionar_produto(
        produtos, codigo, nome, preco_centavos, estoque_minimo
    )
    print(mensagem)


def exibir_produto(produto):
    """Exibe os campos de um produto."""
    print(
        f"Código: {produto['codigo']} | "
        f"Nome: {produto['nome']} | "
        f"Preço: {formatar_reais(produto['preco_centavos'])} | "
        f"Quantidade: {produto['quantidade']} | "
        f"Estoque mínimo: {produto['estoque_minimo']}"
    )


def listar_produtos(produtos):
    """Exibe todos os produtos cadastrados."""
    print("\n--- PRODUTOS CADASTRADOS ---")
    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    for produto in produtos:
        exibir_produto(produto)


def consultar_produto(produtos):
    """Lê um código e exibe o produto correspondente."""
    print("\n--- CONSULTAR PRODUTO ---")
    codigo = ler_codigo("Código: ")
    produto = buscar_produto(produtos, codigo)

    if produto is None:
        print("Produto não encontrado.")
        return

    exibir_produto(produto)


def editar_produto(produtos):
    """Lê e altera os campos permitidos de um produto existente."""
    print("\n--- ALTERAR PRODUTO ---")
    codigo = ler_codigo("Código do produto: ")
    produto = buscar_produto(produtos, codigo)

    if produto is None:
        print("Produto não encontrado.")
        return

    print("Código e quantidade não são alterados neste módulo.")
    novo_nome = ler_nome("Novo nome: ")
    novo_preco_centavos = ler_preco_centavos("Novo preço: R$ ")
    novo_estoque_minimo = ler_inteiro_nao_negativo("Novo estoque mínimo: ")

    sucesso, mensagem = alterar_produto(
        produtos,
        codigo,
        novo_nome,
        novo_preco_centavos,
        novo_estoque_minimo,
    )
    print(mensagem)


def exibir_menu_produtos():
    """Exibe as operações disponíveis para produtos."""
    print("\n=== PRODUTOS ===")
    print("1 - Cadastrar")
    print("2 - Listar")
    print("3 - Consultar por código")
    print("4 - Alterar")
    print("0 - Voltar")


def menu_produtos(produtos):
    """Mantém o submenu de produtos em execução."""
    while True:
        exibir_menu_produtos()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_produto(produtos)
        elif opcao == "2":
            listar_produtos(produtos)
        elif opcao == "3":
            consultar_produto(produtos)
        elif opcao == "4":
            editar_produto(produtos)
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")
