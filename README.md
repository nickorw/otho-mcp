# Otho

Proposta de projeto - Otho

Visão
O melhor gerador de ontologias em OWL para negócios com base em LLM e Agentes de IA

Objetivos
- Superar o state-of-the-art em geração de ontologias em OWL no domínio de negócios
- Equiparar com atual state-of-the-art overall

Hipótese
O uso concomitante de LLMs de ponta associados a Agentes de IA e human-in-the-loop permite melhorar o processo de 
engenharia de ontologias acima da competição.

Definições:

    Tecnologia
    - Uso de Python: Agilidade, bibliotecas de AI amplamente disponíveis, requerimento de cadeira
    - Uso de LangGraph como framework de agentes: LangGraph permite definição de workflows entre agentes bem definidos enquanto permitindo flexibilidade de customização e ampla comunidade e maturidade.
    - Uso de RDF/OWL como tecnologia para Knowledge Graphs: requerimento de interesse, uso de indústria.
    - Uso de Gemini Flash 2.0 como LLM: Disponibilidade para o pesquisador e performance


Etapas de projeto de pesquisa
    1) Pesquisa exploratória em search engines de casos similares
    2) Identificação de experimentos competidores
    3) Identificação de benchmarks
    4) Validação do objetivo de projeto
    5) Design preliminar do sistema
    6) Execução da implementação e registro de passos

Etapas de projeto de desenvolvimento

    Gerar Ontologias OWL válidas através de LLM
    1) Gerar com prompt via chat
    2) Gerar através de aplicação Python via API
    3) Gerar através de Agente LangGraph
    4) Gerar através de aplicação multi-agente LangGraph 
    5) Gerar via chat com prompt e documento de texto com contexto/Competency Questions(CQs)
    6) Gerar através de aplicação LangGraph com prompt e documento de texto com contexto/Competency Questions(CQs)

    7) Extra: Gerar ontologias OWL válidas utilizando LLM através de aplicação multi-agente LangGraph com contexto adicionado genérico de negócios

