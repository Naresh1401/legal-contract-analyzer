"""FastAPI backend for the Legal Contract Analyzer."""

import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.agents.clause_extractor import ClauseExtractor
from src.agents.risk_analyzer import RiskAnalyzer
from src.agents.compliance_checker import ComplianceChecker
from src.agents.contract_comparator import ContractComparator
from src.agents.summary_generator import SummaryGenerator

load_dotenv()

app = FastAPI(
    title="Legal Contract Analyzer API",
    description="AI-powered contract review with clause extraction, risk analysis, compliance checking, and comparison",
    version="1.0.0",
)

# Initialize agents
clause_extractor = ClauseExtractor()
risk_analyzer = RiskAnalyzer()
compliance_checker = ComplianceChecker()
contract_comparator = ContractComparator()
summary_generator = SummaryGenerator()


# --- Request / Response Models ---

class ContractInput(BaseModel):
    """Input model for single contract analysis."""
    contract_text: str = Field(..., min_length=50, description="Full text of the contract to analyze")


class ComplianceInput(BaseModel):
    """Input model for compliance checking."""
    contract_text: str = Field(..., min_length=50, description="Full text of the contract")
    frameworks: Optional[list[str]] = Field(
        default=None,
        description="Compliance frameworks to check (e.g., ['GDPR', 'SOC 2']). Defaults to GDPR + SOC 2.",
    )


class CompareInput(BaseModel):
    """Input model for contract comparison."""
    contract_a: str = Field(..., min_length=50, description="Full text of the first contract")
    contract_b: str = Field(..., min_length=50, description="Full text of the second contract")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str


# --- Endpoints ---

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="1.0.0")


@app.post("/analyze/clauses")
async def analyze_clauses(payload: ContractInput):
    """Extract key clauses from a contract."""
    try:
        result = clause_extractor.extract_as_dict(payload.contract_text)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clause extraction failed: {str(e)}")


@app.post("/analyze/risks")
async def analyze_risks(payload: ContractInput):
    """Analyze contract for risks."""
    try:
        result = risk_analyzer.analyze_as_dict(payload.contract_text)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk analysis failed: {str(e)}")


@app.post("/check/compliance")
async def check_compliance(payload: ComplianceInput):
    """Check contract against compliance frameworks."""
    try:
        result = compliance_checker.check_as_dict(payload.contract_text, payload.frameworks)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compliance check failed: {str(e)}")


@app.post("/compare")
async def compare_contracts(payload: CompareInput):
    """Compare two contracts side by side."""
    try:
        result = contract_comparator.compare_as_dict(payload.contract_a, payload.contract_b)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Contract comparison failed: {str(e)}")


@app.post("/summarize")
async def summarize_contract(payload: ContractInput):
    """Generate an executive summary of a contract."""
    try:
        result = summary_generator.summarize_as_dict(payload.contract_text)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summary generation failed: {str(e)}")
