# Sistema de Controle de Estoque e Vendas

Atividade acadêmica de Paradigmas de Programação desenvolvida em Python 3. O sistema funciona no terminal e aplica o paradigma imperativo por meio de atribuições, condições, laços, funções, listas e dicionários.

## Descrição do problema

O projeto controla produtos, movimentações de estoque e vendas em uma única execução. Ele permite cadastrar e consultar produtos, registrar entradas e saídas, acompanhar saldos, montar vendas e consultar o faturamento.

O sistema não usa classes, frameworks, banco de dados ou interface gráfica. **Todos os dados ficam somente em memória e são perdidos quando o programa é encerrado.**

## Entradas, regras e resultados

### Entradas

O usuário informa dados pelos menus do terminal:

- produtos: código, nome, preço e estoque mínimo;
- estoque: código do produto, tipo da movimentação, quantidade e motivo;
- vendas: código do produto, quantidade e opções para incluir, remover, confirmar ou cancelar itens;
- consultas: código do produto ou opção de histórico e faturamento.

### Regras principais

- o código do produto é obrigatório, único, normalizado sem espaços externos e convertido para letras maiúsculas;
- o nome do produto é obrigatório;
- o preço é positivo e armazenado como um número inteiro de centavos;
- o estoque mínimo é um número inteiro não negativo;
- produtos novos começam com quantidade igual a zero;
- entradas e saídas usam quantidades inteiras positivas;
- uma saída não pode deixar o estoque negativo;
- um produto repetido no carrinho tem sua quantidade acumulada;
- uma venda vazia, com produto inexistente ou quantidade inválida não pode ser confirmada;
- a confirmação revalida todos os itens antes da primeira baixa;
- se a confirmação falhar, os saldos e as movimentações da tentativa são restaurados e a venda não é registrada;
- o cancelamento do carrinho não altera estoque, movimentações ou vendas;
- o histórico da venda guarda nome e preço do momento da confirmação;
- entradas e saídas manuais não fazem parte do faturamento.

### Resultados

O programa apresenta no terminal:

- produtos cadastrados e dados de um produto consultado;
- saldo atual e histórico de movimentações;
- produtos abaixo do estoque mínimo;
- itens, subtotais e total do carrinho;
- histórico de vendas confirmadas;
- faturamento acumulado das vendas confirmadas;
- mensagens de sucesso ou de validação para operações inválidas.

## Execução

É necessário ter o Python 3 instalado. No terminal, dentro da pasta do projeto, execute:

```bash
python main.py
```

Em alguns ambientes, o comando pode ser:

```bash
python3 main.py
```

No Windows, também pode estar disponível:

```powershell
py main.py
```

## Estrutura e integração

- `main.py`: cria as listas compartilhadas e controla o menu principal;
- `produtos.py`: cadastro, listagem, consulta e alteração de produtos;
- `estoque.py`: entradas, saídas, consulta de saldo, histórico e alerta de estoque mínimo;
- `vendas.py`: carrinho, confirmação, histórico e faturamento das vendas.

As listas de produtos, movimentações e vendas são criadas uma única vez em `main.py`. Os submenus recebem essas mesmas listas como argumentos. Como listas e dicionários são mutáveis, uma alteração válida realizada por um módulo permanece visível aos demais durante a mesma execução.

## Contrato de dados

### Produto

Cada produto é um dicionário com os campos:

- `codigo`: texto único usado para localizar o produto;
- `nome`: nome do produto;
- `preco_centavos`: preço inteiro positivo em centavos;
- `quantidade`: quantidade inteira não negativa;
- `estoque_minimo`: quantidade inteira não negativa.

Exemplo:

```python
{
    "codigo": "P001",
    "nome": "Nome do produto",
    "preco_centavos": 1000,
    "quantidade": 0,
    "estoque_minimo": 2,
}
```

O módulo de produtos não modifica `quantidade`. Alterações de saldo são responsabilidade do módulo de estoque. Depois do cadastro, o código não pode ser alterado; somente nome, preço e estoque mínimo podem ser atualizados.

### Movimentação

Cada movimentação é um dicionário com:

- `codigo_produto`: código de um produto existente;
- `tipo`: `entrada` ou `saida`;
- `quantidade`: número inteiro positivo;
- `motivo`: texto que explica a movimentação.

### Venda

Cada venda é um dicionário com:

- `id`: identificador inteiro único durante a sessão;
- `itens`: lista dos itens vendidos;
- `total_centavos`: total inteiro em centavos.

Cada item vendido contém:

- `codigo_produto`;
- `nome`;
- `quantidade`;
- `preco_unitario_centavos`;
- `subtotal_centavos`.

## Contrato das funções compartilhadas

```python
buscar_produto(produtos, codigo)
menu_produtos(produtos)
consultar_saldo(produtos, codigo)
registrar_movimentacao(produtos, movimentacoes, codigo, tipo, quantidade, motivo)
menu_estoque(produtos, movimentacoes)
menu_vendas(produtos, movimentacoes, vendas)
```

- `buscar_produto` retorna o produto correspondente ou `None`;
- `consultar_saldo` retorna a quantidade do produto ou `None`;
- `registrar_movimentacao` retorna `(sucesso, mensagem)` e não deve modificar dados quando a operação é inválida;
- os três menus trabalham sobre as listas recebidas e não precisam retornar valores.

O estoque usa `buscar_produto` para aplicar a mesma normalização do cadastro. Vendas usa `consultar_saldo` para revalidar quantidades e `registrar_movimentacao` para efetuar cada baixa, sem duplicar a regra de estoque.

## Equipe e contribuições reais

Os nomes precisam ser preenchidos pelos próprios integrantes antes da entrega.

| Integrante | Nome | Contribuição real no repositório |
|---|---|---|
| Integrante 1 | Edgar Cauã Mota da Anunciação 04160900 | Base do programa e `main.py`; cadastro, normalização, busca, listagem e alteração de produtos em `produtos.py`. |
| Integrante 2 | Marcelo Vitor Pegado Rodrigues 04167741 | Consulta e alteração de saldos; entradas, saídas, validações, histórico e alerta de estoque mínimo em `estoque.py`. |
| Integrante 3 | Pedro Tocantins Faidherb 04159252 | Carrinho, validações, totais, confirmação e rollback, histórico e faturamento em `vendas.py`. |

### Produtos — integrante 1

O módulo `produtos.py` normaliza e mantém códigos únicos, cria produtos com saldo zero, converte preços para centavos e permite alterar somente nome, preço e estoque mínimo. Ele oferece `buscar_produto` e `menu_produtos` para integração com os demais módulos.

### Estoque — integrante 2

O módulo `estoque.py` implementa `consultar_saldo`, `registrar_movimentacao`, `exibir_historico`, `exibir_produtos_abaixo_minimo` e `menu_estoque`. Ele impede saldo negativo e mantém entradas, saídas manuais e baixas de vendas no mesmo histórico de movimentações.

Um produto é apresentado no alerta somente quando sua quantidade é menor que o estoque mínimo. Saldo igual ao mínimo não entra no alerta.

### Vendas — integrante 3

O módulo `vendas.py` implementa:

- inclusão e acumulação de itens no carrinho;
- remoção e visualização de itens;
- cálculo de subtotais e total em centavos;
- revalidação do carrinho antes da confirmação;
- baixa por meio do módulo de estoque;
- restauração dos dados se uma confirmação falhar;
- cópia dos itens para preservar nome e preço da venda;
- histórico de vendas e faturamento.

Somente uma venda confirmada é adicionada ao histórico. O faturamento soma apenas vendas confirmadas.

## Aplicação do paradigma imperativo

- **atribuição:** variáveis e campos dos dicionários recebem e atualizam valores;
- **decisão:** condições validam entradas, selecionam opções dos menus e impedem operações inválidas;
- **repetição:** laços mantêm os menus ativos e percorrem produtos, movimentações, itens e vendas;
- **funções:** cada operação é dividida em funções de cadastro, consulta, validação, movimentação, cálculo e exibição;
- **estado mutável:** listas e dicionários representam o estado do sistema e são alterados ao longo da execução.

O fluxo de confirmação de uma venda combina esses conceitos: percorre o carrinho, valida os itens, executa cada baixa, registra a venda ao final e restaura o estado anterior quando ocorre uma falha.

## Reflexão da equipe

Esta seção deve registrar somente experiências reais do grupo:

- principais aprendizados: 
Durante o desenvolvimento, aprendemos a usar o paradigma imperativo em um sistema completo, com variáveis, listas, dicionários, condições, repetições e funções. Também entendemos como as partes do sistema compartilham os mesmos dados. Ao integrar produtos, estoque e vendas, percebemos a importância de combinar como as funções devem funcionar e conferir os dados antes de modificá-los.;
- dificuldades realmente encontradas: 
Não encontramos dificuldades relevantes. Foi identificado apenas um pequeno erro na finalização da compra, que poderia gerar uma baixa parcial no estoque em caso de falha. A confirmação da venda foi ajustada para desfazer todas as alterações quando ocorre um erro.;
- decisões tomadas em conjunto: 
A equipe decidiu dividir o sistema em módulos de produtos, estoque e vendas, mantendo o menu principal responsável pela criação e pelo compartilhamento das listas. Os valores monetários foram armazenados como números inteiros em centavos para evitar erros de precisão. Também decidimos manter os dados somente em memória, conforme o escopo do trabalho, e registrar o nome e o preço dos itens no momento da venda para que alterações posteriores no cadastro não modificassem o histórico. As validações foram realizadas antes das alterações sempre que possível, e a confirmação da venda recebeu um mecanismo de restauração para evitar processamento parcial..

## Vídeo de apresentação

Link do vídeo: [**\[PREENCHER\]**](https://youtu.be/XDnPRacHEd8)