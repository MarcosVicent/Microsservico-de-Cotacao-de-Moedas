# Microsserviço de Cotação de Moedas

API RESTful e GraphQL que, dado uma moeda base (ex: USD), retorna sua cotação em relação a outras moedas. O projeto utiliza FastAPI, Docker, Kubernetes e Redis para cache, servindo como uma base sólida para a arquitetura de microsserviços.

## Funcionalidades
- **Cotação em tempo real:** Obtém o valor de câmbio de uma moeda base.
- **Cache com Redis:** Armazena cotações recentes para respostas mais rápidas e redução de chamadas a APIs externas.
- **Múltiplas interfaces:** Disponível via API RESTful e GraphQL.

## Tecnologias e Arquitetura
- **Linguagem:** Python 3.10+
- **Framework Web:** **FastAPI**
- **Camadas de Arquitetura:** Apresentação (API), Serviço e Repositório (Dados).
- **Design Patterns:** **Repository Pattern** e **Dependency Injection**.
- **Cache:** **Redis**
- **Contêinerização:** **Docker** e **Docker Compose**
- **Orquestração:** **Kubernetes (K8s)**
- **Testes:** Testes unitários e de integração com **Pytest**.

## Pré-requisitos
- Python 3.10+
- Docker e Docker Compose

## Como Rodar Localmente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/](https://github.com/)[seu-usuario]/[seu-repositorio].git
    cd [seu-repositorio]
    ```

2.  **Configurar o ambiente:**
    Crie um arquivo `.env` na raiz do projeto com suas variáveis de ambiente, com base no arquivo `.env.example`.
    ```bash
    cp .env.example .env
    ```

3.  **Inicie o microsserviço e o Redis com Docker Compose:**
    Este comando irá construir a imagem da sua aplicação, criar os contêineres e conectá-los em uma única rede.
    ```bash
    docker-compose up --build
    ```
    O serviço estará disponível em `http://localhost:8000`.

## Endpoints da API

### RESTful
- **Cotação de todas as moedas:** `GET /api/v1/cotacao/{moeda_base}`
- **Cotação de uma moeda específica:** `GET /api/v1/cotacao/{moeda_base}/{moeda_alvo}`

### GraphQL
- **Acesse a interface:** `http://localhost:8000/graphql`
- **Exemplo de query:**
    ```graphql
    query {
      cotacao(moedaBase: "USD", moedaAlvo: "BRL") {
        moedaBase
        moedaAlvo
        valor
      }
    }
    ```

## Testes

Para rodar os testes unitários e de integração, use `pytest`.
```bash
pytest