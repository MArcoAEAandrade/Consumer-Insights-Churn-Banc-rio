<img width="828" height="369" alt="image" src="https://github.com/user-attachments/assets/4787c282-913a-448a-b19b-2abe4c1edb34" />

# Diagnóstico de Churn – Consumer Insights

A análise da carteira revela um **churn geral de 18%**, equivalente a **14.400 clientes**. Em média, os clientes que cancelam possuem **47 anos**, cerca de dois anos mais jovens do que aqueles que permanecem na base, enquanto o gênero não apresentou relevância estatística para explicar o comportamento de evasão.

A carteira é predominantemente saudável: **93% dos clientes são classificados como baixo risco**. Por esse motivo, embora **78% dos cancelamentos também pertençam a esse segmento** (11.311), esse resultado não indica, por si só, um problema na classificação de risco, mas sim um reflexo da composição da própria carteira.

O principal insight da análise é que **o banco consegue atrair clientes qualificados, mas encontra dificuldades em desenvolvê-los e retê-los ao longo do relacionamento**. O problema, portanto, não está na aquisição, e sim na construção de engajamento: a média de engajamento de clientes ativos é 3,6 vezes mais alta do que a de inativos **(73,25 vs. 20,37).**

Ao analisar os clientes de baixo risco que cancelaram, observa-se que **70% de todo o churn do banco (10.130 clientes)** está concentrado em um perfil bastante específico: **clientes Bronze, inativos**, com **baixo engajamento (média de 16,48)** e relacionamento relativamente **curto (1,8 anos)**. Esse comportamento caracteriza uma evasão silenciosa, na qual o cliente permanece pouco conectado ao banco até decidir encerrar o relacionamento.

Essa leitura é reforçada quando comparamos os diferentes níveis de fidelidade. Os clientes Bronze apresentam os menores indicadores de relacionamento em toda a carteira: entre os que permanecem ativos, o **engajamento médio é de 29,5**, enquanto entre **os que cancelam cai para 18,8**. Além disso, **utilizam, em média, apenas 2,41 serviços**, contra **3,74 no nível Silver e 4,28 no Gold**. Já os clientes Silver e Gold mantêm índices de engajamento significativamente superiores (entre 57 e 73 pontos) e concentram um volume residual de churn. Esses resultados indicam que o risco de evasão diminui à medida que o cliente amplia seu relacionamento com o banco e avança nos níveis de fidelidade.

Quando observamos os níveis de fidelidade, o desafio torna-se ainda mais evidente. Embora o nível **Bronze represente 87% da base**, ele concentra **97% de todos os cancelamentos** (14.020 clientes). Além disso, como o nível Bronze possui as menores médias de engajamento, o desafio central não é apenas a aquisição, mas criar trilhas de desenvolvimento para que o cliente Bronze avance para os níveis Silver e Gold, onde o churn é residual.

As variáveis financeiras reforçam essa conclusão. Os clientes que permanecem no banco apresentam saldos médios, renda mensal e escore de crédito substancialmente superiores aos dos clientes que cancelam. Em média, os clientes que evadem possuem aproximadamente **um terço do saldo e da renda** dos clientes ativos, além de um **score médio de crédito inferior (653 contra 691 pontos)**.

Ao adicionarmos uma lupa na carteira Bronze, observa-se que a maior parte dos clientes que permanece no banco está no grupo de baixo risco, representando **76,6% da base** — o que é positivo. Entretanto, os clientes de baixo risco que cancelam representam **15,8% da carteira** (referenciando a regra de Pareto, em que essa parcela expressiva responde pela grande maioria das perdas), apresentando saldo médio e score de crédito significativamente menores que os clientes de mesmo perfil que permanecem ativos. Nos segmentos classificados como maior risco, tanto os que permanecem quanto os que cancelam apresentam redução adicional de renda e score, indicando que a evasão está fortemente associada aos clientes de menor capital financeiro e menor capacidade de crédito.

Outro indicador relevante da análise é o status de atividade da conta: **92% de todos os cancelamentos (13.283 clientes) ocorreram entre membros inativos**, enquanto apenas **1,4% dos clientes ativos encerraram o relacionamento**. Esse resultado demonstra que a utilização recorrente dos serviços é o principal fator de proteção contra o churn.

Além do comportamento financeiro, o aprofundamento comportamental revela que **o grupo que evade possui uma média menor de cartões (2,31 contra 2,61 dos ativos)**, reforçando a carência de produtos secundários de ancoragem que sustentam o relacionamento a longo prazo.

Esse cenário de isolamento digital e de produtos fica ainda mais evidente no nível Bronze: enquanto apenas **7,63% dos usuários mobile encerram o relacionamento**, a taxa de churn dispara para **22,51% entre os clientes offline**. Esse contraste evidencia que a ausência de adoção e transação digital atua como o principal vetor de risco para a evasão silenciosa.

---

## Quem é o cliente Bronze?

Após identificar que o nível Bronze concentra 97% de todo o churn, aprofundamos a análise para entender quem compõe esse segmento, isolando os clientes Bronze por segmento de atendimento.

* **Concentração na Base da Pirâmide:** Os clientes *Mass* respondem por **57,0% de todos os cancelamentos do banco** (8.209 clientes), enquanto o segmento *Emerging* responde por **37,9%** (5.464 clientes). Juntos, concentram **94,9% do churn entre clientes Bronze** e aproximadamente 95% de todo o churn da instituição.
* **Participação Residual nos Topos:** Os segmentos de maior valor apresentam uma participação inexpressiva nas perdas. Os clientes *Affluent* somam apenas 336 cancelamentos (**2,33%**), e o segmento *Priority* registra apenas 11 casos (**0,08%**).

Essa distribuição indica que a evasão não ocorre de forma homogênea, estando fortemente concentrada em consumidores de menor patrimônio e menor potencial financeiro. O banco demonstra alta capacidade de preservar seus clientes de maior valor (*Affluent* e *Priority*), tornando prioritário acelerar o desenvolvimento dos clientes da base da pirâmide antes que a evasão silenciosa aconteça.

Além disso, **o problema não é geográfico, mas comportamental**. Ao restringirmos a análise aos clientes *Mass* e *Bronze*, a taxa de churn permanece elevada e homogênea em todas as províncias (variando de **40,52% em Bình Dương** a **45,45% em Hanói** — uma diferença de apenas 5 pontos percentuais). Isso confirma que a localização não dita a evasão, mas sim o baixo desenvolvimento do relacionamento com a instituição, reforçando que o público de maior risco é composto por perfis *Mass*, *Bronze*, inativos e com baixa digitalização.

---

## Conclusão

O diagnóstico aponta que o desafio estratégico do banco não está em melhorar a aquisição de clientes, mas em acelerar sua evolução dentro do ecossistema. O churn concentra-se em clientes Bronze, inativos, com baixa utilização de produtos, baixo engajamento e menor capacidade financeira. Em outras palavras, trata-se de clientes que foram adquiridos com sucesso, mas que nunca desenvolveram um relacionamento consistente com a instituição.

Temos a oportunidade de mover o ponteiro com ações cirúrgicas e de baixo esforço para gerar grandes resultados. Ao atuar em recortes específicos trazidos por esta análise para sanar a evasão invisível de clientes qualificados que abandonam o banco por falta de vínculo, precisamos compreender profundamente esse relacionamento e estreitá-lo.

---

## Recomendações Estratégicas

* **Curto prazo – Reativação e migração digital de clientes inativos/offline:** Implementar campanhas direcionadas especificamente aos clientes Bronze inativos e de perfil offline, utilizando canais alternativos, gatilhos de comunicação e incentivos voltados à ativação do primeiro acesso ao aplicativo e retorno ao uso da conta antes que a evasão se torne definitiva.
* **Médio prazo – Desenvolvimento do relacionamento e ancoragem de produtos:** Estruturar jornadas de *onboarding* e engajamento com foco na ampliação do uso de produtos e serviços (como a adoção de cartões e novos serviços), incentivando a evolução dos clientes Bronze para os níveis Silver e Gold, segmentos nos quais o churn é significativamente menor. O objetivo é aumentar a integração do cliente ao ecossistema do banco, fortalecendo sua retenção no longo prazo.

* ## Status do projeto:  
| Projeto | Status | Tecs Usadas |
| :--- | :--- | :--- |
| 📊 **[PPT_Diagnóstico Churn](https://canva.link/xifcba6630oaklr)**, **[Dashboard.py](http://localhost:8503/)**| Andamento |`Python`, `SQL`, `Cloud` 
