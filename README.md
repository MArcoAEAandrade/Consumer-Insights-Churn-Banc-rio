# Consumer-Insights-Churn-Banc-rio

A análise da nossa carteira revela que o churn geral está em 18% (14.400 clientes). O cliente que cancela apresenta uma idade média de 47 anos, sendo dois anos mais jovem do que quem permanece, enquanto o gênero não demonstrou relevância estatística.

De forma geral, a base apresenta uma carteira considerada de risco baixo e saudável, já que 93% (74.753) dos clientes estão nessa classificação. No entanto, quando cruzamos o churn com o risco, nos deparamos com um dado intrigante: 78% dos clientes que cancelaram estão classificados como risco baixo.

À primeira vista, isso sugeria que o banco estaria perdendo bons clientes de forma inexplicável. Porém, é lógico atestar esse volume sabendo que 93% da carteira geral é saudável — naturalmente, boa parte do churn também viria desse segmento.

O verdadeiro ponto crítico que precisamos destacar é que estamos prospectando clientes qualificados, mas falhamos em retê-los a longo prazo. Acredito que o desafio não está na qualidade da prospecção, mas na incapacidade de engajá-los ativamente.

Ao colocarmos uma lupa nesse grupo dos 78% e observarmos o nível de fidelidade e engajamento, percebemos que a maior parte desse churn de baixo risco (11.130 casos) se concentra nos níveis Bronze de fidelidade e entre membros inativos (especificamente 10.130 clientes no nível Bronze com membro_ativo = false). Ou seja, o cliente não possui um relacionamento estreito com o banco; na verdade, o grupo apresenta uma clara evasão silenciosa, com pouco tempo de relacionamento — inclusive menor do que nos demais segmentos (média de 1,8 anos) — e engajamento baixíssimo com a instituição (média de 16,48), respondendo também por cerca de 70% de todo o churn da carteira.

Perfil Predominante (Bronze e Inativo):

A esmagadora maioria do churn de baixo risco (10.130 clientes) concentra-se no nível Bronze com membro_ativo = false. Esse grupo apresenta um padrão claro de evasão silenciosa: entram com pouco tempo de relacionamento (média de 1,8 anos) e deixam a instituição com baixíssimo engajamento (média de 16,48).

A análise cruzada de produtos e engajamento expõe o verdadeiro antídoto contra o churn: a imersão no ecossistema de serviços. Enquanto os clientes ativos consomem uma média de 3,81 serviços, os que cancelam utilizam apenas 2,44. Esse padrão se reflete diretamente no engajamento (média de 34 para ativos contra 19 nos cancelados) e nas demais métricas de acompanhamento, que consistentemente aparecem mais baixas nos perfis que evadem.

Curiosamente, o tempo de relacionamento se mantém equivalente entre os grupos, provando que o cancelamento não se restringe à fase inicial de casa. Ao direcionarmos a lupa para o perfil Bronze, que concentra 87% da base total, o desafio se torna evidente: esse segmento responde por 97% de todo o churn do banco (14.020 dos 14.400 cancelamentos).

Quando cruzamos esse cenário com o risco, reforçamos a tese anterior: estamos prospectando com alta qualidade, mas falhamos em fazer com que esses clientes evoluam. Como o nível Bronze possui as menores médias de engajamento (18,8 para churns) e de serviços utilizados (2,41), o desafio central passa a ser criar trilhas de desenvolvimento para que o cliente avance para os níveis Silver e Gold, onde o churn é residual.



Quando adicionamos à leitura a média de saldo, a renda mensal e o escore de crédito, a diferença de capital se torna expressiva. Os clientes que ficam na instituição tendem a ser muito mais estáveis e possuem saldos substancialmente maiores. Desconsiderando o contexto da moeda, a proporção deixa claro que os clientes que dão churn possuem saldo médio e renda mensal praticamente três vezes menores em comparação aos que continuam ativos. O escore de crédito reflete exatamente a mesma lógica: quem vai embora possui uma pontuação média de 653 pontos, contra 691 dos ativos.

Ao aprofundarmos essa leitura de capital e escore filtrando especificamente para o perfil Bronze e cruzando por risco, o cenário se torna ainda mais evidente. Observamos que o grande volume da base (76,64% dos clientes, com saldo médio de 6.651.557 e score de 692) permanece ativo no baixo risco (segmento_risco = 0 e churn = 0).

No entanto, o ponto de atenção crítico reside nos clientes de baixo risco que evadem (segmento_risco = 0 e churn = 1), que representam 15,79% da base com saldo médio de 2.186.228 e score de 666,7. Já nos grupos classificados com risco mais alto (segmento_risco = 1), tanto os ativos quanto os que cancelam apresentam uma queda progressiva na renda e no escore de crédito (com pontuações médias de 601,9 e 604,6, respectivamente). A conclusão de negócio é que o risco de evasão está fortemente concentrado nos extremos de menor capital e menor escore dentro da base Bronze, reforçando a necessidade de ações direcionadas a esse público..


Por fim, olhando o status de membro ativo como principal variável de filtro, a esmagadora maioria dos cancelamentos vem de membros inativos, totalizando 13.283 clientes — o que equivale a 92% de todo o churn. Isso evidencia o poder dos clientes engajados: ser um membro ativo é a melhor vacina contra o cancelamento, já que apenas 1,40% dos que usam o banco com frequência decidem ir embora. Portanto, em vez de gastar energia tentando salvar toda a base de forma genérica, o foco deve ser direcionado a campanhas rápidas para acordar quem está com a conta parada antes que o encerramento aconteça de vez.

Para transformar este diagnóstico analítico em execução estratégica, devemos atuar em duas frentes complementares:

Curto Prazo (Reativação de Contas Paradas): Lançar campanhas e gatilhos de engajamento rápidos voltados para os membros inativos da base Bronze, buscando resgatar o vínculo antes que a evasão silenciosa se concretize em encerramento definitivo.

Médio Prazo (Onboarding no Ecossistema): Estruturar trilhas de desenvolvimento para guiar os novos clientes rumo à adoção de mais soluções (meta de superar o limiar crítico de serviços) e estimular sua progressão para os níveis Silver e Gold, onde a retenção é estruturalmente blindada.