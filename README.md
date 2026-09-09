# HIPE historical NER data

Multilingual historical documents annotated for **named entity recognition (NER)** and **entity linking (EL)**. This repository maintains an independent corrected version of the [HIPE-2022 dataset](https://github.com/hipe-eval/HIPE-2022-data).

## Start here

- **[v3.0 data](data/v3.0/)** — latest corrected version, with [release notes](data/v3.0/README.md).
- **[Curation guide](curation/README.md)** — reproduce corrections and audit annotations.
- **[Issue archive](curation/issues/)** — upstream reports and discussions.
- **[Original v2.1 data](data/v2.1/)** — retained for comparison; [v1.0](data/v1.0/) and [v2.0](data/v2.0/) are also available.

### What changed in v3.0?

Twenty annotation rows were corrected across French and German HIPE2020 training data and German NewsEye development data: person labels, nested entities, an organization link, and honorific titles. All 69 source data files are included; token text, document order, splits, and test annotations are preserved.

**Curation is ongoing.** Issue #20 and parts of #18 remain unresolved. See the [release notes](data/v3.0/README.md) for audit findings and limitations. This is an independent release, not an official HIPE organizers’ release.

## Datasets

The collection covers historical newspapers and classical commentaries in five languages. Follow each dataset link for its annotation scheme, sources, and references.

| Dataset | Documents | Languages | License |
| --- | --- | --- | --- |
| [AJMC](documentation/README-ajmc.md) | Classical commentaries | German, English, French | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| [HIPE2020](documentation/README-hipe2020.md) | Newspapers | German, English, French | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) |
| [LeTemps](documentation/README-letemps.md) | Newspapers | French | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) |
| [TopRes19th](documentation/README-topres19th.md) | Newspapers | English | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) |
| [NewsEye](documentation/README-newseye.md) | Newspapers | German, Finnish, French, Swedish | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |
| [SoNAR](documentation/README-sonar.md) | Newspapers | German | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) |

## File format

Data uses UTF-8 TSV files, organized by version, dataset, and language:

```text
data/v3.0/hipe2020/fr/HIPE-2022-v3.0-hipe2020-train-fr.tsv
```

Each token row has ten columns, in this order:

| Column | Content |
| --- | --- |
| `TOKEN` | Original token text |
| `NE-COARSE-LIT` | Coarse entity type, literal sense |
| `NE-COARSE-METO` | Coarse entity type, metonymic sense |
| `NE-FINE-LIT` | Fine entity type, literal sense |
| `NE-FINE-METO` | Fine entity type, metonymic sense |
| `NE-FINE-COMP` | Entity components, such as names, titles, and functions |
| `NE-NESTED` | Nested entity annotations |
| `NEL-LIT` | Literal Wikidata ID or `NIL` |
| `NEL-METO` | Metonymic Wikidata ID or `NIL` |
| `MISC` | Spacing, line/sentence boundaries, and partial-token offsets |

Entity tags use BIO notation: `B-` begins a mention, `I-` continues it, and `O` marks tokens outside that annotation layer. `_` marks unspecified or non-applicable values. Metadata lines start with `#` and identify documents, sources, and applicable columns; blank lines separate documents. Annotation layers and label sets vary by dataset.

Preserve document context when preparing training data: `EndOfSentence` can occur inside an entity. Use annotated train/dev splits for training and tuning; masked test files do not provide full supervision.

## Evaluation and citation

HIPE evaluates coarse NER (`NE-COARSE-LIT`), fine NER (`NE-FINE-LIT` and `NE-NESTED`), and linking (`NEL-LIT`). See the [participation guidelines](https://doi.org/10.5281/zenodo.6045662) for evaluation settings and the [statistics notebook](notebooks/hipe2022-datasets-stats.ipynb) for the original dataset analysis.

When using these data, cite **Ehrmann et al. (2022), [Extended Overview of HIPE-2022: Named Entity Recognition and Linking in Multilingual Historical Documents](https://doi.org/10.5281/zenodo.6979577)**, together with the relevant primary datasets. Report the data version and repository commit used in your experiments.

Original licenses and attribution requirements remain applicable; see [LICENSE](LICENSE) and the dataset documentation above. Credit belongs to the HIPE organizers and the contributing AJMC, HIPE2020, LeTemps, Living with Machines, NewsEye, and SoNAR projects.
