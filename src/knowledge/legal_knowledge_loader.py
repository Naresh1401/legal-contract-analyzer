"""Load legal reference documents, chunk them, and embed into ChromaDB."""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")
CONTRACTS_DIR = os.getenv("CONTRACTS_DIR", "./data/contracts")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# Legal reference knowledge for RAG context
LEGAL_REFERENCE_DOCS = [
    {
        "title": "Standard Contract Clause Guidelines",
        "content": """
STANDARD CONTRACT CLAUSES REFERENCE GUIDE

1. INDEMNIFICATION CLAUSE
A standard indemnification clause should specify:
- Which party indemnifies the other
- Scope of indemnification (third-party claims, direct damages)
- Carve-outs and exceptions
- Notice requirements for claims
- Control of defense provisions
Risk: Missing mutual indemnification creates one-sided liability exposure.

2. LIMITATION OF LIABILITY
Standard provisions include:
- Cap on total liability (typically 12 months of fees)
- Exclusion of consequential, incidental, and punitive damages
- Carve-outs for IP infringement, confidentiality breaches, gross negligence
Risk: Unlimited liability or no cap exposes a party to disproportionate risk.

3. TERMINATION PROVISIONS
Should include:
- Termination for convenience with notice period (30-90 days)
- Termination for cause with cure period (30 days typical)
- Termination for insolvency/bankruptcy
- Effect of termination (survival clauses, wind-down obligations)
- Data return/destruction obligations
Risk: No termination for convenience locks party into unfavorable terms.

4. INTELLECTUAL PROPERTY
Key elements:
- Clear IP ownership assignment or license grant
- Work-for-hire vs. license distinction
- Pre-existing IP carve-outs
- Rights to derivative works
Risk: Ambiguous IP ownership leads to disputes over work product.

5. CONFIDENTIALITY / NON-DISCLOSURE
Must specify:
- Definition of confidential information
- Exclusions (publicly known, independently developed)
- Duration of obligations (2-5 years typical, indefinite for trade secrets)
- Permitted disclosures (legal requirements, advisors)
Risk: Overly broad definitions burden the receiving party.

6. DATA PROTECTION
For GDPR compliance:
- Data processing agreement (DPA) required
- Lawful basis for processing
- Data subject rights procedures
- Cross-border transfer mechanisms
- Breach notification timelines (72 hours under GDPR)
- Sub-processor management
Risk: Missing DPA violates GDPR Article 28.

7. NON-COMPETE / NON-SOLICITATION
Enforceability requires:
- Reasonable geographic scope
- Reasonable time limitation (1-2 years typical)
- Consideration provided
- Narrowly defined restricted activities
Risk: Overly broad restrictions may be unenforceable.

8. PAYMENT TERMS
Standard elements:
- Payment schedule and milestones
- Invoice requirements and net terms (Net 30 typical)
- Late payment penalties
- Currency and tax treatment
- Right to suspend services for non-payment
Risk: No late payment provisions incentivize delayed payments.

9. SERVICE LEVEL AGREEMENTS (SLA)
Should define:
- Uptime guarantees (99.9% typical)
- Response time commitments
- Remedies for SLA breach (service credits)
- Measurement methodology
- Exclusions (scheduled maintenance, force majeure)
Risk: No SLA remedies make uptime commitments meaningless.

10. FORCE MAJEURE
Standard provision covers:
- Natural disasters, war, terrorism
- Government actions, pandemics
- Notice requirements
- Obligation to mitigate
- Right to terminate if event persists (90-180 days typical)
Risk: Overly narrow definition leaves gaps in protection.
""",
    },
    {
        "title": "GDPR Compliance Checklist for Contracts",
        "content": """
GDPR COMPLIANCE REQUIREMENTS FOR CONTRACTS

Article 28 — Processor Obligations:
- Written contract or binding act required
- Process data only on documented instructions
- Ensure confidentiality commitments from personnel
- Implement appropriate technical and organizational security measures
- Sub-processor requirements: prior authorization, flow-down obligations
- Assist controller with data subject rights requests
- Delete or return data after service ends
- Make available information for audits

Article 32 — Security Measures:
- Pseudonymization and encryption of personal data
- Ability to ensure ongoing confidentiality, integrity, availability
- Ability to restore access to data in timely manner
- Regular testing and evaluation of security measures

Article 33 — Breach Notification:
- Notify supervisory authority within 72 hours
- Document all breaches regardless of risk
- Notify data subjects when high risk to rights and freedoms

Cross-Border Transfers (Chapter V):
- Adequacy decisions
- Standard Contractual Clauses (SCCs)
- Binding Corporate Rules
- Transfer Impact Assessments required post-Schrems II

Data Subject Rights (Articles 15-22):
- Right of access
- Right to rectification
- Right to erasure (right to be forgotten)
- Right to restriction of processing
- Right to data portability
- Right to object
- Rights regarding automated decision-making
""",
    },
    {
        "title": "SOC 2 Contract Requirements",
        "content": """
SOC 2 SECURITY PROVISIONS FOR CONTRACTS

Trust Service Criteria Requirements:

1. Security (Common Criteria):
- Access control policies
- Network and infrastructure security
- Security incident management
- Change management procedures
- Risk assessment processes

2. Availability:
- System uptime commitments
- Disaster recovery and business continuity
- Backup and restoration procedures
- Capacity planning

3. Processing Integrity:
- Data processing accuracy and completeness
- Error handling and correction
- Quality assurance procedures

4. Confidentiality:
- Classification of confidential information
- Encryption requirements (at rest and in transit)
- Access restrictions based on need-to-know
- Secure disposal of confidential data

5. Privacy:
- Notice and consent for data collection
- Choice and opt-out mechanisms
- Use limitation to stated purposes
- Retention and disposal policies
- Access and correction rights

Contract Provisions:
- Right to audit or review SOC 2 report
- Requirement to maintain SOC 2 Type II certification
- Notification of material changes to security controls
- Incident notification timelines
- Sub-service organization requirements
""",
    },
]


def build_reference_documents() -> list:
    """Create LangChain documents from legal reference content."""
    from langchain_core.documents import Document

    documents = []
    for ref in LEGAL_REFERENCE_DOCS:
        doc = Document(
            page_content=ref["content"],
            metadata={"source": ref["title"], "type": "legal_reference"},
        )
        documents.append(doc)
    return documents


def load_contract_files() -> list:
    """Load contract files from the contracts directory."""
    contracts_path = Path(CONTRACTS_DIR)
    if not contracts_path.exists():
        print(f"Contracts directory not found: {CONTRACTS_DIR}")
        return []

    loader = DirectoryLoader(
        str(contracts_path),
        glob="**/*.txt",
        loader_cls=TextLoader,
        show_progress=True,
    )
    return loader.load()


def chunk_documents(documents: list, chunk_size: int = 1000, chunk_overlap: int = 200) -> list:
    """Split documents into chunks for embedding."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(documents)


def create_vector_store(documents: list) -> Chroma:
    """Create or update ChromaDB vector store with document embeddings."""
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    persist_path = Path(CHROMA_PERSIST_DIR)
    persist_path.mkdir(parents=True, exist_ok=True)

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=str(persist_path),
        collection_name="legal_knowledge",
    )
    print(f"Vector store created with {len(documents)} chunks at {persist_path}")
    return vector_store


def get_vector_store() -> Chroma:
    """Load existing vector store for retrieval."""
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    return Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="legal_knowledge",
    )


def build_knowledge_base():
    """Main pipeline: load documents, chunk, embed, and persist."""
    print("Building legal knowledge base...")

    # Load reference documents
    ref_docs = build_reference_documents()
    print(f"Loaded {len(ref_docs)} reference documents")

    # Load contract files
    contract_docs = load_contract_files()
    print(f"Loaded {len(contract_docs)} contract files")

    all_docs = ref_docs + contract_docs

    # Chunk
    chunks = chunk_documents(all_docs)
    print(f"Created {len(chunks)} chunks")

    # Embed and store
    vector_store = create_vector_store(chunks)
    return vector_store


if __name__ == "__main__":
    build_knowledge_base()
