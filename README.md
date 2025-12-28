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
    - Blazegraph as Triple Store DB (if needed)


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
    8) Extra: Agentes colaborativos (role-playing)

Avaliação bi-modal
A avaliação deve ser bi-modal, implementando avaliações automatizadas onde viável e utilizando Experts para avaliação qualitativa onde as opções automatizadas tem dificuldade. Avaliações automatizadas são importantes para a escalabilidade do processo avaliativo e enriquecimento dos resultados da pesquisa.

Própria e técnica:
    - Consistência Lógica: Automatizado?(e.g., HermiT, Pellet, FaCT++)
    - Completeness : Recursão Agêntica? Ontologias ouro.
    - Syntaxe RDF + OWL : Bibliotecas disponíveis para validação
    - Frameworks? : OQuaRE (Ontology Quality Re-engineering) / OOPS! (Ontology Pitfall Scanner)
    - Métricas avaliativas para sub-tarefas do framework em cima da datasets de benchmark : Precision, Recall, F1
    - Profundidade e complexidade de estrutura : profundidade das hierarquias de classes, número de propriedades criadas, densidade das interconexões
Externa e Qualitativa (por Experts) - Aproveitar e fazer um estudo comparativo entre role-playing agents versus experts humanos?:
    - Precisão semântica :
    - Escolhas de modelagem : 
    - Usabilidade : 
    - Completude em requisitos implicitos :     


Github Saeedizade et al. ESWC 2024: https://github.com/LiUSemWeb/LLMs4OntologyDev-ESWC2024?tab=readme-ov-file



## Usage

### Full Workflow (Generate all 15 CQs)
```bash
python otho.py --story-id MusicS
```

Generates OWL for each CQ, validates, combines, and attempts to fix any OOPS pitfalls automatically.

### Skip-to-Combine (Checkpoint from existing OWL files)
When you already have all 15 CQ OWL files and want to test combination/validation only:
```bash
python otho.py --story-id MusicS --skip-to-combine
```

**Requirements:** Existing validated OWL files in `data/output/{story_id}_{cq_id}.owl` format.

**What it does:**
- Loads existing OWL files
- Skips CQ generation
- Runs combination and validation phases
- **Automatically corrects OOPS pitfalls** (up to 5 attempts)
- Saves each correction attempt for auditing

**Automatic Pitfall Correction:**
The workflow now detects and attempts to fix all OOPS pitfalls (P08, P13, P22, P24, etc.) automatically. Each correction attempt is saved as `{story_id}_combined_turtle_correction_{attempt}.owl` for review.

## Env Setup
### OOps Pitfall Scanner
1) docker run -p 80:8080 mpovedavillalon/oops:v1
2) Download and mount Wordnet and run: docker run -v ./WordNet:/usr/local/tomcat/WordNet -p 80:8080 mpovedavillalon/oops:v1
3) Then go to http://localhost/OOPS/
