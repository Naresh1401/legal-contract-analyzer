"""LangChain agent for checking contract compliance against regulatory frameworks."""

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


class ComplianceGap(BaseModel):
    """A single compliance gap."""
    gap_id: str = Field(description="Unique identifier (e.g., GAP-001)")
    framework: str = Field(description="Compliance framework (GDPR, SOC 2, HIPAA, PCI-DSS, etc.)")
    requirement: str = Field(description="Specific regulatory requirement")
    article_reference: str = Field(default="", description="Article or section reference (e.g., GDPR Art. 28)")
    status: str = Field(description="Status: Compliant, Partially Compliant, Non-Compliant, Not Applicable")
    gap_description: str = Field(default="", description="Description of the compliance gap if not fully compliant")
    severity: str = Field(default="Medium", description="Severity: Critical, High, Medium, Low")
    recommendation: str = Field(default="", description="Recommended action to achieve compliance")
    suggested_clause: str = Field(default="", description="Suggested contract language to address the gap")


class ComplianceReport(BaseModel):
    """Complete compliance check output."""
    contract_type: str = Field(default="", description="Type of contract analyzed")
    frameworks_checked: list[str] = Field(default_factory=list, description="Compliance frameworks evaluated")
    overall_compliance_score: int = Field(description="Overall compliance percentage (0-100)")
    compliant_count: int = Field(default=0, description="Number of fully compliant requirements")
    partial_count: int = Field(default=0, description="Number of partially compliant requirements")
    non_compliant_count: int = Field(default=0, description="Number of non-compliant requirements")
    not_applicable_count: int = Field(default=0, description="Number of non-applicable requirements")
    gaps: list[ComplianceGap] = Field(default_factory=list, description="List of compliance gaps")
    summary: str = Field(description="Executive summary of compliance status")
    priority_actions: list[str] = Field(default_factory=list, description="Top priority actions to improve compliance")


COMPLIANCE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert legal compliance analyst specializing in regulatory frameworks.
Analyze the provided contract against the following compliance frameworks and identify gaps.

FRAMEWORKS TO CHECK:

1. GDPR (General Data Protection Regulation):
   - Article 28: Data processing agreement requirements
   - Article 32: Security measures (encryption, pseudonymization, resilience)
   - Article 33: Breach notification (72-hour timeline)
   - Article 44-49: Cross-border data transfer safeguards
   - Data subject rights provisions (Articles 15-22)
   - Data retention and deletion obligations
   - Sub-processor management
   - Lawful basis for processing

2. SOC 2 Trust Service Criteria:
   - Security: Access controls, incident management, change management
   - Availability: Uptime commitments, DR/BCP, backup/restore
   - Processing Integrity: Data accuracy, QA procedures
   - Confidentiality: Classification, encryption, secure disposal
   - Privacy: Notice, consent, use limitation, retention

3. INDUSTRY-SPECIFIC REGULATIONS:
   - If the contract involves healthcare data: HIPAA requirements
   - If the contract involves payment data: PCI-DSS requirements
   - If the contract involves financial data: SOX requirements
   - California-specific: CCPA/CPRA consumer privacy rights

For each requirement, assess whether the contract is:
- Compliant: Fully addresses the requirement
- Partially Compliant: Addresses some aspects but has gaps
- Non-Compliant: Does not address the requirement
- Not Applicable: Requirement does not apply to this contract

{format_instructions}

LEGAL REFERENCE CONTEXT:
{legal_context}"""),
    ("human", """Check the following contract for compliance gaps.
Frameworks to check: {frameworks}

CONTRACT:
{contract_text}"""),
])


class ComplianceChecker:
    """Checks contract compliance against regulatory frameworks using LLM + RAG."""

    DEFAULT_FRAMEWORKS = ["GDPR", "SOC 2"]

    def __init__(self, model_name: Optional[str] = None):
        self.llm = ChatOpenAI(
            model=model_name or OPENAI_MODEL,
            temperature=0,
        )
        self.parser = PydanticOutputParser(pydantic_object=ComplianceReport)

    def _get_legal_context(self, contract_text: str) -> str:
        """Retrieve relevant compliance knowledge from vector store."""
        try:
            vector_store = get_vector_store()
            docs = vector_store.similarity_search(
                "compliance GDPR SOC 2 data protection security", k=5
            )
            return "\n\n".join(doc.page_content for doc in docs)
        except Exception:
            return "No legal reference context available. Use general compliance knowledge."

    def check(
        self,
        contract_text: str,
        frameworks: Optional[list[str]] = None,
    ) -> ComplianceReport:
        """Check contract compliance against specified frameworks."""
        frameworks = frameworks or self.DEFAULT_FRAMEWORKS
        legal_context = self._get_legal_context(contract_text)

        chain = COMPLIANCE_PROMPT | self.llm | self.parser
        result = chain.invoke({
            "contract_text": contract_text,
            "frameworks": ", ".join(frameworks),
            "legal_context": legal_context,
            "format_instructions": self.parser.get_format_instructions(),
        })
        return result

    def check_as_dict(self, contract_text: str, frameworks: Optional[list[str]] = None) -> dict:
        """Check compliance and return as dictionary."""
        return self.check(contract_text, frameworks).model_dump()

    def check_as_json(self, contract_text: str, frameworks: Optional[list[str]] = None) -> str:
        """Check compliance and return as JSON string."""
        return self.check(contract_text, frameworks).model_dump_json(indent=2)
