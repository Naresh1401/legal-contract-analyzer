"""LangChain agent for analyzing risks in legal contracts."""

import os
from typing import Optional

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from src.knowledge.legal_knowledge_loader import get_vector_store

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")


class RiskItem(BaseModel):
    """A single identified risk."""
    risk_id: str = Field(description="Unique identifier for this risk (e.g., RISK-001)")
    category: str = Field(description="Risk category (Missing Clause, One-Sided Term, Liability Exposure, Weak Termination, Non-Standard Language, Ambiguity)")
    severity: str = Field(description="Severity: Critical, High, Medium, or Low")
    title: str = Field(description="Short title describing the risk")
    description: str = Field(description="Detailed description of the risk")
    section_reference: str = Field(default="", description="Relevant section of the contract")
    recommendation: str = Field(description="Recommended action to mitigate the risk")
    standard_language: str = Field(default="", description="Suggested standard language to address the risk")


class RiskAnalysis(BaseModel):
    """Complete risk analysis output."""
    contract_type: str = Field(default="", description="Type of contract analyzed")
    overall_risk_level: str = Field(description="Overall risk level: Critical, High, Medium, or Low")
    risk_score: int = Field(description="Numerical risk score from 0 (no risk) to 100 (maximum risk)")
    total_risks: int = Field(description="Total number of risks identified")
    critical_count: int = Field(default=0, description="Number of critical risks")
    high_count: int = Field(default=0, description="Number of high risks")
    medium_count: int = Field(default=0, description="Number of medium risks")
    low_count: int = Field(default=0, description="Number of low risks")
    risks: list[RiskItem] = Field(default_factory=list, description="List of identified risks")
    executive_summary: str = Field(description="Brief executive summary of the risk analysis")


RISK_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert legal risk analyst. Analyze the provided contract for
potential risks and issues. Use the legal reference knowledge provided for context
on standard clauses and best practices.

Evaluate the contract for the following risk categories:

1. MISSING STANDARD CLAUSES - Identify clauses that should be present but are missing:
   - Indemnification, limitation of liability, termination, confidentiality
   - Data protection, force majeure, dispute resolution, IP ownership
   - Insurance requirements, representations and warranties

2. ONE-SIDED TERMS - Flag provisions that disproportionately favor one party:
   - Unilateral termination rights
   - Asymmetric indemnification
   - Broad IP assignment without compensation
   - Unfair payment terms

3. UNLIMITED LIABILITY EXPOSURE - Identify areas of uncapped risk:
   - No liability cap or unreasonably high cap
   - Missing consequential damages exclusion
   - Broad indemnification without carve-outs

4. WEAK TERMINATION RIGHTS - Assess termination provisions:
   - No termination for convenience
   - Excessive notice periods
   - No cure periods for breach
   - Auto-renewal without notice mechanism

5. NON-STANDARD LANGUAGE - Flag unusual or non-standard provisions:
   - Unusual definitions
   - Non-standard governing law
   - Atypical remedies or penalties
   - Unusual assignment restrictions

6. AMBIGUITY - Identify vague or unclear provisions:
   - Undefined key terms
   - Ambiguous obligations
   - Conflicting provisions

Assign severity levels:
- Critical: Immediate legal or financial exposure requiring urgent attention
- High: Significant risk that should be addressed before signing
- Medium: Notable concern that should be negotiated if possible
- Low: Minor issue to be aware of

{format_instructions}

LEGAL REFERENCE CONTEXT:
{legal_context}"""),
    ("human", "Analyze the following contract for risks:\n\n{contract_text}"),
])


class RiskAnalyzer:
    """Analyzes contracts for legal and business risks using LLM + RAG."""

    def __init__(self, model_name: Optional[str] = None):
        self.llm = ChatOpenAI(
            model=model_name or OPENAI_MODEL,
            temperature=0,
        )
        self.parser = PydanticOutputParser(pydantic_object=RiskAnalysis)

    def _get_legal_context(self, contract_text: str) -> str:
        """Retrieve relevant legal knowledge from vector store."""
        try:
            vector_store = get_vector_store()
            docs = vector_store.similarity_search(contract_text, k=5)
            return "\n\n".join(doc.page_content for doc in docs)
        except Exception:
            return "No legal reference context available. Use general legal knowledge."

    def analyze(self, contract_text: str) -> RiskAnalysis:
        """Perform risk analysis on a contract."""
        legal_context = self._get_legal_context(contract_text)

        chain = RISK_ANALYSIS_PROMPT | self.llm | self.parser
        result = chain.invoke({
            "contract_text": contract_text,
            "legal_context": legal_context,
            "format_instructions": self.parser.get_format_instructions(),
        })
        return result

    def analyze_as_dict(self, contract_text: str) -> dict:
        """Analyze and return as dictionary."""
        return self.analyze(contract_text).model_dump()

    def analyze_as_json(self, contract_text: str) -> str:
        """Analyze and return as JSON string."""
        return self.analyze(contract_text).model_dump_json(indent=2)
