# Sistema de Controle de Estoque e Vendas

Atividade acadêmica de Paradigmas de Programação desenvolvida em Python 3. O sistema é executado no terminal e aplica o estilo imperativo por meio de funções, condições, laços, listas e dicionários.

## Escopo

O projeto foi dividido em três áreas:

- produtos: cadastro, listagem, consulta e alteração de nome, preço e estoque mínimo;
- estoque: entradas, saídas, consulta de saldo, histórico de movimentações e alerta de estoque mínimo;
- vendas: montagem, confirmação e consulta de vendas.

Nesta versão, a base do programa e os módulos de produtos, estoque e vendas estão implementados.

O sistema não usa classes, frameworks, banco de dados ou interface gráfica. Todos os dados ficam somente em memória e serão perdidos quando o programa for encerrado.

## Execução

É necessário ter o Python 3 instalado. No terminal, dentro da pasta do projeto, execute:

```bash
python main.py
```

Em alguns ambientes, o comando pode ser:

```bash
python3 main.py
```

## Estrutura e compartilhamento dos dados

- `main.py`: cria uma única lista de produtos, uma de movimentações e uma de vendas, e controla o menu principal;
- `produtos.py`: contém as funções do cadastro de produtos;
- `estoque.py`: contém consulta de saldo, entradas, saídas, histórico e listagem de produtos abaixo do estoque mínimo;
- `vendas.py`: montagem, confirmação, histórico e faturamento das vendas.

As três listas são criadas somente uma vez em `main.py`. Ao chamar cada menu, o programa passa essas mesmas listas como argumentos. Como listas e dicionários são mutáveis, as funções trabalham sobre os objetos compartilhados; nenhum módulo deve criar uma segunda lista para substituir a recebida. Assim, uma alteração válida feita por um módulo fica visível aos demais durante a mesma execução.

## Contrato de dados

### Produto

Cada produto é um dicionário com os campos:

- `codigo`: texto único usado para localizar o produto;
- `nome`: nome do produto;
- `preco_centavos`: preço inteiro positivo em centavos;
- `quantidade`: quantidade inteira não negativa em unidades;
- `estoque_minimo`: quantidade inteira não negativa em unidades.

Todo produto novo começa com `quantidade` igual a `0`. O módulo de produtos não deve modificar essa quantidade; alterações de saldo são responsabilidade do módulo de estoque.

O `codigo` é normalizado sem espaços externos e com letras maiúsculas antes do cadastro ou da busca. Depois do cadastro, o código não pode ser alterado. A alteração de produtos permite modificar somente `nome`, `preco_centavos` e `estoque_minimo`.

Exemplo estrutural:

```python
{
    "codigo": "P001",
    "nome": "Nome do produto",
    "preco_centavos": 1000,
    "quantidade": 0,
    "estoque_minimo": 2,
}
```

### Movimentação

Cada movimentação é um dicionário com:

- `codigo_produto`: código textual de um produto existente;
- `tipo`: texto `entrada` ou `saida`;
- `quantidade`: quantidade inteira positiva em unidades;
- `motivo`: texto que explica a movimentação.

### Venda

Cada venda é um dicionário com:

- `id`: identificador da venda;
- `itens`: lista de itens vendidos;
- `total_centavos`: total inteiro em centavos.

Cada item da lista `itens` é um dicionário com:

- `codigo_produto`;
- `nome`;
- `quantidade`: quantidade inteira positiva em unidades;
- `preco_unitario_centavos`: preço unitário inteiro em centavos;
- `subtotal_centavos`: subtotal inteiro em centavos.

O módulo de vendas gera identificadores inteiros únicos durante a sessão atual.

Quantidades sempre representam unidades inteiras. Valores monetários são armazenados como inteiros em centavos e exibidos ao usuário em reais. Não devem ser armazenados como `float`.

## Contrato das funções compartilhadas

```python
buscar_produto(produtos, codigo)
menu_produtos(produtos)
consultar_saldo(produtos, codigo)
registrar_movimentacao(produtos, movimentacoes, codigo, tipo, quantidade, motivo)
menu_estoque(produtos, movimentacoes)
menu_vendas(produtos, movimentacoes, vendas)
```

- `buscar_produto` retorna o dicionário do produto correspondente ou `None` se o código não existir.
- `consultar_saldo` retorna a quantidade inteira do produto ou `None` se o produto não existir.
- `registrar_movimentacao` retorna a tupla `(sucesso, mensagem)`. `sucesso` indica se a operação foi concluída. Em qualquer erro, a função não pode alterar o produto nem a lista de movimentações.
- Os três menus não precisam retornar valores.

As funções `consultar_saldo`, `registrar_movimentacao`, `menu_estoque` e `menu_vendas` estão implementadas. Uma venda somente é adicionada depois da validação completa e da conclusão de todas as suas baixas.

## Responsabilidades de integração

- Integrante 1 — produtos: normalizar e manter códigos únicos, criar produtos com saldo zero, armazenar preços em centavos, permitir somente as alterações previstas no contrato e oferecer `buscar_produto` e `menu_produtos`.
- Integrante 2 — estoque: consultar e alterar saldos, validar entradas e saídas, impedir saldo negativo, registrar e consultar movimentações e listar produtos abaixo do estoque mínimo.
- Integrante 3 — vendas: manter o carrinho, validar produtos e quantidades, calcular subtotais e total em centavos, confirmar baixas pelo módulo de estoque, preservar cópias dos itens, consultar histórico e faturamento e implementar `menu_vendas`.

Antes de alterar dados, estoque e vendas devem concluir todas as validações necessárias. A confirmação revalida todos os itens antes da primeira baixa. Se uma baixa falhar depois de outras terem sido realizadas, o módulo restaura os saldos originais e remove somente as movimentações criadas naquela tentativa, sem adicionar a venda.

O módulo de estoque usa `buscar_produto` para localizar códigos segundo a mesma normalização do cadastro. O módulo de vendas usa `consultar_saldo` para revalidar o saldo acumulado e `registrar_movimentacao` para cada saída confirmada, sem duplicar a lógica de baixa.

### Operações de estoque

O módulo de estoque entrega as funções `consultar_saldo`, `registrar_movimentacao`, `exibir_historico`, `exibir_produtos_abaixo_minimo` e `menu_estoque`. As assinaturas compartilhadas de consulta, movimentação e menu permanecem conforme o contrato do projeto.

O histórico usa os campos `codigo_produto`, `tipo`, `quantidade` e `motivo` definidos no contrato de movimentação. Ele pode ser consultado por completo ou filtrado pelo código normalizado de um produto. Consultas de saldo e histórico somente leem as listas compartilhadas.

A listagem de estoque mínimo percorre os produtos e exibe somente aqueles cuja `quantidade` seja menor que `estoque_minimo`. Um saldo igual ao mínimo não é incluído.

Reposições e saídas manuais representam apenas movimentações de unidades. Elas não calculam nem registram receita. Uma venda pode aparecer no mesmo histórico ao usar um motivo identificável:

```python
registrar_movimentacao(
    produtos, movimentacoes, "P001", "entrada", 10, "Reposição"
)
registrar_movimentacao(
    produtos, movimentacoes, "P001", "saida", 2, "Saída manual"
)
registrar_movimentacao(
    produtos, movimentacoes, "P001", "saida", 1, "Venda 15"
)
```

No fluxo imperativo do estoque, o `while` mantém o submenu em execução até a opção de voltar. Os laços `for` percorrem movimentações ou produtos, enquanto condições `if` selecionam o código solicitado, identificam listas vazias e verificam quais quantidades estão abaixo do mínimo.

No fluxo de vendas, o carrinho permite incluir, acumular, remover e visualizar itens antes da confirmação. A confirmação não solicita novas entradas entre a validação final e as baixas. O histórico mantém cópias dos itens, nomes e preços, e o faturamento soma somente vendas confirmadas, sem incluir reposições ou saídas manuais.

### Contribuição real do integrante 3

O módulo [vendas.py](./vendas.py) implementa:

- `adicionar_item_carrinho`: valida produto e quantidade, acumula o mesmo código em um único item e confere o saldo disponível;
- `remover_item_carrinho`: remove o item inteiro sem alterar estoque;
- `calcular_total` e `exibir_carrinho`: calculam e exibem subtotais e total em centavos, formatados em reais;
- `validar_carrinho`: repete todas as validações antes da confirmação;
- `confirmar_venda`: executa as saídas por `registrar_movimentacao`, registra a venda somente ao final e desfaz saldos e movimentações da tentativa se uma baixa falhar;
- `montar_venda`, `iniciar_venda` e `menu_vendas`: controlam a interação no terminal;
- `exibir_historico_vendas` e `exibir_faturamento`: consultam somente vendas confirmadas.

Os itens copiados para `vendas` preservam nome, preço, quantidade e subtotal do momento da confirmação. O faturamento não considera entradas, reposições ou saídas manuais.

### Sequência de uma venda

1. O usuário escolhe a opção de nova venda e o programa cria um carrinho local.
2. A função `adicionar_item_carrinho` busca o produto e atribui quantidade, preço e subtotal.
3. Uma condição rejeita código inexistente, quantidade não positiva ou saldo acumulado insuficiente.
4. Um laço percorre o carrinho para revalidar todos os itens antes de qualquer baixa.
5. Outro laço chama `registrar_movimentacao` com tipo `saida` para cada item.
6. Se todas as chamadas forem bem-sucedidas, uma venda com cópias dos itens é acrescentada à lista e o carrinho é limpo.
7. Se uma chamada falhar, uma condição aciona o rollback dos saldos e remove somente as movimentações criadas naquela tentativa.

Essa sequência demonstra **atribuição** nas variáveis e dicionários do carrinho, **decisão** nas validações e opções do menu, **repetição** nos laços de itens e menus e **funções** para separar cálculo, validação, baixa, rollback e exibição.

## Equipe e contribuições

- Integrante 1: ____________________ — base do programa, menu principal e produtos.
- Integrante 2: ____________________ — estoque e movimentações.
- Integrante 3: ____________________ — vendas.

## Aplicação do paradigma imperativo

O programa descreve uma sequência explícita de ações e altera o estado das listas durante a execução. As funções organizam as operações; as condições selecionam o comportamento conforme as opções e validações; os laços mantêm os menus ativos e percorrem os produtos; e listas e dicionários armazenam os dados em memória.

## Reflexão da equipe

Preencher após a conclusão do trabalho:

- principais aprendizados: ________________________________________________
- dificuldades encontradas: ______________________________________________
- decisões tomadas em equipe: ____________________________________________

## Vídeo de apresentação

Link: ________________________________________________
