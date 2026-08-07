# Diagnóstico de Churn – Consumer Insights

A análise da carteira revela um **churn geral de 18%**, equivalente a **14.400 clientes**. Em média, os clientes que cancelam possuem **47 anos**, cerca de dois anos mais jovens do que aqueles que permanecem na base, enquanto o gênero não apresentou relevância estatística para explicar o comportamento de evasão.

A carteira é predominantemente saudável: **93% dos clientes são classificados como baixo risco**. Por esse motivo, embora **78% dos cancelamentos também pertençam a esse segmento**, esse resultado não indica, por si só, um problema na classificação de risco, mas sim um reflexo da composição da própria carteira.

O principal insight da análise é que **o banco consegue atrair clientes qualificados, mas encontra dificuldades em desenvolvê-los e retê-los ao longo do relacionamento**. O problema, portanto, não está na aquisição, e sim na construção de engajamento.

Ao analisar os clientes de baixo risco que cancelaram, observa-se que **70% de todo o churn do banco (10.130 clientes)** está concentrado em um perfil bastante específico: **clientes Bronze, inativos**, com baixo engajamento (média de 16,48) e relacionamento relativamente curto (1,8 anos). Esse comportamento caracteriza uma evasão silenciosa, na qual o cliente permanece pouco conectado ao banco até decidir encerrar o relacionamento.

Essa leitura é reforçada quando comparamos os diferentes níveis de fidelidade. Os clientes Bronze apresentam os menores indicadores de relacionamento em toda a carteira: entre os que permanecem ativos, o engajamento médio é de 29,5, enquanto entre os que cancelam cai para 18,8. Além disso, utilizam, em média, apenas 2,41 serviços, contra 3,74 no nível Silver e 4,28 no Gold. Já os clientes Silver e Gold mantêm índices de engajamento significativamente superiores (entre 57 e 73 pontos) e concentram um volume residual de churn. Esses resultados indicam que o risco de evasão diminui à medida que o cliente amplia seu relacionamento com o banco e avança nos níveis de fidelidade.

Essa hipótese é reforçada pela análise de utilização dos produtos. Enquanto os clientes ativos utilizam, em média, **3,81 produtos**, os clientes que cancelam utilizam apenas **2,44**. Da mesma forma, o índice médio de engajamento é significativamente maior entre os clientes ativos (**34**) do que entre os que evadem (**19**). Em contrapartida, o tempo médio de relacionamento permanece semelhante entre os grupos, indicando que o churn não ocorre apenas na fase inicial da jornada, mas está mais associado ao baixo uso do ecossistema do banco do que ao tempo de permanência.

Quando observamos os níveis de fidelidade, o desafio torna-se ainda mais evidente. Embora o nível **Bronze represente 87% da base**, ele concentra **97% de todos os cancelamentos** (14.020 clientes). Além disso, esse segmento apresenta as menores médias de engajamento e utilização de produtos, indicando que grande parte dos clientes nunca evolui dentro do relacionamento com a instituição.

As variáveis financeiras reforçam essa conclusão. Os clientes que permanecem no banco apresentam saldos médios, renda mensal e escore de crédito substancialmente superiores aos dos clientes que cancelam. Em média, os clientes que evadem possuem aproximadamente **um terço do saldo e da renda** dos clientes ativos, além de um **score médio de crédito inferior (653 contra 691 pontos)**.

Ao restringir a análise ao segmento Bronze, observa-se que a maior parte da carteira permanece ativa no grupo de baixo risco (**76,6% da base**). Entretanto, os clientes de baixo risco que cancelam representam **15,8% da carteira**, apresentando saldo médio e score de crédito significativamente menores que os clientes de mesmo perfil que permanecem ativos. Nos segmentos classificados como maior risco, tanto ativos quanto cancelados apresentam redução adicional de renda e score, indicando que a evasão está fortemente associada aos clientes de menor capital financeiro e menor capacidade de crédito.

O indicador mais relevante da análise, contudo, é o status de atividade da conta. **92% de todos os cancelamentos (13.283 clientes) ocorreram entre membros inativos**, enquanto apenas **1,4% dos clientes ativos encerraram o relacionamento**. Esse resultado demonstra que a utilização recorrente dos serviços é o principal fator de proteção contra o churn.

Além disso, o aprofundamento comportamental e de produtos demonstra que **o grupo que evadem possui uma média menor de cartões (2,31 contra 2,61 dos ativos)**, reforçando a carência de produtos secundários de ancoragem. No recorte digital do nível Bronze, **22,51% dos clientes offline encerram o relacionamento**, em contraste com apenas **7,63% dos usuários mobile**, evidenciando que a ausência de adoção e transação digital atua como um forte vetor de risco para a evasão.

Quem é o cliente Bronze?

Após identificar que o nível Bronze concentra 97% de todo o churn, aprofundamos a análise para entender quem compõe esse segmento. Para isso, isolamos os clientes Bronze e analisamos sua distribuição por segmento de cliente.

Os resultados mostram uma forte concentração do churn nos segmentos de entrada da carteira. Os clientes Mass representam 57,0% de todos os cancelamentos do banco (8.209 clientes), enquanto o segmento Emerging responde por 37,9% (5.464 clientes). Juntos, esses dois segmentos concentram 94,9% do churn entre clientes Bronze e aproximadamente 95% de todo o churn da instituição.

Em contrapartida, os segmentos de maior valor apresentam uma participação praticamente residual. Os clientes Affluent somam apenas 336 cancelamentos (2,33%), enquanto o segmento Priority registra apenas 11 casos (0,08%).

Essa distribuição indica que a evasão não ocorre de forma homogênea na carteira. O problema está fortemente concentrado na base da pirâmide de clientes, composta por consumidores de menor patrimônio e menor potencial financeiro. Isso reforça os insights apresentados anteriormente: os clientes que cancelam são, em sua maioria, clientes Bronze, com baixo engajamento, pouca utilização dos serviços e pertencentes aos segmentos Mass e Emerging, que ainda não desenvolveram um relacionamento consistente com o banco.

Do ponto de vista estratégico, o banco demonstra boa capacidade de preservar seus clientes de maior valor (Affluent e Priority). O principal desafio passa a ser acelerar o desenvolvimento dos clientes da base da pirâmide, aumentando seu engajamento e utilização do ecossistema bancário antes que a evasão silenciosa aconteça.

O problema não é geográfico, mas comportamental. Ao restringirmos a análise aos clientes Mass e Bronze, observamos que a taxa de churn permanece elevada em todas as províncias, variando entre 40,5% e 45,5%. Embora Hanói apresente a maior taxa (45,45%) e Bình Dương a menor (40,52%), a diferença entre as regiões é de apenas 5 pontos percentuais, indicando um comportamento relativamente homogêneo.

Esse resultado reforça que a localização geográfica não é o principal fator associado ao cancelamento. Independentemente da província, clientes pertencentes ao segmento Mass e ao nível de fidelidade Bronze apresentam elevada propensão à evasão. Assim, o churn parece estar muito mais relacionado ao baixo desenvolvimento do relacionamento com o banco do que a características regionais.

Esse achado fortalece os insights obtidos nas análises anteriores: o perfil de maior risco é composto por clientes Mass, Bronze, inativos, com baixo engajamento e baixa utilização de produtos, sugerindo que a principal oportunidade está em estratégias de ativação e aumento do uso do ecossistema bancário, e não em ações regionalizadas.

## Conclusão

O diagnóstico aponta que o desafio estratégico do banco não está em melhorar a aquisição de clientes, mas em acelerar sua evolução dentro do ecossistema. O churn concentra-se em clientes Bronze, inativos, com baixa utilização de produtos, baixo engajamento e menor capacidade financeira. Em outras palavras, trata-se de clientes que foram adquiridos com sucesso, mas que nunca desenvolveram um relacionamento consistente com a instituição.

Temos a oportunidade de mover o ponteiro com ações cirúrgicas e de baixo esforço para gerar grandes resultados. Ao atuar em recortes específicos trazidos por esta análise para sanar a evasão invisível de clientes qualificados que abandonam o banco por falta de vínculo, precisamos compreender profundamente esse relacionamento e estreitá-lo.

## Recomendações Estratégicas

Curto prazo – Reativação e migração digital de clientes inativos/offline
Implementar campanhas direcionadas especificamente aos clientes Bronze inativos e de perfil offline, utilizando canais alternativos, gatilhos de comunicação e incentivos voltados à ativação do primeiro acesso ao aplicativo e retorno ao uso da conta antes que a evasão se torne definitiva.
Médio prazo – Desenvolvimento do relacionamento e ancoragem de produtos
Estruturar jornadas de onboarding e engajamento com foco na ampliação do uso de produtos e serviços (como a adoção de cartões e novos serviços), incentivando a evolução dos clientes Bronze para os níveis Silver e Gold, segmentos nos quais o churn é significativamente menor. O objetivo é aumentar a integração do cliente ao ecossistema do banco, fortalecendo sua retenção no longo prazo.