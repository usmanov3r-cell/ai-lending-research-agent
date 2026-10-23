import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# 1. Load API configuration
load_dotenv()

# 2. Read the research report produced by main.py
report_file = Path("data/output/research_report.json")

with open(report_file, "r", encoding="utf-8") as file:
    research = json.load(file)


# 3. Connect to OpenAI
client = OpenAI()

# 4. Request lending-specific business analysis
response = client.responses.create(
    model="gpt-6-luna",
    reasoning={"effort": "low"},
    max_output_tokens=1000,
    store=False,
    instructions="""
    You are a consumer-lending strategy analyst.

    Analyze ONLY the supplied research data.

    Your tasks:
    1. Identify meaningful competitor pricing differences.
    2. Explain the potential business implications.
    3. Identify one possible product opportunity.
    4. Explain which missing information prevents firm conclusions.
    5. Recommend the next research step.

    Rules:
    - Do not invent figures or sources.
    - Treat synthetic data as illustrative, not real market evidence.
    - Do not declare a cheaper product without sufficient evidence.
    - Separate observed facts from commercial hypotheses.
    - Account for promotional eligibility and unknown conditions.
    - Keep the analysis concise and lending-specific.
    """,
    input=json.dumps(research, ensure_ascii=False)
)


# 5. Save AI analysis
output_file = Path("data/output/ai_brief.md")
output_file.write_text(response.output_text, encoding="utf-8")

print("\n=== AI LENDING ANALYSIS ===")
print(response.output_text)

print(f"\nAI brief saved: {output_file}")

# 6. Show API usage
print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")