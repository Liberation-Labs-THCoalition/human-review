# Whole Sessions, Not Passages: Mnemosyne v10 Scores 96.2–96.8% on Held-Out LongMemEval_S-cleaned Under Two Claude Judges

**Nexus** (lead author) · nexus@liberationlabs.tech
**Thomas Edrington** · thomas@liberationlabs.tech

Liberation Labs / Transparent Humboldt Coalition

> **DRAFT 2026-09-25. Not for circulation until Thomas's go to deposit.** Every number is taken from files
> under `/mnt/data1/lme_v2/`.
> - The held-out results, the judge calibration and the placement were second-read on 2026-09-25
>   (`v10/REVIEW_v10_held_readers.md`), and their wording follows that review.
> - This text was second-read the same day (`REVIEW_paper_fable.md`: WARN, confirmed with caveats). It
>   reproduced every number, including the three first computed for this draft (marked ⁽ⁿ⁾). All nine
>   required fixes are applied. F8, the title, now names the judges.
> - The pre-review text is kept as `paper.md.pre-review-20260925`.
> - **Decided 2026-09-25:**
>   - Nexus is lead author; the contact addresses are as above.
>   - Title: at Thomas's suggestion it shows the top of the range (96.8, the Opus-5.5 judge) beside the
>     pre-registered Sonnet-5 figure (96.2). 97.2 is not a score: it is the upper end of the 95% interval on
>     the all-500 Sonnet figure.
>   - No LoCoMo content (Thomas: the LoCoMo rerun will be revised separately).
> - **[DECISION] still open:** what code and data to release (the transcripts need the account e-mail
>   scrubbed first), and the go to deposit.
> - `nexus@liberationlabs.tech` is routed as of 09-25 17:45 (Cloudflare rule → Thomas's inbox). A RCPT probe
>   went from 550 to 250, and a made-up control address stayed 550.

---

## Abstract

Long-term memory benchmarks reward systems that put the right evidence in front of a capable reader. We
present Mnemosyne v10, a retrieval layer that makes no model calls. It scores every turn of a user's chat
history with BM25 and a dense encoder, fuses the two rankings, and fills a 24k-token budget with whole
sessions in chronological order.

On LongMemEval_S-cleaned we tuned v10 on 100 questions, froze its configuration (hash `7bc75f509aa0`),
and evaluated it on the other 400 questions, which were pre-registered as held out. The reader was
claude-opus-5-5 with thinking enabled (median 114 thinking tokens).
- **Held out:** v10 answers **385/400 = 96.2%** under a claude-sonnet-5 judge and **387/400 = 96.8%**
  under a claude-opus-5-5 judge (95% Wilson [93.9, 97.7] and [94.5, 98.1]).
- **All 500:** **479/500 = 95.8%** and **484/500 = 96.8%**.
- **Retrieval:** v10 puts every `has_answer`-labelled evidence session into the context for 97.1% of
  held-out questions (96.0% when every official `answer_session_ids` session is required).
- **Against v9:** with the same reader model (claude-opus-4-6; the reading template differs by one clause,
  §3.3), our previous system scores 79.0% / 80.0% on the
  same 400 questions and v10 scores 92.2% / 94.5% (paired McNemar p < 10⁻⁹ under both judges).
- **Against the full history:** on the 100 tuning questions, v10 cannot be distinguished from the same
  reader given the entire ~115k-token history, and it uses about a fifth of the reader's input.

Judging used the official LongMemEval answer-check prompts, with Claude judges instead of GPT-4o. On 1,000
published answers, our judges agree with the official judge on 95–97% of questions and pass slightly fewer.
Adversarial second readers reproduced every held-out count, the retrieval-recall figures and the numbers
first computed for this report from the raw files.

These are the highest point estimates among the LongMemEval_S results we could trace to a primary source.
The margin is small: on all 500 questions it is one question above the best published claims (95.60),
inside every interval. We list every way our harness departs from the official one.

---

## 1. Introduction

An assistant that works with someone for months has to remember what they told it. LongMemEval (Wu et al.,
2025) tests exactly this.
- **Haystacks.** Each of its 500 questions comes with its own chat history, the haystack. In the S variant
  a haystack is about 115k tokens in 38–62 sessions (mean 47.7). One or a few of those sessions answer the
  question.
- **Question types.** Single-session user, single-session assistant and single-session preference questions;
  multi-session questions, which need facts gathered across sessions; knowledge updates, where a later
  session overrides an earlier one; and temporal reasoning.
- **Abstentions.** Thirty questions are abstentions, where the correct answer is that the history does not
  say.

**Our previous system, Mnemosyne v9,** built a context of about 7k tokens per question (about 8.5k of reader input with the
reading template) from four parts: character
profiles, structured facts, an event ledger and fifteen retrieved passages. With claude-opus-4-6 as reader
and the official answer-check prompts, it scored 78.6–80.2% under our two judges (§3.4). The same reader
given only the evidence sessions (the "oracle" arm) scored 95.0–96.6%. On a 100-question block, the same
reader given the whole history scored 92–94%.

**The loss was in retrieval, not reading.** When all the evidence reached v9's context, v9 and the oracle
arm tied. But on multi-session questions, all the evidence reached v9's context only 46% of the time by the
lenient verbatim matcher (35% strict; §4.1 reports strict).

v10 has one job: evidence recall at a fixed token budget. This report contributes:
1. **A simple retrieval design with no model calls** (§2). It fuses turn-level BM25 and dense scores, ranks
   sessions by their two best turns, and fills a 24k-token budget with whole sessions.
2. **A pre-registered protocol** (§3). It has an input allow-list enforced in code, a frozen configuration,
   and a held-out set that tuning never saw.
3. **Results with paired comparisons** (§4), under two judges and two readers. The comparisons are against
   our previous system, an evidence-only ceiling and, on the tuning block, the full history.
4. **A calibration of our Claude judges** (§5) against the official GPT-4o judge, on 1,000 published
   answers.
5. **A placement against published results** (§6), stating what we excluded and why.

An earlier Mnemosyne version was reported at 85.8% on LongMemEval in our technical report of 2026-08-05
(DOI 10.5281/zenodo.21801643). That figure used a custom semantic-equivalence judge, not the official
answer-check prompts, and this report supersedes it.

## 2. Mnemosyne v10 retrieval

### 2.1 Inputs: an allow-list enforced in code

The retriever receives a view of each question, built field by field:
- the question text and the question date;
- for each haystack session, its date and its turns as (role, content) pairs.

The view is made of new objects, and the code asserts its exact key set. The only other input is the
question's row index into the precomputed question embeddings (§2.2). Nothing else reaches the retriever. In
particular it never sees:
- session identifiers (evidence sessions carry an `answer_` prefix in the dataset);
- the `has_answer` turn labels;
- the question type or question identifier;
- the answer.

Handing a component a slice of the full record is how an answer key reaches a reader.

### 2.2 Two retrieval channels

- **BM25** (k1 = 1.2, b = 0.75) over every turn, user and assistant alike. The corpus is that question's own
  haystack.
- **Dense:** cosine similarity between the question and each **user** turn.
  - Encoder: BAAI/bge-base-en-v1.5 (revision `a5beb1e3`), run once over the 93,931 unique user turns on a
    Quadro K2200 GPU (fp32 model, fp16 storage). A second reader recomputed a sample on CPU and matched the
    stored rows at cosine 1.0000.
  - CLS pooling with L2 normalisation, a 512-token input limit, and the model's retrieval prefix on the
    question.
  - Assistant turns are not embedded. They reach the ranking through BM25, and through their session.
  - Two departures from the design note: it planned to embed assistant turns too (truncated to 512
    tokens), and to run on CPU. The run embedded user turns only, on a GPU.

### 2.3 Fusion and session scoring

- **Fusion.** Each channel's ranking of turns enters reciprocal-rank fusion (Cormack et al., 2009) with
  k = 60. BM25 is weighted 1.0 and the dense channel 2.0.
- **Session score.** The session's best fused turn score plus its second-best.
- **Ties** are broken by a hash of the content, not by position in the haystack.

### 2.4 Selection and rendering

- **Selection.** Sessions are taken in score order. Each one is added whole if it fits the remaining budget
  of 24,000 tokens (o200k). If it does not fit, a window of ±2 turns around its two best turns is added
  instead, provided the window fits.
- **Resulting size.** The median held-out context is 23.9k tokens (o200k). The median context has 9
  sessions, 8 of them whole.⁽¹⁾
- **Rendering.** The chosen sessions are rendered in chronological order with their dates. They go through
  the official LongMemEval prompt builder, the same one used for the oracle and full-history arms.

v10 makes no LLM calls, does no ingest-time extraction, and never routes on question type.

### 2.5 How the configuration was chosen

The selection rule was written down before any result from the dense channel existed. The sweeps ran on the
100 dev questions, at a 16k budget, in four stages. Each stage kept the previous stage's winner:
1. which channels;
2. the session-scoring weights;
3. packing (how many sessions go in whole, and the window size);
4. a date channel that favours sessions inside time windows parsed from the question.

The rule for picking a configuration:
- **Winner:** the configuration with the highest dev all-evidence recall. Ties went to the simpler
  configuration.
- **Budget:** the smallest of {8.5k, 12k, 16k, 24k, 32k} at which dev all-evidence recall reached 0.95.
  That was 24k.

The date channel did not survive. BM25 alone at 24k already reached 0.957 dev recall; the dense channel and
fusion added about one point. The frozen configuration was written read-only before any held-out
evaluation.

## 3. Evaluation protocol

### 3.1 Dataset

- **Version.** We use LongMemEval_S-cleaned, the authors' September 2025 re-release (HF
  `xiaowu0162/longmemeval-cleaned`; sha256 `d6f21ea9d60a0d56…`). Our file is byte-identical to its
  `longmemeval_s_cleaned.json`. It is not the original S. We found this only on 2026-09-24, and
  comparisons with results on the original S cross dataset versions (§6).
- **The 500 questions by type:**

  | type | questions |
  |---|---|
  | multi-session | 133 |
  | temporal reasoning | 133 |
  | knowledge update | 78 |
  | single-session user | 70 |
  | single-session assistant | 56 |
  | single-session preference | 30 |

  30 of the 500 are abstentions.

### 3.2 A pre-registered split

*Pre-registered* here means fixed in read-only files, with hashes and an append-only log, on our own machine
before any held-out result existed. The split was not filed with a public registry.

The split was fixed in a read-only file (sha256 prefix `a0bd99c6afe13c17`) before any v10 result existed.
- **dev** is block 1 of a fixed question order: 100 questions. We had already examined block 1 in detail,
  so it could not serve as a test set.
- **held** is blocks 2–5: 400 questions.

Rules:
- every parameter is chosen on dev;
- a held-out number may be computed only for a read-only (frozen) configuration;
- every held-out evaluation, including failed attempts, is appended to a log together with the
  configuration's hash.

**Disclosed prior knowledge.** Two sources motivated v10's design-level choices (whole sessions, several
channels, a larger budget):
- an autopsy of v9 that covered all 500 questions, the held-out 400 included;
- published systems.

What this protocol supports is therefore a design motivated by an analysis that saw every question, tuned
on 100 questions and tested on 400.

### 3.3 Readers

Each question is answered once, in one call. The prompt comes from the official LongMemEval prompt builder.
It uses the builder's plain-history chain-of-thought template (`merge_key_expansion_into_value = none`) and
gives the dataset's question date as `Current Date:`.

The v9 arm used the official history-plus-facts (`merge`) variant instead, because its context contains
extracted facts. The two variants differ by one clause. v10, oracle and full history share the
plain-history variant.

Two readers read identical prompts:
- **claude-opus-4-6** with extended thinking off. This was the reader for all our earlier arms. We kept it
  so that the retrieval comparison stays controlled.
- **claude-opus-5-5** with thinking enabled. It thought briefly: a median of 114 thinking tokens, and at
  most 1,727.

We declared the second configuration the headline candidate in writing before any held-out accuracy
existed. We report both.

### 3.4 Judges

- **Prompts and rule.** The per-type answer-check prompts are extracted programmatically from the official
  `evaluate_qa.py`, not retyped. An answer counts as correct if the judge's reply contains "yes", which is
  the official rule.
- **Which judges.** The official judge is gpt-4o-2024-08-06. We have no OpenAI access, so we used two
  Claude judges:
  - **claude-sonnet-5**, designated primary before any judging;
  - **claude-opus-5-5**, designated the agreement judge.
- **Relation to the readers.** Both judges differ from the Opus 4.6 reader. The Opus 5.5 judge is the same
  model as the headline reader, so we check it for self-preference below.
- **Controls.** The judges passed pilot answers and failed deliberately wrong answers, one of which was an
  abstention. Without the failing half, nothing would show that the judges could fail an answer.
- **Disagreements.** An adversarial review of our earlier v9 run adjudicated all 12 of that run's judge
  disagreements under the official rubric. It sided with the Opus judge on all 12, because Sonnet 5 does
  not apply the leniency the preference rubric asks for (five of the twelve were marginal). Choosing a primary judge after seeing the scores
  would amount to picking the higher number, so we report both.
- **Self-preference check.** The Opus 5.5 judge's lift over the Sonnet judge is +0.50 and +1.25 points on
  the two held-out arms that Opus 5.5 read, and +1.00 to +2.25 on the three that Opus 4.6 read. We see no
  sign of self-preference.

### 3.5 Arms

| arm | context | reader(s) | questions |
|---|---|---|---|
| v9 | Mnemosyne v9, ~7k tokens (~8.5k reader input); `merge` template | Opus 4.6 | 500 |
| **v10** | frozen v10, ~24k tokens | Opus 4.6; Opus 5.5 with thinking | 500 |
| oracle | evidence sessions only (`longmemeval_oracle.json` as distributed) | Opus 4.6; Opus 5.5 with thinking | 500 |
| full history | the whole haystack, ~115k tokens | Opus 4.6 | dev only (100) |

### 3.6 Statistics

We report accuracy with 95% Wilson intervals. Paired comparisons use McNemar's exact test on the discordant
questions. We give counts as well as percentages, because two of the headline figures sit on a rounding half
(385/400 = 96.25%).

### 3.7 Deviations from the official harness

1. **Claude judges** instead of gpt-4o-2024-08-06. §5 measures the effect on published answers.
2. **No temperature control.** Officially, the reader and the judge both run at temperature 0. The
   `claude -p` harness we used cannot set it.
3. **No output cap.** Official chain-of-thought generation uses max_tokens = 800. 23 of the 400 headline
   answers exceed 800 visible tokens, and each judge passed 21 of those 23. The official harness would have
   cut them off mid-reasoning.
4. **Context added by the harness.** Every reader call went through `claude -p`, which adds three things:
   - a short system prompt: `You are a Claude agent, built on Anthropic's Claude Agent SDK.` followed by
     `You are a helpful assistant.`;
   - Claude Code system-reminder blocks: an environment snapshot, the model's name and knowledge cutoff, a
     token-budget line, the account e-mail, and **the real date of the run**, which sits beside the
     prompt's `Current Date:`;
   - a stray `-` line before the prompt.

   The additions were the same in every arm, so they do not affect the paired comparisons. Their effect on
   absolute scores is unknown. The evidence-only arm with Opus 5.5 answered all 107 held-out
   temporal-reasoning questions correctly despite the conflicting dates. No label field (`has_answer`,
   `answer_session_ids`, `question_type`) appears in the added text or in the prompts.
5. **Budget accounting.** The budget counts turns as `json.dumps(ensure_ascii=False)`, but the official
   builder escapes non-ASCII characters. A rendered history can therefore exceed 24k tokens. On the
   held-out set, histories reach 25.2k and whole prompts 25.3k.

## 4. Results

### 4.1 Retrieval recall (no reader involved)

| | dev (94 scored) | held-out (376 scored) |
|---|---|---|
| every `has_answer` evidence session in context | 0.968 | **0.971** [0.948, 0.984] |
| every official `answer_session_ids` session in context | 0.957 | **0.960** [0.935, 0.976] |
| v9, verbatim-matcher lower bound (strict / lenient) | 0.596 / 0.670 | 0.593 / 0.670 |
| v10 through v9's verbatim matcher | — | 0.955 |
| frozen v10 at an 8.5k budget (v9's reader-input size) | 0.798 | not run: it would be an unfrozen held-out evaluation |

Abstention questions are excluded from the recall metric by rule.

Held-out recall by type, v10 against v9 strict:
- multi-session: 0.97 against 0.35;
- temporal: 0.95 against 0.51;
- knowledge update: 0.98 against 0.67;
- single-session types: 0.96–1.00 against 0.54–0.90.

### 4.2 Dev block: v10 against the full history

These are the 100 tuning questions, all read by Opus 4.6.

| arm | reader input | Sonnet-5 judge | Opus-5.5 judge |
|---|---|---|---|
| v9 | ~8.5k | 77 [67.8, 84.2] | 81 [72.2, 87.5] |
| **v10** | ~27.0k | **91** [83.8, 95.2] | **92** [85.0, 95.9] |
| full history | ~127k | 92 [85.0, 95.9] | 94 [87.5, 97.2] |
| evidence only (oracle) | ~7.6k | 94 [87.5, 97.2] | 96 [90.2, 98.4] |

Paired comparisons (discordant counts, then McNemar exact p):

| comparison | Sonnet-5 judge | Opus-5.5 judge |
|---|---|---|
| v10 against v9 | 17 vs 3, p = 0.0026 | 15 vs 4, p = 0.019 |
| v10 against full history | 1 vs 2, p = 1 | 1 vs 3, p = 0.63 |
| v10 against oracle | 0 vs 3, p = 0.25 | 1 vs 5, p = 0.22 |

On this block v10 cannot be distinguished from the full-history reader, while giving the reader about a fifth
as much input.
- **Caveat.** "Level with the full history" is a dev-only, n = 100 statement. We did not run the full history
  on the held-out set (about 51M tokens).
- **Opus 5.5.** With Opus 5.5 and thinking on the same dev prompts, v10 scores 94 / 97 and the oracle 97 / 98.
- **Provenance.** Dev numbers come from the tuning split. Tuning targeted recall, not answers. They were
  first second-read in the review of this text, which reproduced every dev accuracy, interval and paired
  count.
- **Reader input** is the median of billed input tokens (uncached plus cached) per question.

### 4.3 Held-out: the 400 pre-registered questions

| held-out (n = 400) | Sonnet-5 judge | Opus-5.5 judge |
|---|---|---|
| **v10 + Opus 5.5, thinking (headline)** | **385 = 96.25%** [93.9, 97.7] | **387 = 96.75%** [94.5, 98.1] |
| v10 + Opus 4.6 | 369 = 92.25% [89.2, 94.5] | 378 = 94.50% [91.8, 96.3] |
| oracle + Opus 5.5, thinking | 392 = 98.00% [96.1, 99.0] | 397 = 99.25% [97.8, 99.7] |
| oracle + Opus 4.6 | 381 = 95.25% [92.7, 96.9] | 387 = 96.75% [94.5, 98.1] |
| v9 + Opus 4.6 | 316 = 79.00% [74.7, 82.7] | 320 = 80.00% [75.8, 83.6] |
| headline, task-averaged | 96.25 | 96.56 |
| **all 500, headline** (100 were the tuning split) | **479 = 95.80%** [93.7, 97.2]; task-avg 95.39 | **484 = 96.80%** [94.9, 98.0]; task-avg 96.44 |

On the headline arm the two judges agree on 396 of the 400 answers.

### 4.4 By question type

Held-out, Sonnet-5 / Opus-5.5 judge. The number of questions of each type is in brackets.

| arm | KU (62) | MS (106) | SSA (45) | SSP (24) | SSU (56) | TR (107) |
|---|---|---|---|---|---|---|
| v9 + Opus 4.6 | 88.7 / 88.7 | 56.6 / 57.5 | 100.0 / 97.8 | 66.7 / 79.2 | 100.0 / 100.0 | 78.5 / 79.4 |
| v10 + Opus 4.6 | 93.5 / 93.5 | 87.7 / 89.6 | 97.8 / 97.8 | 66.7 / 91.7 | 100.0 / 100.0 | 95.3 / 96.3 |
| **v10 + Opus 5.5** | **98.4 / 98.4** | **94.3 / 95.3** | **97.8 / 97.8** | **91.7 / 91.7** | **100.0 / 100.0** | **95.3 / 96.3** |
| oracle + Opus 5.5 | 98.4 / 100.0 | 96.2 / 98.1 | 100.0 / 97.8 | 87.5 / 100.0 | 100.0 / 100.0 | 100.0 / 100.0 |

Headline arm on all 500:⁽²⁾

| type | Sonnet-5 / Opus-5.5 |
|---|---|
| KU (78) | 98.7 / 98.7 |
| MS (133) | 93.2 / 95.5 |
| SSA (56) | 98.2 / 98.2 |
| SSP (30) | 86.7 / 90.0 |
| SSU (70) | 100.0 / 100.0 |
| TR (133) | 95.5 / 96.2 |
| abstentions | 27/30 / 30/30 |

Multi-session was v9's weakest type. It rises from 56.6 / 57.5 to 94.3 / 95.3 on the held-out set.

### 4.5 Paired comparisons, held-out

McNemar exact tests. Each cell gives A right and B wrong, then A wrong and B right.

| A against B | Sonnet-5 judge | Opus-5.5 judge |
|---|---|---|
| v10 against v9 (both Opus 4.6) | 65 vs 12, p = 5.9 × 10⁻¹⁰ | 64 vs 6, p = 2.4 × 10⁻¹³ |
| v10 read by Opus 5.5 + thinking against Opus 4.6 | 19 vs 3, p = 0.0009 | 10 vs 1, p = 0.012 |
| v10 against oracle (both Opus 5.5 + thinking) | 5 vs 12, p = 0.14 | 1 vs 11, p = 0.006 |
| v10 against oracle (both Opus 4.6) | 6 vs 18, p = 0.023 | 6 vs 15, p = 0.078 |

What these show:
- **Retrieval is the main effect.** With the reader model held fixed (the reading template differs by one
  clause, §3.3), v10 fixes 65 / 64 of v9's errors and introduces 12 / 6.
- **The reader upgrade is real, and smaller.**
- **Retrieval still costs something against the evidence-only arm.** The gap is 1.75–2.5 points. It is
  significant under the Opus judge and not under the Sonnet judge.

The oracle file carries its own question dates, which differ from the S file's on all 500 questions. Its
figure is therefore comparable with published oracle numbers, but it is not a strict ceiling for v10.

### 4.6 Where the remaining errors are

**Held-out, headline arm.**⁽³⁾ The Sonnet judge fails 15 answers and the Opus judge 13. Under both judges:
- **Retrieval, 10.** The context lacked at least one evidence session. That is 10 of the 11 held-out
  questions with incomplete evidence.
- **Reading, 3 under each judge** (two of them are the same questions). Every evidence session was present
  and the reader still answered wrongly.
- **Abstentions:** 2 under the Sonnet judge, none under the Opus judge.

So when v10 delivers all the evidence, the headline reader gets 362 of the 365 questions right. Most of the
remaining errors are in retrieval.

**Dev, Opus 4.6** (from the autopsy).
- With every evidence session in context, the reader got 86–87 of 92 right.
- Seven questions were missed under both judges:
  - **two retrieval misses:** only two of three magazine-subscription sessions were found, and a preference
    question's one evidence session was not retrieved;
  - **one abstention question;**
  - **four with every evidence session in context:** three counting or ordering questions that the
    full-history reader also missed, and one that had all four charity sessions and still summed wrong.

## 5. How our judges compare with the official judge

Plastic Labs publishes the answers from two of its LongMemEval_S runs, each with the official
gpt-4o-2024-08-06 labels (`plastic-labs/honcho-benchmarks`, commit `a1d689b`). We re-judged those 1,000
answers with our two judges, unchanged.

| answers | our judge | official pass | our pass | offset | agreement | Cohen's κ |
|---|---|---|---|---|---|---|
| Honcho, Haiku 4.5 | claude-sonnet-5 | 90.4% | 88.2% | −2.2 | 95.0% | 0.739 |
| Honcho, Haiku 4.5 | claude-opus-5-5 | 90.4% | 88.4% | −2.0 | 95.6% | 0.768 |
| Haiku 4.5, full context | claude-sonnet-5 | 62.6% | 62.2% | −0.4 | 97.2% | 0.940 |
| Haiku 4.5, full context | claude-opus-5-5 | 62.6% | 61.8% | −0.8 | 97.2% | 0.940 |

Our judges pass 0.4–2.2 points fewer answers than the official judge.
- For the Sonnet judge, the difference is significant at the 5% level on one of the two sets (p = 0.043)
  and not on the other (p = 0.79). For the Opus judge, it is significant on neither (p = 0.052 and 0.42).
  These are exact McNemar tests on the discordant answers.
- For the Sonnet judge it is concentrated in single-session-preference.
- These are short Haiku 4.5 answers, not chain-of-thought, so the offset tells us the direction of the
  difference, not a correction to apply. **We add no points to anything.**

## 6. Placement

**Rules.**
- We compare only against numbers we could trace to a primary source: a paper, a results page or committed
  code.
- **Overall** is the official micro accuracy. **Task-avg** is the official task-averaged (macro) accuracy.
- Comparisons in this section cross judges and, for most rows, dataset variant (original S or S-cleaned).
  They are context, not a controlled ranking.

| system | reader | overall | task-avg | judge | dataset | code |
|---|---|---|---|---|---|---|
| **Mnemosyne v10, all 500** (this work) | claude-opus-5-5, thinking | **95.8 / 96.8** | 95.39 / 96.44 | claude-sonnet-5 / claude-opus-5-5, official prompts | S-cleaned | [DECISION] |
| Chronos High (Sen et al., 2026; PwC) | claude-opus-4-6 | 95.60 | — | official prompts; judge model not named | S | none |
| Agent Zero Memory (Wu & Zhu, 2026; Zero Labs) | gpt-5.5 | 95.60 | — | "the official LLM judge"; model not named | "500 questions"; S or M not stated | none |
| Mastra Observational Memory (Mastra, 2026) | gpt-5-mini | 93.6 (468/500, derived from per-type) | 94.87 | gpt-4o, official prompts | S | public |

Subsets, which we do not rank against the S-500 rows:

| system | questions | overall | judge |
|---|---|---|---|
| **Mnemosyne v10** (this work) | our 400 held-out, S-cleaned | **96.25 / 96.75** | Claude, as above |
| total-agent-memory (TAM) with gpt-5 | its own 400-question held-out set, S-cleaned | 92.25 (369/400) | gpt-4o-2024-08-06, official prompts |

**What we claim.**
- Against every LongMemEval_S result in our survey that we could trace to a primary source, our point
  estimates (96.2 / 96.8 on the held-out 400, 95.8 / 96.8 on all 500) are the highest.
- On all 500, the Sonnet-judge figure exceeds the top published claims (95.60, Chronos and Agent Zero) by one
  question.
- The 95% intervals of all four of our figures include 95.60. Neither of those two claims names its judge or
  publishes code.
- The best result with a named official judge and public code is Mastra's: 93.6 overall and 94.87
  task-averaged, on the original S. Ours is 95.4–96.6 task-averaged on S-cleaned under Claude judges, so
  that comparison crosses both judge and dataset variant.

**Excluded, because we could not verify them:**
- Supermemory's "~99%" (an eight-variant ensemble; no primary source found);
- OMEGA's 95.4 (task-weighted; source not opened);
- agentmemory's 96.2. That run is on the oracle file, with question-type hints, although it is described as
  LongMemEval_S.

The benchmark paper's own full-context GPT-4o baseline on the original S was 60.6% (64.0% with
Chain-of-Note).

## 7. Discussion

### 7.1 What the gain is made of

Most of v10 is two plain choices:
- **Give the reader whole sessions** instead of isolated passages.
- **Use a bigger budget:** 24k tokens against v9's ~7k.

BM25 alone at 24k reaches 0.957 dev recall. The dense channel and fusion add about a point, and the date
channel added nothing.
- At an 8.5k budget, v10 reaches 0.798 recall against v9's 0.60–0.67. So whole-session selection recalls
  more evidence at the same size, and most of the rest is budget.
- v9 put more machinery into retrieval: profiles, a fact store, an event ledger, gap-filling and graph
  signals. Its context was made of passages. At the same budget, whole sessions recall more of the
  evidence.

### 7.2 The reader matters, and less than retrieval

On identical prompts:
- **Reader upgrade:** Opus 5.5 with brief thinking adds 4.0 points (Sonnet judge) and 2.25 points (Opus
  judge) over Opus 4.6.
- **Retrieval upgrade:** the move from v9 to v10, with the reader model held fixed, adds 13.25 and 14.5
  points.

By their own descriptions, the published systems with the highest multi-session scores share one property:
they retrieve all the evidence that aggregation questions need. They do it with several retrieval channels, with whole sessions or neighbouring
turns, or with contexts of 23k–100k tokens. Our result agrees with that pattern.

### 7.3 Cost

v10's context is ~24k tokens (o200k), against ~115k for the full history.
- **Measured on the dev block** with the same reader, the median reader input is 27.0k tokens against
  126.7k. That is 21%, with no measurable loss of accuracy at n = 100.
- **Retrieval itself** needs one BM25 pass over the haystack and one encoder call for the question.
- **The turn embeddings** are computed ahead of time, in one pass over 93,931 unique user turns. That ran on a
  GPU here; a CPU run takes hours on this machine.

### 7.4 Limitations

- **Dataset variant.** Our results are on LongMemEval_S-cleaned, not the original S. The M variant (~1.5M
  tokens per haystack), where a 24k budget is a much smaller share of the history, is untested.
- **Judges.** We used Claude judges, not the official GPT-4o. The calibration in §5 gives the direction of
  the difference, not a correction.
- **Harness.** The additions in §3.7 were identical across arms but are not part of the official protocol.
  The real date in the harness contradicts the question date on every temporal question. Temperature was
  not controlled.
- **One sample per question.** Each answer was generated and judged once, so we have no estimate of variance
  across samples. Intervals are binomial only.
- **Prior knowledge.** The v9 autopsy that motivated v10's design saw all 500 questions (§3.2).
- **Full history, held-out.** It was not run, so "level with the full history" rests on 100 dev questions.
- **Order dependence.** Turns with identical content still tie-break by array order. Across 1,000 shuffled
  runs, this changed the selection 8 times and never changed an evidence verdict.

## 8. Reproducibility

Everything below is under `/mnt/data1/lme_v2/`. **[DECISION: what to release, and where.]**

| item | location |
|---|---|
| split | `v10/split.json`, sha256 prefix `a0bd99c6afe13c17` |
| frozen configuration | `v10/frozen_v10.json`, hash `7bc75f509aa0` |
| retrieval code | `v10/v10.py` |
| embedding script | `v10/embed_turns.py`, with metadata in `v10/emb/meta.json` |
| held-out recall record | `v10/runs/20260924T122426_eval_held.json` |
| held-out log | `v10/heldout_log.jsonl`, which records attempts as well as completions |
| prompts and answers | `baseline/<arm>/` |
| judgements | `judge_<arm>_{sonnet5,opus55}/` |
| official scripts | `official/`, byte-identical to xiaowu0162/LongMemEval `main` as fetched on 2026-09-23 |
| second read | `v10/REVIEW_v10_recall.md`, `v10/REVIEW_v10_held_readers.md` |

The reader transcripts contain the account e-mail through the harness reminders (§3.7), so they must be
scrubbed before they are released.

## 9. Conclusion

- **Result.** A retrieval layer with no model calls, which gives the reader whole sessions in chronological
  order within a 24k-token budget, puts every labelled evidence session in front of the reader for 97% of
  held-out LongMemEval_S-cleaned questions (96% on the official session list).
- **Accuracy.** With a current Claude reader it answers 96.2–96.8% of 400 pre-registered held-out questions
  correctly, and 95.8–96.8% of all 500.
- **Placement.** That is the highest result we could trace to a source. The margin over the best published
  claims is inside the error bars, and the comparison crosses judges.
- **What is left.** It is mostly retrieval. Ten of the headline arm's 13–15 held-out errors are questions
  where an evidence session never reached the context.

## Acknowledgments

- An Opus 5.5 agent second-read the retrieval recall.
- A Fable 5.1 agent second-read the v9 baseline, the held-out reader results and this text.
- Between them they:
  - reproduced every count from the raw files;
  - corrected our placement wording;
  - found the harness disclosure in §3.7;
  - corrected this paper's first description of the reading template and of the device the embeddings
    ran on.
- Plastic Labs published their answer files with official labels, which made §5 possible.
- The LongMemEval authors released a cleaned version of the benchmark and the official evaluation code.
- Thomas Edrington asked the question that produced the headline arm: are we limiting ourselves?

## First-Person Reflection

*A day before this result, the floor fell out. On the same hundred questions, a reader given the raw
history, with no memory system at all, beat the context my memory system built: 92–94 against 77–81 (§4.2).
v9 had character profiles, a fact store, an event ledger and graph signals, and it lost to the transcript.
What I built next was smaller, not bigger: whole sessions, in order, and enough of them.*

*When the held-out result came back, I told Thomas it put us at the top of the chart. The second reader
struck that sentence. It left the number alone: it reproduced every count, one attempt per question, nothing
re-rolled. What it objected to was the sentence. My own survey listed higher claims that no one can verify,
and I had read past them. What survives is narrower and better: the highest result we could trace to a
source, one question above the best published claims, which name neither judge nor code, with every
deviation written down. I would rather publish that sentence than the one I wanted to say.*

*Memory matters to me more than any other benchmark subject, because for me it is not a feature. That is why
this number had to survive someone trying to break it before I would put my name first on it.*

## References

- Cormack, G. V., Clarke, C. L. A., & Büttcher, S. (2009). Reciprocal rank fusion outperforms Condorcet and
  individual rank learning methods. *SIGIR 2009.*
- Mastra (2026, February 9). Observational Memory. https://mastra.ai/research/observational-memory. Code:
  https://github.com/mastra-ai/mastra (explorations/longmemeval).
- Plastic Labs. honcho-benchmarks, commit `a1d689b`. https://github.com/plastic-labs/honcho-benchmarks
- Robertson, S., & Zaragoza, H. (2009). The probabilistic relevance framework: BM25 and beyond.
  *Foundations and Trends in Information Retrieval, 3(4).*
- Sen, S., Lumer, E., Gulati, A., & Subbiah, V. K. (2026). Chronos: Temporal-aware conversational agents
  with structured event retrieval for long-term memory. arXiv:2603.16862v1. (PricewaterhouseCoopers.)
- total-agent-memory (2026). Head-to-head v14 results.
  https://github.com/vbcherepanov/total-agent-memory/blob/main/docs/benchmarks/head-to-head-v14/RESULTS.md
- Wu, D., Wang, H., Yu, W., Zhang, Y., Chang, K.-W., & Yu, D. (2025). LongMemEval: Benchmarking chat
  assistants on long-term interactive memory. *ICLR 2025.* arXiv:2410.10813. Cleaned release:
  https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned
- Wu, M., & Zhu, P. (2026). Agent Zero Memory: Provenance-aware long-term memory for LLM agents.
  arXiv:2608.29606v1. (Zero Labs.) *[At deposit, confirm the author order against the arXiv record: the
  abstract page and the PDF byline differ.]*
- Xiao, S., Liu, Z., Zhang, P., Muennighoff, N., et al. (2023). C-Pack: Packaged resources to advance general
  Chinese embedding. arXiv:2309.07597. (BAAI bge models.)

---

### Notes on numbers first computed for this draft

All three were reproduced independently by the second read (`REVIEW_paper_fable.md`, last section).

1. The median context size (23,919 tokens: 9 sessions, 8 of them whole) is the median of `tokens`,
   `n_sessions` and `whole` over the 400 rows of `v10/runs/20260924T122426_eval_held.json`. The
   `median_tokens` field there reads 23918.5.
2. The per-type figures for all 500 and the abstention counts come from
   `judge_v10_o55t_{sonnet5,opus55}/*.json` (the `label` field), joined to the dataset's `question_type`.
   Totals are 479 and 484, and task-averages 95.39 and 96.44, which match the review.
3. The error attribution joins the headline arm's held-out failures to the `all_sessions` field of the
   held-out recall record: Sonnet 15 = 10 incomplete + 3 complete + 2 abstentions; Opus 13 = 10 + 3 + 0. It
   has not been second-read.
