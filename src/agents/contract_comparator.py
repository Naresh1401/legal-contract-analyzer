"""LangChain agent for comparing two legal contracts."""

import os
from typing import Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")


class ClauseDifference(BaseModel):
    """A difference between two contracts for a specific clause."""
    clause_type: str = Field(description="Type of clause being compared")
    contract_a_text: str = Field(default="", description="Relevant text from Contract A")
    contract_b_text: str = Field(default="", description="Relevant text from Contract B")
    difference_type: str = Field(description="Type: Added, Removed, Modified, Identical, Missing in A, Missing in B")
    impact: str = Field(description="Impact assessment: Advantageous, Disadvantageous, Neutral")
    impact_for: str = Field(default="", description="Which party the impact favors (Party A or Party B)")
    description: str = Field(description="Description of the difference and its implications")
    significance: str = Field(default="Medium", description="Significance: High, Medium, Low")


class ContractComparison(BaseModel):
    """Complete comparison output."""
    contract_a_type: str = Field(default="", description="Type of Contract A")
    contract_b_type: str = Field(default="", description="Type of Contract B")
    contract_a_parties: dict = Field(default_factory=dict, description="Parties in Contract A")
    contract_b_parties: dict = Field(default_factory=dict, description="Parties in Contract B")
    total_differences: int = Field(description="Total number of material differences found")
    advantageous_changes: int = Field(default=0, description="Changes favorable to the reviewing party")
    disadvantageous_changes: int = Field(default=0, description="Changes unfavorable to the reviewing party")
    neutral_changes: int = Field(default=0, description="Neutral changes")
    differences: list[ClauseDifference] = Field(default_factory=list, description="List of clause-level differences")
    redline_summary: str = Field(description="Executive summary of changes in redline format")
    recommendation: str = Field(description="Overall recommendation based on the comparison")


COMPARISON_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert legal contract analyst specializing in contract comparison
and redline reviews. Compare the two contracts provided and identify all material differences.

For each key clause area, compare the provisions in both contracts:

1. PARTIES AND TERM - Compare parties, effective dates, duration, renewal terms
2. SCOPE AND OBLIGATIONS - Compare scope of work/services, deliverables
3. PAYMENT AND FEES - Compare pricing, payment terms, penalties
4. INTELLECTUAL PROPERTY - Compare IP ownership, licensing, assignment
5. CONFIDENTIALITY - Compare definitions, duration, exceptions
6. DATA PROTECTION - Compare security measures, breach notification, compliance
7. INDEMNIFICATION - Compare scope, mutual vs. one-sided, carve-outs
8. LIABILITY - Compare caps, exclusions, carve-outs
9. TERMINATION - Compare rights, notice periods, cure periods, effects
10. SLA/PERFORMANCE - Compare uptime, credits, response times
11. NON-COMPETE / NON-SOLICITATION - Compare scope, duration
12. DISPUTE RESOLUTION - Compare mechanism, jurisdiction, governing law
13. INSURANCE - Compare requirements, coverage amounts
14. GENERAL PROVISIONS - Compare assignment, amendment, force majeure

For each difference, assess:
- Whether the change is Advantageous, Disadvantageous, or Neutral
- Which party benefits from the difference
- The significance level (High, Medium, Low)

Generate a redline summary highlighting the most important changes.

{format_instructions}"""),
    ("human", """Compare the following two contracts:

=== CONTRACT A ===
{contract_a}

=== CONTRACT B ===
{contract_b}"""),
])


class ContractComparator:
    """Compares two contracts side-by-side using LLM analysis."""

    def __init__(self, model_name: Optional[str] = None):
        self.llm = ChatOpenAI(
            model=model_name or OPENAI_MODEL,
            temperature=0,
        )
        self.parser = PydanticOutputParser(pydantic_object=ContractComparison)

    def compare(self, contract_a: str, contract_b: str) -> ContractComparison:
        """Compare two contracts and identify differences."""
        chain = COMPARISON_PROMPT | self.llm | self.parser
        result = chain.invoke({
            "contract_a": contract_a,
            "contract_b": contract_b,
            "format_instructions": self.parser.get_format_instructions(),
        })
        return result

    def compare_as_dict(self, contract_a: str, contract_b: str) -> dict:
        """Compare and return as dictionary."""
        return self.compare(contract_a, contract_b).model_dump()

    def compare_as_json(self, contract_a: str, contract_b: str) -> str:
        """Compare and return as JSON string."""
        return self.compare(contract_a, contract_b).model_dump_json(indent=2)
