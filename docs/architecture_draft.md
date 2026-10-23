# Lending Market Research & Decision-Support Application

A lending-specific application that structures, validates and compares consumer-credit
products across lenders, and turns calculated evidence into business analysis.

It is **not** a generic AI research assistant. Numbers come from sources or from
deterministic Python calculations; the LLM interprets evidence, it does not produce it.

> **Status:** early development. First market: **Poland**. First product:
> **unsecured personal loans**. First scope: **3 competitors**.
> Build priority: **structured data → Python calculations → JSON comparison → LLM
> analysis → working demo.**
> The **MVP** sections describe what is being built now.
> Sections marked *(target)* describe planned architecture, not shipped functionality.

---

## Why this exists

Researching a consumer-lending market means comparing competitor products, pricing,
fees, promotions, repayment mechanics and regulatory constraints. Done by hand, it is
slow, goes stale, and rarely records *where* each number came from or *how sure* we are.

Generic AI tools make this worse: they produce confident tables with no way to tell a
verified fee from a guess, or a recalculated APR from a copied one.

This project takes the opposite approach:

- **Every field has a source and a verification status.**
- **Every calculation is deterministic Python, with explicit assumptions.**
- **The LLM interprets calculated evidence; it never invents figures.**
- **Missing or unverifiable information is reported, with the reason.**

---

## What it does: Python vs LLM

| Responsibility | Python (deterministic) | LLM |
|---|---|---|
| Fees, instalments, total cost | ✅ | — |
| APR recalculation | ✅ | — |
| Regulatory limit checks | ✅ | — |
| Comparison across a scenario grid | ✅ | — |
| Business interpretation | — | ✅ |
| Proposition / opportunity ideas | — | ✅ (labelled as interpretation) |
| Extraction from documents *(target)* | Schema and evidence validation *(target)* | ✅ |

---

## First analytical feature (MVP)

Two competitors, same loan request:

| Variable | Competitor A | Competitor B |
|---|---|---|
| Loan amount | PLN 10,000 | PLN 10,000 |
| Nominal interest | 11% | 10% |
| Origination fee | PLN 0 | PLN 500 |
| Term | 24 months | 24 months |

*Illustrative figures, not real offers.*

**Python** calculates comparable costs with explicit assumptions (annuity repayment,
monthly compounding, fee paid upfront **or** financed into the principal).

Total cost of credit, PLN (interest + fee):

| Amount / term | A | B, fee upfront | B, fee financed | Cheaper |
|---|---|---|---|---|
| 10,000 / 24 m | 1,186 | 1,575 | 1,629 | **A** |
| 20,000 / 48 m | 4,812 | 4,848 | 4,957 | **A** (marginal) |
| 40,000 / 48 m | 9,623 | 9,196 | 9,305 | **B** |
| 60,000 / 60 m | 18,273 | 16,989 | 17,127 | **B** |

**LLM** interprets the calculated evidence, for example:

> Competitor B advertises a lower nominal rate but charges a fixed origination fee.
> For small, short loans B is more expensive; above roughly PLN 20–40k and longer
> terms, B becomes cheaper. A fixed fee penalises small loans, so a transparent
> "no-fee" proposition is most competitive in the small-ticket segment.

This is a business interpretation based on calculated evidence, not an invented fact.
It also shows why a single example is not enough: **the cheaper offer depends on amount
and term**, which is why every comparison runs on a scenario grid.

---

## Inputs (MVP)

| Input | Example |
|---|---|
| Market | `PL` |
| Product type (canonical) | `unsecured_instalment_loan` |
| Product data | `data/input/pl_personal_loans.json` (manually researched) |
| Scenario grid | `markets/pl/scenario_grid.yaml` |
| Research date | `2026-10-22` (determines which rules apply) |

---

## Pipeline

### MVP

```
 Manually researched products (JSON, with sources)
          │
          ▼
 1. Load & validate against schema
          │
          ▼
 2. Calculate  (Python)
    instalments, total cost, APR status, scenario grid
          │
          ▼
 3. Rule checks  (Python, market- and date-specific)
          │
          ▼
 4. Comparison output  (JSON + table)
          │
          ▼
 5. Business analysis  (LLM, evidence in → interpretation out)
```

### Target

```
 Source registry (curated)            Agent helpers (target)
 markets/<country>/lenders.yaml  <──  - link health checks
          │                           - change detection
          ▼                           - discovery suggestions (human-approved)
 Collect & snapshot  →  Extract (LLM)  →  Classify  →  Validate & calculate
          →  Reconcile pricing layers  →  Coverage report  →  Analysis
```

**Design choice: registry vs evidence.**

- The **source registry** defines *which* sources are approved for research
  (lender, document role, URL, tier). It is a list of where to look, not a source of facts.
- The **lender's original documents** (fee table, T&Cs, promo terms, SECCI) provide the
  *evidence*. A field can only be `verified` against a document, never against the registry.
- Agentic helpers *(target)* may propose changes to the registry, subject to human
  approval. They never create evidence.

---

## Data model

```
Lender
 └── Product            (canonical type + original lender name)
      └── Variant       (eligibility, channel, customer type)
           ├── Advertised pricing   (representative example, banners)
           ├── Contractual pricing  (fee table, T&Cs, promo terms)
           ├── Quoted pricing       (calculator results)       (target)
           └── Promotions           (conditional objects)
```

### Field-level provenance

```json
{
  "value": 500,
  "unit": "PLN",
  "status": "verified",
  "source_role": "fee_table",
  "source_tier": 1,
  "evidence": {
    "url": "https://...",
    "retrieved_at": "2026-10-22",
    "text_span": "…"
  }
}
```

In the MVP, evidence is a URL, date and quoted text. Archived snapshots with hashes are
*(target)*.

### Verification status

| Status | Meaning |
|---|---|
| `verified` | From a tier-1 source, with evidence |
| `extracted_unverified` | Recorded, not confirmed by a tier-1 source |
| `derived` | Calculated by Python from other fields |
| `conflicting` | Sources disagree; all values kept |
| `manually_collected` | Entered by a human (screenshot, PDF), with a note |
| `not_published` | Lender does not disclose it publicly |
| `not_accessible` | Could not be retrieved; see reason code |

`not_accessible` reason codes: `bot_protection` · `login_required` ·
`personalised_pricing_only` · `calculator_requires_personal_data` ·
`js_only_no_static_data` · `pdf_unreadable` · `robots_or_tos_disallow` ·
`http_error` · `timeout` · `geo_blocked`

### APR status

APR is treated separately because "verified" must mean recalculated, not copied.

| APR status | Meaning |
|---|---|
| `apr_verified` | Recalculated from complete cash flows and matches the published APR within tolerance |
| `apr_mismatch` | Recalculated from complete cash flows and does **not** match the published APR |
| `apr_reported` | Published by the lender, not independently recalculated (insufficient cash-flow data) |
| `apr_unavailable` | Not published and cannot be calculated |

The LLM receives the APR status with every figure and must not describe an
`apr_reported` value as verified.

### Source tiers

| Tier | Source | Can produce `verified`? |
|---|---|---|
| 1 | Fee table, T&Cs, promo terms, loan agreement template, SECCI | Yes |
| 2 | Lender product / marketing pages, calculators | No, unless confirmed by tier 1 |
| 3 | Comparison sites, news | No, leads only |

---

## Regulatory rules (market- and date-specific)

Rules live in `markets/<country>/rules/` and each carries a legal basis and an
effective-date range. The research date determines which rules apply.

**Poland: separate rules, separate mechanics**

| Rule | Legal basis | Depends on |
|---|---|---|
| Maximum contractual interest | Civil Code | NBP reference rate (loaded at runtime) |
| Maximum non-interest costs | Consumer Credit Act, Art. 36a | Principal and duration (statutory formula) |
| APR / representative example | Consumer Credit Act | Cash flows and disclosure completeness |

**Current law vs future requirements.** CCD II (Directive (EU) 2023/2225) requires
Member States to apply their implementing measures from 20 November 2026. At the time of
writing (October 2026), Poland's implementing legislation was still being finalised.
The directive itself does not change the rules a Polish lender must follow; the
national implementing act does. The application therefore distinguishes:

- **Applicable rules**: in force on the research date (checks produce pass / fail)
- **Upcoming requirements**: adopted or expected but not yet applicable
  (produce *readiness observations*, never pass / fail)

Rule outputs are compliance indicators for research purposes, not legal opinions.

**MVP scope:** the rule engine structure plus the simplest checks. Detailed regulatory
validation is *(target)*.

---

## Product classification

Products are classified by **attributes**, not names. In Poland, *kredyt gotówkowy*
(banks only) and *pożyczka gotówkowa* (any lender) can be the same product for a consumer.

Canonical types (initial): `unsecured_instalment_loan` · `single_repayment_short_term` ·
`consolidation_loan` · `revolving_credit_line` · `pos_instalment`

A per-market `glossary.yaml` maps local terms to canonical types as hints; rules decide.

---

## Promotions & special conditions captured

**Price promotions:** 0% first loan · interest-free period (and post-promo rate) ·
0% commission / origination fee · no admin or account fee · online-only rate ·
cashback / refunded instalment · deferred first payment · tiered pricing by amount/term

**Conditional pricing:** salary account or card required · insurance (mandatory /
optional / required for promo price) · cross-sell bundles

**Retention & repeat customers:** loyalty pricing · refinancing / consolidation ·
top-ups · referral bonuses

**Servicing costs:** early repayment fee and cost refund · extension / rollover fees ·
late payment interest, reminder and collection fees · payment holidays / restructuring

Every promotion records eligibility, validity dates, amount/term caps, what applies
after it ends, and whether the representative example reflects it.

---

## Pricing layers & reconciliation *(target)*

| Layer | Answers |
|---|---|
| **Advertised** | What does the lender want customers to see? |
| **Contractual** | What is the lender legally bound to? |
| **Quoted** | What does a customer see for a given amount and term? |

Flags such as: calculator APR ≠ APR recalculated from the fee table; fee-table
commission ≠ calculator commission; representative example at the cheapest grid point.

---

## Coverage report *(target)*

Lenders in scope vs covered · field fill rate · fields per status · failures with reason
codes · source documents changed since the last run.

---

## Repository structure

```
markets/
  pl/
    scenario_grid.yaml
    glossary.yaml
    rules/              # one module per rule, with legal basis + effective dates
    lenders.yaml        # source registry
schema/
  product.schema.json
data/
  input/                # manually researched products (MVP)
  output/
src/
  calc/                 # instalments, total cost, APR
  rules/                # rule engine
  compare/              # scenario-grid comparison
  analysis/             # LLM prompt + evidence packaging
  collect/              # (target) fetch, snapshot
  extract/              # (target) LLM extraction
tests/
  gold/                 # hand-verified reference cases
```

---

## Evaluation

- Calculations are tested against hand-calculated reference cases.
- APR recalculation is tested against published representative examples.
- LLM output is checked for unsupported figures: every number in the analysis must
  appear in the evidence package it received.

---

## Non-goals & principles

- No personal data entered anywhere, including calculators
- No bypassing of CAPTCHAs, bot protection, logins or access restrictions
- Respect robots.txt and website terms of use
- Not financial or legal advice; outputs are market research
- Facts, derived values and interpretation are always labelled separately
- Gaps are reported as gaps

---

## Roadmap

| Milestone | Deliverable | Status |
|---|---|---|
| **M1** | Lending schema, source registry, 3 manually researched products | ☐ |
| **M2** | Working Python CLI, JSON input/output, deterministic comparisons | ☐ |
| **M3** | LLM API integration, evidence-based business analysis | ☐ |
| **M4** | Automated source retrieval, validation, improvements *(target)* | ☐ |

### Build priority

```
Structured lending data → Python calculations → JSON comparison → LLM analysis → working demo
```

Everything on this line comes first. Automated collection, detailed regulatory
validation, pricing-layer reconciliation and agentic functionality follow **only after**
M3 is demonstrable. Architecture sections in this README describe direction, not the
order of work.

---

## Technology

Python · JSON / JSON Schema · YAML · Git & GitHub · LLM API ·
Playwright *(target, calculators)*

## How this is built

A hands-on learning project, built with AI-assisted coding. The domain logic, data model,
validation rules and lending analysis are designed by the author, drawing on experience
in consumer-lending product, analytics and regulatory implementation (CCD II / DMD II).
