<div align="center">

<h1>CiteSpectrum</h1>

<h3>Show Me How You Cite: Citation Fidelity, Usage, and Topology<br>in the Evidence Behavior of AI Scientific Writing</h3>

<p><b>A citation dataset spanning AI-generated and human-authored scientific writing.</b></p>

<p>Jihwan Oh &nbsp;·&nbsp; Gyeonghun Sun &nbsp;·&nbsp; Jisoo Kim &nbsp;·&nbsp; Yuho Lee &nbsp;·&nbsp; Taewon Yun &nbsp;·&nbsp; Jisu Shin &nbsp;·&nbsp; Hwanjun Song</p>

<p>Korea Advanced Institute of Science and Technology (KAIST) &nbsp;·&nbsp; Cluvion</p>

<p>
<img src="https://img.shields.io/badge/EMNLP_2026-Oral-6D4BC3?style=flat-square" alt="EMNLP 2026 Oral">
<a href="data/README.md"><img src="https://img.shields.io/badge/Dataset-78%2C016_citation_events-287B74?style=flat-square" alt="78,016 citation events from 550 paper entries"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/Annotations-CC_BY--NC_4.0-476C9B?style=flat-square" alt="CiteSpectrum annotations: CC BY-NC 4.0"></a>
</p>

<p>
<b>Paper</b> &nbsp;·&nbsp;
<a href="data/README.md"><b>Browse papers</b></a> &nbsp;·&nbsp;
<a href="#download"><b>Download</b></a>
</p>

<a href="assets/overview.pdf"><img src="assets/overview.svg" width="100%" alt="CiteSpectrum study overview: five levels of AI involvement, three dimensions of citation behavior, and citation-based AI paper detection"></a>

</div>

---

**CiteSpectrum** provides citation-level data from **450 surveys and 100 method papers**. The survey collection covers five writing conditions with **GPT-5.4** and **Qwen3-Next-80B-A3B-Instruct**, paired across the same 50 source topics.

| Five writing conditions | Two model families | 450 unique surveys | 14 domains |
|:---:|:---:|:---:|:---:|
| From LLM-Only to Human-Authored | GPT-5.4 · Qwen3-Next-80B | 400 AI-involved + 50 human | Paired by source topic |

## Survey settings

Each step adds a different form of guidance. The source topic stays fixed, so papers can be compared across conditions using the same source ID.

| Condition | What guides the writing? | GPT-5.4 | Qwen3-Next-80B |
|:---|:---|:---:|:---:|
| **LLM-Only** | Topic; the model supplies references, structure, and prose from parametric knowledge | [50 surveys](data/survey/gpt54/llm-only) | [50 surveys](data/survey/qwen80b/llm-only) |
| **RAG** | Topic and retrieved scholarly literature | [50 surveys](data/survey/gpt54/rag) | [50 surveys](data/survey/qwen80b/rag) |
| **Outline-Guided** | Human-authored outline and reference pool | [50 surveys](data/survey/gpt54/outline-guided) | [50 surveys](data/survey/qwen80b/outline-guided) |
| **Text-Guided** | Human-authored prose and reference pool; the model restores citations | [50 surveys](data/survey/gpt54/text-guided) | [50 surveys](data/survey/qwen80b/text-guided) |
| **Human-Authored** | Original human-authored survey | [50 surveys](data/survey/human-authored) | [50 surveys](data/survey/human-authored) |

The survey collection contains **69,983 citation events from 450 surveys**, stored as per-paper `citations.jsonl` files. The **same 50 human surveys** serve as the baseline for both models and are stored once in `human-authored/`. Source IDs `001`–`050` pair the same topics across all conditions and models.

## Released data

**78,016 citation events across 550 papers.** Each paper directory contains only `citations.jsonl`.

| Collection | Papers | Browse |
|:---|---:|:---|
| **Survey** · GPT-5.4 | 200 | [Four writing conditions](data/survey/gpt54/) |
| **Survey** · Qwen3-Next | 200 | [Four writing conditions](data/survey/qwen80b/) |
| **Survey** · Human | 50 | [Human baseline](data/survey/human-authored/) |
| **Method** · AI | 50 | [AI methods](data/methods/ai/) |
| **Method** · Human | 50 | [Human methods](data/methods/human/) |
| **Total** | **550** | [Full paper titles](data/README.md) |

[Browse all paper titles](data/README.md)

## Download

```bash
git clone --depth 1 https://github.com/DISL-Lab/CiteSpectrum.git
```

The dataset is in `CiteSpectrum/data/`.

## License

CiteSpectrum annotations and original generated survey prose: [CC BY-NC 4.0](LICENSE). Original excerpts and upstream materials retain their [source licenses and author credits](data/SOURCES.md).

## Citation
