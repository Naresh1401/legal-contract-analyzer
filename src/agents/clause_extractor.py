"""LangChain agent for extracting key clauses from legal contracts."""

import json
import os
from typing import Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")


class ClauseDetail(BaseModel):
    """A single extracted clause."""
    clause_type: str = Field(description="Type of clause (e.g., 'Indemnification', 'Termination')")
    present: bool = Field(description="Whether this clause is found in the contract")
    summary: str = Field(default="", description="Brief summary of the clause content")
    key_terms: list[str] = Field(default_factory=list, description="Key terms or conditions in this clause")
    section_reference: str = Field(default="", description="Section number or heading where clause appears")
    full_text_excerpt: str = Field(default="", description="Relevant excerpt from the contract")


class ExtractedClauses(BaseModel):
    """Structured output for all extracted clauses."""
    parties: dict = Field(default_factory=dict, description="Parties to the contract with roles")
    effective_date: str = Field(default="", description="Effective date of the contract")
    contract_type: str = Field(default="", description="Type of contract (NDA, SaaS, Employment, etc.)")
    term_duration: str = Field(default="", description="Duration/term of the contract")
    clauses: list[ClauseDetail] = Field(default_factory=list, description="List of extracted clauses")
    governing_law: str = Field(default="", description="Governing law jurisdiction")
    dispute_resolution: str = Field(default="", description="Dispute resolution mechanism")


EXTRACTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert legal contract analyst. Your task is to carefully read
the provided contract and extract all key clauses into a structured format.

For each clause type below, determine if it is present and extract the relevant details:
- Parties and their roles
- Effective date
- Term / Duration
- Termination provisions (for cause, for convenience, notice periods)
- Indemnification (mutual vs. one-sided, scope, carve-outs)
- Limitation of liability (cap amount, exclusions, carve-outs)
- Intellectual property (ownership, assignment, licenses)
- Non-compete provisions (scope, duration, geographic limits)
- Non-solicitation provisions (scope, duration)
- Confidentiality / NDA (definition, duration, exceptions)
- Payment terms (amounts, schedule, late fees)
- Service Level Agreement / SLA (uptime, credits, response times)
- Data protection / Privacy (GDPR, security measures, breach notification)
- Force majeure
- Governing law and dispute resolution
- Insurance requirements
- Representations and warranties

Be precise and reference specific section numbers where possible.

{format_instructions}"""),
    ("human", "Analyze the following contract and extract all key clauses:\n\n{contract_text}"),
])


class ClauseExtractor:
    """Extracts key clauses from legal contracts using an LLM."""

    def __init__(self, model_name: Optional[str] = None):
        self.llm = ChatOpenAI(
            model=model_name or OPENAI_MODEL,
            temperature=0,
        )
        self.parser = PydanticOutputParser(pydantic_object=ExtractedClauses)

    def extract(self, contract_text: str) -> ExtractedClauses:
        """Extract clauses from contract text."""
        chain = EXTRACTION_PROMPT | self.llm | self.parser
        result = chain.invoke({
            "contract_text": contract_text,
            "format_instructions": self.parser.get_format_instructions(),
        })
        return result

    def extract_as_dict(self, contract_text: str) -> dict:
        """Extract clauses and return as dictionary."""
        result = self.extract(contract_text)
        return result.model_dump()

    def extract_as_json(self, contract_text: str) -> str:
        """Extract clauses and return as JSON string."""
        result = self.extract(contract_text)
        return result.model_dump_json(indent=2)
