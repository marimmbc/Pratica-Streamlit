# Justificativa das métricas — Dashboard 2

## Métrica 1: Diabetes entre pessoas com obesidade
- **Variável:** `BMI` (IMC) e `Diabetes`
- **O que mede:** a porcentagem de pessoas com diabetes entre quem tem obesidade (IMC maior ou igual a 30), comparada com a porcentagem entre quem não tem obesidade. Conta como diabetes apenas a resposta `Yes` (pré-diabetes e diabetes gestacional ficam de fora).
- **Por que foi escolhida:** a obesidade é um dos fatores de risco mais conhecidos para o diabetes, e o IMC é uma informação simples de medir. Na base completa, cerca de 21% das pessoas com obesidade têm diabetes, contra cerca de 9% das que não têm.
- **Público-alvo:** gestores e equipes de saúde pública (por exemplo, atenção básica).
- **Qual decisão pode ser apoiada por essa métrica?** Priorizar exames de glicemia e programas de controle de peso para pessoas com obesidade, principalmente nos grupos de sexo e idade onde a diferença for maior.
- **O que comunica ao público-alvo:** "Entre as pessoas com obesidade, o diabetes é mais que o dobro do que entre as demais."

## Métrica 2: Diabetes entre quem não pratica exercícios
- **Variável:** `Exercise` e `Diabetes`
- **O que mede:** a porcentagem de pessoas com diabetes entre quem não pratica exercício físico, comparada com a porcentagem entre quem pratica.
- **Por que foi escolhida:** a falta de atividade física é um hábito que pode ser mudado, então a métrica aponta um ponto concreto de ação. Na base completa, cerca de 22% de quem não se exercita tem diabetes, contra cerca de 10% de quem se exercita.
- **Público-alvo:** gestores e equipes de saúde pública.
- **Qual decisão pode ser apoiada por essa métrica?** Investir em campanhas e programas de incentivo à atividade física, escolhendo os grupos de sexo e idade com a maior diferença.
- **O que comunica ao público-alvo:** "Quem não pratica exercícios tem diabetes com muito mais frequência do que quem pratica."

## Métrica 3: Doença cardíaca entre quem tem histórico de tabagismo
- **Variável:** `Smoking_History` e `Heart_Disease`
- **O que mede:** a porcentagem de pessoas com doença cardíaca entre quem já fumou (histórico de tabagismo), comparada com a porcentagem entre quem nunca fumou.
- **Por que foi escolhida:** o cigarro é um fator de risco conhecido para o coração e, assim como o exercício, é um hábito que pode ser mudado. Na base completa, cerca de 12% de quem tem histórico de tabagismo tem doença cardíaca, contra cerca de 6% de quem não tem.
- **Público-alvo:** gestores e equipes de saúde pública.
- **Qual decisão pode ser apoiada por essa métrica?** Reforçar programas para parar de fumar e o acompanhamento cardiológico de quem tem histórico de tabagismo.
- **O que comunica ao público-alvo:** "Quem já fumou tem cerca de duas vezes mais doença cardíaca do que quem nunca fumou."

## Métrica 4: Diabetes e doença cardíaca por categoria de IMC (gráfico de barras)
- **Variável:** `BMI` agrupado em categorias (abaixo do peso: < 18,5; normal: 18,5 a 24,9; sobrepeso: 25 a 29,9; obesidade: 30 ou mais), `Diabetes` e `Heart_Disease`
- **O que mede:** a porcentagem de pessoas com diabetes e a porcentagem com doença cardíaca em cada categoria de IMC, lado a lado.
- **Por que foi escolhida:** mostra de forma visual como as duas condições mudam conforme o peso aumenta, sem que o público precise interpretar números de IMC. Na base tratada, o diabetes vai de cerca de 6% na faixa normal para cerca de 21% na obesidade, e a doença cardíaca vai de cerca de 6% para cerca de 10%.
- **Público-alvo:** gestores e equipes de saúde pública.
- **Qual decisão pode ser apoiada por essa métrica?** Definir a partir de qual faixa de peso vale a pena intensificar a prevenção e o acompanhamento.
- **O que comunica ao público-alvo:** "A partir do peso normal, quanto maior a faixa de peso, mais pessoas têm diabetes e doença cardíaca. O diabetes é o que mais aumenta." (Quem está abaixo do peso também tem um pouco mais de doença cardíaca do que quem está no peso normal.)
