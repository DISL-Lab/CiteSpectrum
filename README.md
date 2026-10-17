<div align="center">

<h1>CiteSpectrum</h1>

<h3>Show Me How You Cite: Citation Fidelity, Usage, and Topology<br>in the Evidence Behavior of AI Scientific Writing</h3>

<p><b>Tracing how AI uses scientific evidence, from model-only writing to human authorship.</b></p>

<p>Jihwan Oh &nbsp;·&nbsp; Gyeonghun Sun &nbsp;·&nbsp; Jisoo Kim &nbsp;·&nbsp; Yuho Lee &nbsp;·&nbsp; Taewon Yun &nbsp;·&nbsp; Jisu Shin &nbsp;·&nbsp; Hwanjun Song</p>

<p>Korea Advanced Institute of Science and Technology (KAIST) &nbsp;·&nbsp; Cluvion</p>

<p>
<img src="https://img.shields.io/badge/EMNLP_2026-Oral-6D4BC3?style=flat-square" alt="EMNLP 2026 Oral">
<a href="data/README.md"><img src="https://img.shields.io/badge/Dataset-78%2C016_citation_events-287B74?style=flat-square" alt="78,016 citation events from 550 paper entries"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/Annotations-CC_BY_4.0-476C9B?style=flat-square" alt="CiteSpectrum annotations: CC BY 4.0"></a>
</p>

<p>
<b>Paper</b> &nbsp;·&nbsp;
<a href="data/README.md"><b>Browse papers</b></a> &nbsp;·&nbsp;
<a href="#download"><b>Download</b></a>
</p>

<a href="assets/overview.pdf"><img src="assets/overview.svg" width="100%" alt="CiteSpectrum study overview: five levels of AI involvement, three dimensions of citation behavior, and citation-based AI paper detection"></a>

<details>
<summary><b>Enlarged views of the study design</b></summary>
<p><a href="assets/overview-spectrum.pdf"><img src="assets/overview-spectrum.svg" width="65%" alt="Enlarged panel A: the five levels of AI involvement"></a></p>
<p><a href="assets/overview-analysis.pdf"><img src="assets/overview-analysis.svg" width="100%" alt="Enlarged panel B: citation fidelity, usage, and topology"></a></p>
<p><a href="assets/overview-detection.pdf"><img src="assets/overview-detection.svg" width="65%" alt="Enlarged panel C: citation-based AI paper detection"></a></p>
</details>

</div>

---

**CiteSpectrum** studies how scientific writing changes as AI involvement varies. Starting from the same 50 source surveys, we compare five writing conditions with **GPT-5.4** and **Qwen3-Next-80B-A3B-Instruct**, keeping source topics paired across the spectrum. We analyze citations through **fidelity**, **usage**, and **topology**, and show that these behaviors carry an interpretable signal for identifying AI-generated papers.

| Five writing conditions | Two model families | 450 unique surveys | 14 domains |
|:---:|:---:|:---:|:---:|
| From LLM-Only to Human-Authored | GPT-5.4 · Qwen3-Next-80B | 400 AI-involved + 50 human | Paired by source topic |

## The AI involvement spectrum

Each step adds a different form of guidance. The source topic stays fixed, so papers can be compared across conditions using the same source ID.

| Condition | What guides the writing? | GPT-5.4 | Qwen3-Next-80B |
|:---|:---|:---:|:---:|
| **LLM-Only** | Topic; the model supplies references, structure, and prose from parametric knowledge | [50 surveys](data/survey/gpt54/llm-only) | [50 surveys](data/survey/qwen80b/llm-only) |
| **RAG** | Topic and retrieved scholarly literature | [50 surveys](data/survey/gpt54/rag) | [50 surveys](data/survey/qwen80b/rag) |
| **Outline-Guided** | Human-authored outline and reference pool | [50 surveys](data/survey/gpt54/outline-guided) | [50 surveys](data/survey/qwen80b/outline-guided) |
| **Text-Guided** | Human-authored prose and reference pool; the model restores citations | [50 surveys](data/survey/gpt54/text-guided) | [50 surveys](data/survey/qwen80b/text-guided) |
| **Human-Authored** | Original human-authored survey | [50 shared surveys](data/survey/human-authored) | [50 shared surveys](data/survey/human-authored) |

The survey collection contains **69,983 citation events from 450 surveys**, stored as per-paper `citations.jsonl` files. The **same 50 human surveys** serve as the baseline for both models and are stored once in `human-authored/`. Source IDs `001`–`050` pair the same topics across all conditions and models.

## What citation behavior reveals

We organize **11 citation-behavior feature groups** along three complementary dimensions.

| Dimension | Question | Feature groups |
|:---|:---|:---|
| **Fidelity** | Do references exist, and do they support the claims? | Ghost reference rate, evidence grounding, evidence provenance |
| **Usage** | What role does a citation play in the argument? | Citation purpose, citation stance |
| **Topology** | How are references selected, reused, and connected? | Reference age, venue diversity, field diversity, citation count, repetition, network clustering |

**Retrieval resolves fabricated references, but grounding still needs guidance.** Ghost reference rates fall from 79.2% in LLM-Only to 0.4% in RAG. Yet 36% of RAG citation instances remain unsupported, compared with 14% in Human-Authored writing.

**Human prose changes citation usage.** RAG and Outline-Guided writing cite predominantly as affirmative evidence. Text guidance brings citation purpose and stance closer to human writing, including a larger share of neutral citations.

<table>
<tr>
<td width="50%" align="center" valign="top"><a href="assets/fidelity.pdf"><img src="assets/fidelity.svg" alt="Citation fidelity: evidence grounding and evidence provenance across writing conditions" width="100%"></a><br><sub><b>Fidelity:</b> stronger guidance improves grounding.</sub></td>
<td width="50%" align="center" valign="top"><a href="assets/usage.pdf"><img src="assets/usage.svg" alt="Citation usage: purpose and stance distributions across writing conditions" width="100%"></a><br><sub><b>Usage:</b> human prose changes how evidence is used.</sub></td>
</tr>
</table>

**AI reference networks remain broader and less interconnected.** AI-involved surveys span more venues and fields and favor highly cited references, while human reference networks show stronger clustering. Text guidance only partially closes these structural gaps.

<p align="center"><a href="assets/topology.pdf"><img src="assets/topology.svg" width="100%" alt="Six citation topology features: reference age, venue diversity, field diversity, citation count, repetition rate, and clustering coefficient"></a><br><sub>Figures reproduced from the paper. Click any figure to zoom in its vector PDF. <a href="assets/README.md">Download full-resolution figures.</a></sub></p>

## Citation-based AI paper detection

A lightweight **Citation-MLP** uses citation behavior to distinguish AI-involved from human-authored papers. In the paper's binary detection experiment, it achieves **0.880 balanced accuracy** and **0.944 AUROC**, outperforming all six text-based baselines.

| Method | Balanced accuracy | Macro-F1 | AUROC |
|:---|---:|---:|---:|
| Qwen3-80B-Inst. | 0.626 | 0.506 | 0.650 |
| Fast-DetectGPT | 0.611 | 0.542 | 0.674 |
| EditLens | 0.660 | 0.471 | 0.787 |
| Pangram | 0.844 | 0.731 | 0.816 |
| DistilBERT | 0.775 | 0.763 | 0.882 |
| Llama-3.2-3B | 0.793 | 0.792 | 0.924 |
| **Citation-MLP (Ours)** | **0.880** | **0.876** | **0.944** |

Results are from Table 4 of the paper, using domain-balanced five-fold cross-validation on 350 AI-generated and 100 human-authored papers. The data release includes both the survey and method-paper collections.

## Released data

**78,016 citation events across 550 papers.** Each paper directory contains only `citations.jsonl`.

| Collection | Papers | Citation events | Browse |
|:---|---:|---:|:---|
| GPT-5.4 surveys | 200 | 37,002 | [Four writing conditions](data/survey/gpt54/) |
| Qwen3-Next-80B-A3B-Instruct surveys | 200 | 19,262 | [Four writing conditions](data/survey/qwen80b/) |
| Shared Human-Authored surveys | 50 | 13,719 | [Human baseline](data/survey/human-authored/) |
| AI method papers | 50 | 2,415 | [AI methods](data/methods/ai/) |
| Human method papers · ICLR 2026 Oral | 50 | 5,618 | [Human methods](data/methods/human/) |
| **Total** | **550** | **78,016** | [Full paper titles](data/README.md) |

[Browse all paper titles](data/README.md)

## Download

```bash
git clone --depth 1 https://github.com/DISL-Lab/CiteSpectrum.git
```

The dataset is in `CiteSpectrum/data/`.

## License and attribution

CiteSpectrum annotations and original generated survey prose: [CC BY 4.0](LICENSE). Original excerpts and upstream materials retain their [source licenses and author credits](data/SOURCES.md).

## Citation
