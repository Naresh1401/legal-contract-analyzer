"""LangChain agent for generating executive summaries of legal contracts."""

import os
from typing import Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")


class PartyObligation(BaseModel):
    """Obligations for a specific party."""
    party_name: str = Field(description="Name of the party")
    role: str = Field(default="", description="Role in the contract (e.g., Provider, Customer)")
    key_obligations: list[str] = Field(default_factory=list, description="Key obligations for this party")
    key_rights: list[str] = Field(default_factory=list, description="Key rights granted to this party")


class KeyDate(BaseModel):
    """An important date or deadline in the contract."""
    date: str = Field(description="The date or relative time reference")
    description: str = Field(description="What this date relates to")
    is_recurring: bool = Field(default=False, description="Whether this is a recurring date")


class KeyTerm(BaseModel):
    """A key term at a glance."""
    term: str = Field(description="Name of the term")
    value: str = Field(description="Value or description of the term")


class RecommendedAction(BaseModel):
    """A recommended action for the reader."""
    priority: str = Field(description="Priority: High, Medium, Low")
    action: str = Field(description="Description of the recommended action")
    reason: str = Field(default="", description="Why this action is recommended")


class ExecutiveSummary(BaseModel):
    """Complete executive summary output."""
    contract_title: str = Field(description="Title or type of the contract")
    parties: list[str] = Field(default_factory=list, description="All parties to the contract")
    effective_date: str = Field(default="", description="When the contract takes effect")
    expiration_date: str = Field(default="", description="When the contract expires")
    purpose: str = Field(description="Brief statement of the contract's purpose")
    key_terms_at_a_glance: list[KeyTerm] = Field(default_factory=list, description="Key terms overview")
    financial_summary: str = Field(default="", description="Summary of financial terms")
    party_obligations: list[PartyObligation] = Field(default_factory=list, description="Obligations per party")
    key_dates_and_deadlines: list[KeyDate] = Field(default_factory=list, description="Important dates and deadlines")
    risk_highlights: list[str] = Field(default_factory=list, description="Top risk highlights to be aware of")
    recommended_actions: list[RecommendedAction] = Field(default_factory=list, description="Recommended next steps")
    plain_english_summary: str = Field(description="2-3 paragraph summary in plain English")


SUMMARY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert legal analyst who creates clear, actionable executive
summaries of contracts for business stakeholders. Your summaries should be understandable
by non-lawyers while capturing all critical details.

Generate a comprehensive executive summary covering:

1. KEY TERMS AT A GLANCE
   - Contract type, parties, term/duration
   - Financial terms (total value, payment schedule)
   - Key performance metrics (SLAs, deliverables)
   - Liability cap, indemnification scope

2. OBLIGATIONS PER PARTY
   For each party, list:
   - Primary obligations and deliverables
   - Key rights and protections
   - Performance standards to meet

3. KEY DATES AND DEADLINES
   - Effective date and expiration
   - Payment milestones
   - Notice periods (termination, renewal)
   - Cure periods
   - Reporting or audit deadlines

4. RISK HIGHLIGHTS
   - Top 3-5 risk areas to be aware of
   - Any unusual or non-standard provisions

5. RECOMMENDED ACTIONS
   Prioritized list of actions for the reviewer:
   - Items to negotiate before signing
   - Internal preparations needed
   - Compliance steps required
   - Calendar reminders to set

6. PLAIN ENGLISH SUMMARY
   Write a 2-3 paragraph summary that a non-lawyer executive could quickly read to
   understand the essence of the contract, key commitments, and what to watch out for.

{format_instructions}"""),
    ("human", "Generate an executive summary for the following contract:\n\n{contract_text}"),
])


class SummaryGenerator:
    """Generates executive summaries of legal contracts using LLM."""

    def __init__(self, model_name: Optional[str] = None):
        self.llm = ChatOpenAI(
            model=model_name or OPENAI_MODEL,
            temperature=0.1,
        )
        self.parser = PydanticOutputParser(pydantic_object=ExecutiveSummary)

    def summarize(self, contract_text: str) -> ExecutiveSummary:
        """Generate executive summary for a contract."""
        chain = SUMMARY_PROMPT | self.llm | self.parser
        result = chain.invoke({
            "contract_text": contract_text,
            "format_instructions": self.parser.get_format_instructions(),
        })
        return result

    def summarize_as_dict(self, contract_text: str) -> dict:
        """Summarize and return as dictionary."""
        return self.summarize(contract_text).model_dump()

    def summarize_as_json(self, contract_text: str) -> str:
        """Summarize and return as JSON string."""
        return self.summarize(contract_text).model_dump_json(indent=2)
