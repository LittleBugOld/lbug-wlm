# Lbug-WLM

## Descrição

Lbug-WLM é uma ferramenta Python para mesclar e filtrar listas de palavras (wordlists) utilizadas em segurança ofensiva e pentests. Esta ferramenta permite que você selecione arquivos, defina limites de tamanho de palavras e processe as listas para criar um arquivo final otimizado.

## Funcionalidades

- Mescla múltiplas wordlists
- Filtra palavras com base em um comprimento mínimo e máximo
- Interface interativa para selecionar arquivos e definir configurações
- Gera um arquivo de saída com as palavras filtradas

## Como Usar

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/lbug-wlm.git
    cd lbug-wlm
    ```

2. Instale as dependências necessárias:
    ```bash
    pip install -r requirements.txt
    ```

3. Execute o script:
    ```bash
    python3 src/lbug_wlm.py
    ```

## Requisitos

- Python 3.6 ou superior
- Bibliotecas: `colorama`, `tqdm`, `pyfiglet`, `InquirerPy`, `matplotlib`

## Licença

Este projeto é licenciado sob a Licença MIT - veja o arquivo LICENSE para mais detalhes.

