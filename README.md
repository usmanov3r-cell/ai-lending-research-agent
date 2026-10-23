# AI Lending Product Intelligence Agent



**Python + OpenAI | Consumer Lending | Product Research | Financial Validation**



A working prototype that transforms structured consumer-lending competitor research into financial validation results and AI-assisted business insights.



**Current scope:** Poland | Unsecured instalment loans | Provident and Wonga



**Status:** Functional prototype — October 2026



## 1. Business Problem



Consumer lenders need reliable competitor intelligence to support pricing, product development and market strategy.



However, researching lending products involves more than comparing advertised interest rates.



Relevant factors include:



* APR (RRSO), nominal interest rates and fees.

* Loan amounts, repayment terms and eligibility.

* Commission-payment and financing arrangements.

* Promotions and repayment flexibility.

* Customer affordability and total repayment obligations.

* Regulatory considerations and evidence quality.



Comparing incomplete or inconsistent product information can lead to misleading commercial conclusions.



**This project demonstrates how a combination of deterministic Python rules and LLM analysis can support more reliable lending product research.**



## 2. What the Application Does



The current prototype:



1\. Loads manually researched consumer-lending product information.

2\. Normalizes different lender records into a common data structure.

3\. Validates disclosed financial figures using Python.

4\. Identifies missing information and unresolved evidence.

5\. Checks whether representative loan scenarios can be directly compared.

6\. Analyzes customer fee-payment alternatives.

7\. Produces a structured JSON research report.

8\. Optionally uses an OpenAI model to generate a commercial analysis.

9\. Runs automated financial regression tests.



The application separates **financial calculations from AI-generated interpretation**.



## 3. Architecture



```text

Published lender information

&#x20;         |

&#x20;         v

Manual research and structured JSON

&#x20;         |

&#x20;         v

Data normalization (Python)

&#x20;         |

&#x20;         v

Financial validation (Python)

&#x20;         |

&#x20;         v

Evidence and comparability checks

&#x20;         |

&#x20;         v

Structured research report (JSON)

&#x20;         |

&#x20;         v

OpenAI analysis (optional)

&#x20;         |

&#x20;         v

Product intelligence brief (Markdown)

```



### Python responsibilities



Python handles financial reconciliation, fee-payment calculations, comparison eligibility, data-quality checks and test execution.



### LLM responsibilities



The LLM interprets the supplied research data and produces:



* Product positioning observations.

* Customer-choice and affordability considerations.

* Commercial opportunities and hypotheses.

* Regulatory questions requiring further review.

* Recommended research and validation activities.



The LLM is instructed not to invent missing information, override financial validation results or make unsupported legal conclusions.



## 4. Real Lending Research Example



The current dataset includes two Polish non-bank lending brands: **Provident** and **Wonga**.



### Published representative examples



| Attribute        |    Provident |          Wonga |

| ---------------- | -----------: | -------------: |

| Loan amount      |    PLN 9,300 |      PLN 6,000 |

| Term             |    24 months |      42 months |

| Nominal interest |     7% fixed | 14.5% variable |

| Published APR    |          29% |         73.69% |

| Commission       | PLN 1,887.88 |      PLN 2,700 |



These are recorded lender-published representative examples, not personalized quotations or independently verified current offers.



**The application does not rank these products as directly comparable offers**, because their representative loan amounts and terms differ.



### Wonga: Commission-payment alternatives



The research dataset records two disclosed commission-payment arrangements.



| Attribute                  | Upfront commission | Separately financed commission |

| -------------------------- | -----------------: | -----------------------------: |

| Upfront commission payment |          PLN 2,700 |                          PLN 0 |

| Primary loan repayments    |       PLN 7,707.83 |                   PLN 7,707.83 |

| Additional loan repayments |                  — |                   PLN 3,468.50 |

| Total customer outflow     |      PLN 10,407.83 |                  PLN 11,176.33 |

| Incremental financing cost |              PLN 0 |                     PLN 768.50 |



The figures illustrate a potential customer trade-off between upfront liquidity and total repayment obligations.



The application validates the recorded arithmetic and identifies that the commission is settled separately from the primary loan's published instalments.



**Financial reconciliation does not establish regulatory compliance.** The legal treatment of commission financing requires separate assessment.



## 5. Getting Started



### Requirements



* Python 3

* Git

* OpenAI API key (only for AI-generated analysis)



The commands below are intended for Windows Git Bash.



### Installation



Clone the repository and open the project folder.



Create a virtual environment:



```bash

python -m venv .venv

```



Activate it:



```bash

source .venv/Scripts/activate

```



Install dependencies:



```bash

python -m pip install -r requirements.txt

```



### Run the research pipeline



```bash

python run\_pipeline.py --data real

```



This command:



* Normalizes Provident and Wonga data.

* Runs automated financial tests.

* Validates lending product information.

* Produces the structured research report.

* Checks the AI input without calling the OpenAI API.



**No API key or paid API call is required for this mode.**



### Generate the AI analysis



Create a local `.env` file based on `.env.example` and provide your OpenAI API key:



```text

OPENAI\_API\_KEY=your\_key\_here

```



Then execute:



```bash

python run\_pipeline.py --data real --with-ai

```



**This command makes a paid OpenAI API request.**



The `.env` file is excluded from Git.



### Run with synthetic data



```bash

python run\_pipeline.py --data synthetic

```



Synthetic mode uses fictional lending products for development and testing.



### Run automated tests independently



```bash

python -m unittest discover -s tests -v

```



## 6. Outputs



| File                                    | Description                                           |

| --------------------------------------- | ----------------------------------------------------- |

| `data/output/real\_research\_report.json` | Structured competitor research and validation results |

| `data/output/real\_ai\_brief.md`          | AI-generated lending product intelligence brief       |

| `data/output/research\_report.json`      | Synthetic research report                             |

| `data/output/ai\_brief.md`               | Synthetic AI analysis example                         |



Example outputs are included in the repository.



## 7. Important Limitations



This is a research prototype, not a production lending or regulatory-compliance system.



Current limitations include:



* Competitor information is collected manually.

* There is no automated website extraction or monitoring.

* Source records remain marked as not independently verified.

* Published APRs are reported, not recalculated.

* Financial validation checks arithmetic consistency, not contractual accuracy.

* The comparison implementation is limited and does not perform a full scenario-grid analysis.

* Legal issues are flagged for review; regulatory compliance is not determined automatically.

* Automated tests cover selected financial scenarios rather than comprehensive production requirements.



The application should not be used to make customer lending decisions or definitive compliance assessments.



## 8. Development Roadmap



Potential next developments:



* Automated collection of approved lender disclosures.

* Source snapshots and change detection.

* Broader competitor and product coverage.

* Comparable loan-amount and maturity scenarios.

* Enhanced fee-financing and APR calculations.

* Market-specific regulatory rule validation.

* Automated monitoring and periodic research reports.

* Improved testing with independent fixtures.

* Human approval workflows for research findings.



The original broader architecture concept is preserved in \[`docs/architecture\_draft.md`](docs/architecture\_draft.md).



## 9. Project Objective



This project explores how domain-specific financial rules, structured evidence and AI analysis can support better decision-making in consumer lending.



The core design principle is:



**Python validates the numbers. AI interprets the findings. Humans remain responsible for decisions.**



