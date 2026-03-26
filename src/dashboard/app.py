"""Streamlit dashboard for the Legal Contract Analyzer."""

import json
import streamlit as st

from src.agents.clause_extractor import ClauseExtractor
from src.agents.risk_analyzer import RiskAnalyzer
from src.agents.compliance_checker import ComplianceChecker
from src.agents.contract_comparator import ContractComparator
from src.agents.summary_generator import SummaryGenerator
from src.knowledge.sample_contracts import SAMPLE_CONTRACTS

# --- Page Config ---
st.set_page_config(
    page_title="Legal Contract Analyzer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Sidebar ---
st.sidebar.title("⚖️ Legal Contract Analyzer")
st.sidebar.markdown("AI-powered contract review with LangChain & RAG")

analysis_mode = st.sidebar.radio(
    "Analysis Mode",
    [
        "📋 Clause Extraction",
        "⚠️ Risk Analysis",
        "✅ Compliance Check",
        "🔄 Contract Comparison",
        "📝 Executive Summary",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Sample Contracts**")
sample_choice = st.sidebar.selectbox(
    "Load a sample contract",
    ["None"] + list(SAMPLE_CONTRACTS.keys()),
)


# --- Helpers ---
@st.cache_resource
def get_clause_extractor():
    return ClauseExtractor()


@st.cache_resource
def get_risk_analyzer():
    return RiskAnalyzer()


@st.cache_resource
def get_compliance_checker():
    return ComplianceChecker()


@st.cache_resource
def get_comparator():
    return ContractComparator()


@st.cache_resource
def get_summary_generator():
    return SummaryGenerator()


def get_contract_text() -> str:
    """Get contract text from input methods."""
    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader(
            "Upload a contract file", type=["txt", "pdf", "docx"]
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if sample_choice != "None":
            if st.button("Load Sample"):
                st.session_state["contract_text"] = SAMPLE_CONTRACTS[sample_choice].strip()

    default_text = st.session_state.get("contract_text", "")

    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            default_text = uploaded_file.read().decode("utf-8")
        else:
            st.warning("PDF and DOCX parsing requires additional setup. Please paste the text directly.")

    contract_text = st.text_area(
        "Or paste contract text below",
        value=default_text,
        height=300,
        placeholder="Paste the full contract text here...",
    )
    return contract_text


# --- Analysis Views ---

def clause_extraction_view():
    """Clause extraction analysis view."""
    st.header("📋 Clause Extraction")
    st.markdown("Extract and structure key clauses from your contract.")

    contract_text = get_contract_text()

    if st.button("🔍 Extract Clauses", type="primary", disabled=not contract_text):
        with st.spinner("Extracting clauses with AI..."):
            extractor = get_clause_extractor()
            result = extractor.extract_as_dict(contract_text)

        # Contract overview
        st.subheader("Contract Overview")
        overview_cols = st.columns(4)
        overview_cols[0].metric("Type", result.get("contract_type", "N/A"))
        overview_cols[1].metric("Effective Date", result.get("effective_date", "N/A"))
        overview_cols[2].metric("Term", result.get("term_duration", "N/A"))
        overview_cols[3].metric("Governing Law", result.get("governing_law", "N/A"))

        # Parties
        if result.get("parties"):
            st.subheader("Parties")
            for role, name in result["parties"].items():
                st.markdown(f"**{role}:** {name}")

        # Clauses
        st.subheader("Extracted Clauses")
        for clause in result.get("clauses", []):
            status_icon = "✅" if clause.get("present") else "❌"
            with st.expander(f"{status_icon} {clause.get('clause_type', 'Unknown')} — {clause.get('section_reference', '')}"):
                st.markdown(f"**Summary:** {clause.get('summary', 'N/A')}")
                if clause.get("key_terms"):
                    st.markdown("**Key Terms:**")
                    for term in clause["key_terms"]:
                        st.markdown(f"- {term}")
                if clause.get("full_text_excerpt"):
                    st.markdown("**Excerpt:**")
                    st.code(clause["full_text_excerpt"], language=None)

        # Raw JSON
        with st.expander("📄 Raw JSON Output"):
            st.json(result)


def risk_analysis_view():
    """Risk analysis dashboard view."""
    st.header("⚠️ Risk Analysis")
    st.markdown("Identify potential risks and issues in your contract.")

    contract_text = get_contract_text()

    if st.button("🔍 Analyze Risks", type="primary", disabled=not contract_text):
        with st.spinner("Analyzing contract risks..."):
            analyzer = get_risk_analyzer()
            result = analyzer.analyze_as_dict(contract_text)

        # Score & overview
        st.subheader("Risk Overview")
        score_cols = st.columns(5)
        score_cols[0].metric("Risk Score", f"{result.get('risk_score', 0)}/100")
        score_cols[1].metric("🔴 Critical", result.get("critical_count", 0))
        score_cols[2].metric("🟠 High", result.get("high_count", 0))
        score_cols[3].metric("🟡 Medium", result.get("medium_count", 0))
        score_cols[4].metric("🟢 Low", result.get("low_count", 0))

        # Severity chart
        severity_data = {
            "Severity": ["Critical", "High", "Medium", "Low"],
            "Count": [
                result.get("critical_count", 0),
                result.get("high_count", 0),
                result.get("medium_count", 0),
                result.get("low_count", 0),
            ],
        }
        st.bar_chart(severity_data, x="Severity", y="Count")

        # Executive summary
        st.subheader("Executive Summary")
        st.info(result.get("executive_summary", ""))

        # Individual risks
        st.subheader("Identified Risks")
        for risk in result.get("risks", []):
            severity = risk.get("severity", "Medium")
            color_map = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}
            icon = color_map.get(severity, "⚪")
            with st.expander(f"{icon} [{severity}] {risk.get('risk_id', '')} — {risk.get('title', '')}"):
                st.markdown(f"**Category:** {risk.get('category', 'N/A')}")
                st.markdown(f"**Description:** {risk.get('description', '')}")
                if risk.get("section_reference"):
                    st.markdown(f"**Section:** {risk['section_reference']}")
                st.markdown(f"**Recommendation:** {risk.get('recommendation', '')}")
                if risk.get("standard_language"):
                    st.markdown("**Suggested Language:**")
                    st.code(risk["standard_language"], language=None)

        with st.expander("📄 Raw JSON Output"):
            st.json(result)


def compliance_check_view():
    """Compliance checking view."""
    st.header("✅ Compliance Check")
    st.markdown("Check your contract against regulatory compliance frameworks.")

    contract_text = get_contract_text()

    frameworks = st.multiselect(
        "Select compliance frameworks",
        ["GDPR", "SOC 2", "HIPAA", "PCI-DSS", "CCPA"],
        default=["GDPR", "SOC 2"],
    )

    if st.button("🔍 Check Compliance", type="primary", disabled=not contract_text):
        with st.spinner("Checking compliance..."):
            checker = get_compliance_checker()
            result = checker.check_as_dict(contract_text, frameworks)

        # Score
        st.subheader("Compliance Overview")
        score_cols = st.columns(5)
        score_cols[0].metric("Compliance Score", f"{result.get('overall_compliance_score', 0)}%")
        score_cols[1].metric("✅ Compliant", result.get("compliant_count", 0))
        score_cols[2].metric("🟡 Partial", result.get("partial_count", 0))
        score_cols[3].metric("❌ Non-Compliant", result.get("non_compliant_count", 0))
        score_cols[4].metric("➖ N/A", result.get("not_applicable_count", 0))

        # Summary
        st.subheader("Summary")
        st.info(result.get("summary", ""))

        # Priority actions
        if result.get("priority_actions"):
            st.subheader("Priority Actions")
            for i, action in enumerate(result["priority_actions"], 1):
                st.markdown(f"**{i}.** {action}")

        # Gap table
        st.subheader("Compliance Gap Details")
        gaps = result.get("gaps", [])
        if gaps:
            for gap in gaps:
                status = gap.get("status", "")
                status_map = {
                    "Compliant": "✅",
                    "Partially Compliant": "🟡",
                    "Non-Compliant": "❌",
                    "Not Applicable": "➖",
                }
                icon = status_map.get(status, "⚪")
                with st.expander(f"{icon} [{gap.get('framework', '')}] {gap.get('requirement', '')}"):
                    st.markdown(f"**Status:** {status}")
                    st.markdown(f"**Article:** {gap.get('article_reference', 'N/A')}")
                    st.markdown(f"**Severity:** {gap.get('severity', 'N/A')}")
                    if gap.get("gap_description"):
                        st.markdown(f"**Gap:** {gap['gap_description']}")
                    if gap.get("recommendation"):
                        st.markdown(f"**Recommendation:** {gap['recommendation']}")
                    if gap.get("suggested_clause"):
                        st.markdown("**Suggested Clause:**")
                        st.code(gap["suggested_clause"], language=None)

        with st.expander("📄 Raw JSON Output"):
            st.json(result)


def contract_comparison_view():
    """Contract comparison view."""
    st.header("🔄 Contract Comparison")
    st.markdown("Compare two contracts side by side to identify differences.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Contract A")
        sample_a = st.selectbox("Load sample for A", ["None"] + list(SAMPLE_CONTRACTS.keys()), key="sample_a")
        default_a = SAMPLE_CONTRACTS.get(sample_a, "").strip() if sample_a != "None" else ""
        contract_a = st.text_area("Contract A text", value=default_a, height=300, key="contract_a_input")

    with col2:
        st.subheader("Contract B")
        sample_b = st.selectbox("Load sample for B", ["None"] + list(SAMPLE_CONTRACTS.keys()), key="sample_b")
        default_b = SAMPLE_CONTRACTS.get(sample_b, "").strip() if sample_b != "None" else ""
        contract_b = st.text_area("Contract B text", value=default_b, height=300, key="contract_b_input")

    if st.button("🔍 Compare Contracts", type="primary", disabled=not (contract_a and contract_b)):
        with st.spinner("Comparing contracts..."):
            comparator = get_comparator()
            result = comparator.compare_as_dict(contract_a, contract_b)

        # Overview
        st.subheader("Comparison Overview")
        overview_cols = st.columns(4)
        overview_cols[0].metric("Total Differences", result.get("total_differences", 0))
        overview_cols[1].metric("👍 Advantageous", result.get("advantageous_changes", 0))
        overview_cols[2].metric("👎 Disadvantageous", result.get("disadvantageous_changes", 0))
        overview_cols[3].metric("➖ Neutral", result.get("neutral_changes", 0))

        # Redline summary
        st.subheader("Redline Summary")
        st.markdown(result.get("redline_summary", ""))

        # Recommendation
        st.subheader("Recommendation")
        st.info(result.get("recommendation", ""))

        # Differences
        st.subheader("Clause-by-Clause Differences")
        for diff in result.get("differences", []):
            impact = diff.get("impact", "Neutral")
            impact_map = {"Advantageous": "👍", "Disadvantageous": "👎", "Neutral": "➖"}
            icon = impact_map.get(impact, "⚪")
            with st.expander(f"{icon} {diff.get('clause_type', '')} — {diff.get('difference_type', '')}"):
                st.markdown(f"**Impact:** {impact} ({diff.get('impact_for', '')})")
                st.markdown(f"**Significance:** {diff.get('significance', 'N/A')}")
                st.markdown(f"**Description:** {diff.get('description', '')}")
                dcol1, dcol2 = st.columns(2)
                with dcol1:
                    st.markdown("**Contract A:**")
                    st.code(diff.get("contract_a_text", "Not present"), language=None)
                with dcol2:
                    st.markdown("**Contract B:**")
                    st.code(diff.get("contract_b_text", "Not present"), language=None)

        with st.expander("📄 Raw JSON Output"):
            st.json(result)


def executive_summary_view():
    """Executive summary generator view."""
    st.header("📝 Executive Summary")
    st.markdown("Generate a clear, actionable executive summary of your contract.")

    contract_text = get_contract_text()

    if st.button("🔍 Generate Summary", type="primary", disabled=not contract_text):
        with st.spinner("Generating executive summary..."):
            generator = get_summary_generator()
            result = generator.summarize_as_dict(contract_text)

        # Header info
        st.subheader(result.get("contract_title", "Contract Summary"))
        info_cols = st.columns(3)
        info_cols[0].metric("Effective Date", result.get("effective_date", "N/A"))
        info_cols[1].metric("Expiration", result.get("expiration_date", "N/A"))
        info_cols[2].metric("Parties", str(len(result.get("parties", []))))

        # Purpose
        st.subheader("Purpose")
        st.markdown(result.get("purpose", ""))

        # Key terms at a glance
        if result.get("key_terms_at_a_glance"):
            st.subheader("Key Terms at a Glance")
            for term in result["key_terms_at_a_glance"]:
                st.markdown(f"- **{term.get('term', '')}:** {term.get('value', '')}")

        # Financial summary
        if result.get("financial_summary"):
            st.subheader("💰 Financial Summary")
            st.markdown(result["financial_summary"])

        # Obligations per party
        if result.get("party_obligations"):
            st.subheader("Party Obligations")
            for party in result["party_obligations"]:
                with st.expander(f"📌 {party.get('party_name', '')} ({party.get('role', '')})"):
                    if party.get("key_obligations"):
                        st.markdown("**Obligations:**")
                        for ob in party["key_obligations"]:
                            st.markdown(f"- {ob}")
                    if party.get("key_rights"):
                        st.markdown("**Rights:**")
                        for right in party["key_rights"]:
                            st.markdown(f"- {right}")

        # Key dates
        if result.get("key_dates_and_deadlines"):
            st.subheader("📅 Key Dates & Deadlines")
            for kd in result["key_dates_and_deadlines"]:
                recurring = " 🔁" if kd.get("is_recurring") else ""
                st.markdown(f"- **{kd.get('date', '')}** — {kd.get('description', '')}{recurring}")

        # Risk highlights
        if result.get("risk_highlights"):
            st.subheader("⚠️ Risk Highlights")
            for rh in result["risk_highlights"]:
                st.markdown(f"- {rh}")

        # Recommended actions
        if result.get("recommended_actions"):
            st.subheader("✅ Recommended Actions")
            for ra in result["recommended_actions"]:
                priority_map = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                icon = priority_map.get(ra.get("priority", ""), "⚪")
                st.markdown(f"{icon} **[{ra.get('priority', '')}]** {ra.get('action', '')}")
                if ra.get("reason"):
                    st.markdown(f"  _{ra['reason']}_")

        # Plain English summary
        st.subheader("📖 Plain English Summary")
        st.markdown(result.get("plain_english_summary", ""))

        with st.expander("📄 Raw JSON Output"):
            st.json(result)


# --- Main ---

view_map = {
    "📋 Clause Extraction": clause_extraction_view,
    "⚠️ Risk Analysis": risk_analysis_view,
    "✅ Compliance Check": compliance_check_view,
    "🔄 Contract Comparison": contract_comparison_view,
    "📝 Executive Summary": executive_summary_view,
}

view_map[analysis_mode]()
