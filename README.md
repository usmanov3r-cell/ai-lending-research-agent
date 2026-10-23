# AI Lending Product Intelligence Agent

**Consumer lending research · Python + OpenAI**  
**Prototype | Poland | Provident and Wonga | October 2026**

A working prototype that turns structured competitor disclosures into **financial checks** and an optional **AI-generated product strategy brief**.

## What it does

- **Normalizes** manually researched lender products into one data model.
- **Checks the numbers:** fees, total repayable, instalments and alternative fee-payment arrangements.
- **Flags uncertainty:** missing evidence, unverified APRs and offers that cannot be compared fairly.
- **Generates insights:** an optional LLM brief on customer choices, product economics and questions for further research.

**Design principle:** Python checks calculations; AI interprets results. Neither replaces source verification or human judgment.

## Example: Wonga commission choices

The recorded representative example describes a **PLN 2,700 commission** that can be paid upfront or financed with a separate loan.

| Customer impact | Pay upfront | Separate commission loan |
|---|---:|---:|
| Commission paid upfront | PLN 2,700 | PLN 0 |
| Total customer cash outflow | PLN 10,407.83 | PLN 11,176.33 |
| Extra cost of financing commission | PLN 0 | **PLN 768.50** |

**Insight:** Financing removes the upfront cash requirement but increases repayment obligations. The application reconciles these figures; it **does not determine legal compliance**.

The Provident and Wonga representative examples use different amounts and terms, so the application **does not rank them as like-for-like offers**.

## Run the prototype

From the project folder, using **Windows Git Bash**:

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
python run_pipeline.py --data real
```

This runs normalization, three regression tests, financial checks and a **free AI-input dry run**. The structured result is saved to `data/output/real_research_report.json`.

For an AI-generated brief, add your API key to a local `.env` file (see `.env.example`) and run:

```bash
python run_pipeline.py --data real --with-ai
```

**The `--with-ai` option makes a paid API call.** The brief is saved to `data/output/real_ai_brief.md`.

## Scope and limitations

This is a **demonstration, not a production system**. Source data was collected manually; representative figures have not been independently verified; APR is not recalculated; the tests cover selected financial cases only. Automated source collection, wider market coverage and legal rule checks are **future work**.

See [the architecture draft](docs/architecture_draft.md) for the broader design and roadmap.
