# Escalabilidade e Infraestrutura

Este documento explica as escolhas arquiteturais de infraestrutura feitas para permitir que o SST Manager atenda a milhares de *tenants* de forma horizontal.

## Filosofia "Stateless" (Sem Estado)

> [!NOTE]
> O backend do SST Manager é 100% *stateless* e pronto para nuvem (cloud-native).

Nenhuma sessão de usuário é armazenada na memória da aplicação ou em disco local da instância. Toda a informação de autenticação e identidade de *tenant* transita via **JWT (JSON Web Token)** pelo lado do cliente.
Isso permite que qualquer requisição de um usuário seja atendida por qualquer container da aplicação.

## Arquitetura de Escalabilidade Horizontal

```mermaid
flowchart TD
    Client((Clientes Web)) -->|HTTPS| LB[Load Balancer / Nginx]
    
    subgraph Aplicação (Horizontal Scaling)
        LB --> API1[Instância FastAPI 1]
        LB --> API2[Instância FastAPI 2]
        LB --> APIN[Instância FastAPI N]
    end
    
    subgraph Camada de Dados
        API1 --> Redis[(Redis Cache)]
        API2 --> Redis
        APIN --> Redis
        
        API1 --> DB_W[(MySQL Primary/Writer)]
        API2 --> DB_W
        APIN --> DB_W
        
        DB_W -.->|Replicação Async| DB_R[(MySQL Read Replica)]
    end
```

## Escalabilidade de Banco de Dados
- **Connection Pooling**: Utilizamos o recurso nativo de Pool do SQLAlchemy assíncrono para gerenciar conexões ao MySQL eficientemente.
- **Read Replicas (Planejado)**: Para picos de visualização em relatórios complexos, queries de leitura podem ser roteadas futuramente para réplicas de leitura, liberando a instância primária para operações de escrita (CRUD/Transações).

## Estratégia de Cache
- **Redis** é introduzido no ecossistema não para armazenar sessão de usuário, mas para cachear:
  - Listas estáticas e informações que mudam raramente (ex. Tabela de naturezas de CBO/CNAE).
  - Resultados computacionalmente caros (consultas de Dashboards pesadas).
  - Controle de *Rate Limiting*.

## Docker Compose para Produção
No ambiente de produção ou *staging*, recomendamos o uso do `docker-compose.yml` que provisiona a *stack* inteira:
1. `nginx`: Atua como proxy reverso, terminador SSL/TLS e balanceador.
2. `api`: Container baseado na imagem oficial Python 3.11 *slim*, rodando Uvicorn/Gunicorn.
3. `db`: Imagem MySQL 8 otimizada.
4. `redis`: Instância simples do Redis.

## Monitoramento
Para garantir a integridade em escala, endpoints de monitoramento estão disponíveis:
- `/health`: Retorna 200 OK com latência da conexão do banco de dados, usado por *liveness probes*.
- Recomendado integrar com ferramentas de logs centralizados, visto que a aplicação utiliza logging estruturado enviando saídas para o `STDOUT` do container.
