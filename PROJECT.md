# Visão Geral do Projeto

Este documento detalha o que é o **SST Manager**, seus principais conceitos de negócio, fluxos de trabalho, regras de negócio e personas.

> [!NOTE]
> O SST Manager é um sistema SaaS de Gestão de Segurança e Saúde no Trabalho (SST), desenvolvido para facilitar e organizar a rotina de profissionais e clínicas de SST.

## O que é o SST Manager
O SST Manager é uma plataforma robusta e escalável desenvolvida para centralizar a gestão de dados ocupacionais de empresas e seus funcionários. Como uma solução multilocatária (multi-tenant), permite que diversas clínicas ou empresas de consultoria em SST gerenciem seus clientes finais em um único ambiente seguro e isolado, garantindo conformidade com a legislação trabalhista brasileira.

## Glossário de Termos de SST

- **ASO (Atestado de Saúde Ocupacional)**: Documento médico que avalia a aptidão do trabalhador para exercer suas funções.
- **CAT (Comunicação de Acidente de Trabalho)**: Documento obrigatório para registrar acidentes ou doenças ocupacionais junto ao INSS.
- **EPI (Equipamento de Proteção Individual)**: Todo dispositivo ou produto de uso individual utilizado pelo trabalhador para proteção contra riscos.
- **NR (Norma Regulamentadora)**: Conjunto de requisitos e procedimentos relativos à segurança e medicina do trabalho.
- **CA (Certificado de Aprovação)**: Documento emitido pelo Ministério do Trabalho que atesta a eficácia e validade de um EPI.
- **PCMSO (Programa de Controle Médico de Saúde Ocupacional)**: Programa focado em promover e preservar a saúde dos trabalhadores.
- **PGR (Programa de Gerenciamento de Riscos)**: Programa que visa identificar, avaliar e propor medidas de controle de riscos ambientais.
- **LTCAT (Laudo Técnico das Condições Ambientais de Trabalho)**: Documento que atesta as condições ambientais de trabalho para fins previdenciários.

## Fluxo de Trabalho do Usuário

### 1. Gestão de Funcionários
O usuário cadastra funcionários vinculando-os ao *tenant* (cliente) adequado. Cada funcionário possui dados como nome, CPF, matrícula, cargo, setor e data de admissão. O controle de status (ativo/inativo) é mantido para manter o histórico sem deletar os registros (soft delete).

### 2. Entrega e Controle de EPIs
Após o cadastro do funcionário, o técnico de segurança registra a entrega de EPIs gerando a "Ficha de Entrega de EPI". Isso exige a inserção do CA válido, data de entrega e data de validade, além do controle de assinaturas.

### 3. Gestão de Saúde Ocupacional (ASO)
O médico do trabalho ou equipe administrativa registra a realização de exames (admissional, periódico, de retorno, etc.). O sistema emite alertas para ASOs próximos do vencimento.

### 4. Monitoramento de NRs e Acidentes (CAT)
O sistema permite avaliar o status de conformidade da empresa em relação às NRs aplicáveis. Em caso de acidente, o formulário de CAT é preenchido com descrição, parte do corpo afetada e dias de afastamento.

### 5. Visão Gerencial
No Dashboard, gestores acompanham métricas agregadas: funcionários ativos, ASOs vencendo nos próximos 30 dias, CATs registradas no ano e pendências em NRs.

## Regras de Negócio Importantes

> [!IMPORTANT]
> As seguintes regras devem ser aplicadas rigorosamente no backend:

- **Isolamento de Dados**: NENHUM usuário pode acessar ou modificar registros de outro `tenant_id`. Todas as queries devem filtrar por este identificador.
- **Validade do ASO**: A validade depende do risco e do tipo de exame, mas o sistema deve alertar com pelo menos 30 dias de antecedência.
- **Controle de EPIs**: Um EPI não pode ser entregue se o seu CA estiver vencido ou for inválido.
- **Status das NRs**: O status global de uma NR para a empresa só é dado como "Em conformidade" se todas as verificações exigidas estiverem cumpridas.
- **Exclusão de Registros**: O sistema prioriza exclusão lógica (campo `ativo = false`) para manter a rastreabilidade e histórico, especialmente para funcionários e registros médicos.

## Público-Alvo e Personas

1. **Técnico de Segurança (tecnico)**
   - **Foco**: Operação diária, entrega de EPIs, registro de CATs e inspeções de NR.
   - **Necessidades**: Agilidade no cadastro, alertas de validade.

2. **Engenheiro/Médico de Segurança (gestor)**
   - **Foco**: Aprovação de ASOs, validação de PGR, análise técnica.
   - **Necessidades**: Visualização detalhada de riscos e exames.

3. **Gestor de RH / Administração (admin/gestor)**
   - **Foco**: Acompanhamento de indicadores de absenteísmo, custos com acidentes e conformidade legal.
   - **Necessidades**: Dashboards, relatórios gerenciais e extração de dados.

4. **Auditor / Visualizador (visualizador)**
   - **Foco**: Visualização apenas-leitura de evidências para auditorias e fiscalizações.
   - **Necessidades**: Acesso simples para emitir relatórios de conformidade.
