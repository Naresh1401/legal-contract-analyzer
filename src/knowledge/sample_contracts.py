"""Generate synthetic sample contract text files for testing and demonstration."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

CONTRACTS_DIR = os.getenv("CONTRACTS_DIR", "./data/contracts")

SAMPLE_CONTRACTS = {
    "nda_mutual.txt": """MUTUAL NON-DISCLOSURE AGREEMENT

This Mutual Non-Disclosure Agreement ("Agreement") is entered into as of January 15, 2025
("Effective Date"), by and between:

Party A: TechCorp Solutions Inc., a Delaware corporation with its principal office at
1200 Innovation Drive, San Francisco, CA 94105 ("Disclosing Party")

AND

Party B: DataFlow Analytics LLC, a California limited liability company with its principal
office at 450 Market Street, Suite 300, San Francisco, CA 94107 ("Receiving Party")

(collectively the "Parties" and individually a "Party")

1. PURPOSE
The Parties wish to explore a potential business relationship regarding cloud-based data
analytics integration ("Purpose"). In connection with the Purpose, each Party may disclose
certain confidential and proprietary information to the other Party.

2. DEFINITION OF CONFIDENTIAL INFORMATION
"Confidential Information" means any non-public information disclosed by either Party to the
other Party, whether orally, in writing, or by inspection, including but not limited to:
(a) trade secrets, inventions, patents, copyrights, and know-how;
(b) business plans, financial data, customer lists, and pricing strategies;
(c) technical data, designs, algorithms, source code, and specifications;
(d) any information marked as "Confidential" or "Proprietary."

Exclusions: Confidential Information does not include information that:
(i) is or becomes publicly available through no fault of the Receiving Party;
(ii) was already known to the Receiving Party prior to disclosure;
(iii) is independently developed by the Receiving Party without use of Confidential Information;
(iv) is rightfully obtained from a third party without restriction.

3. OBLIGATIONS OF RECEIVING PARTY
The Receiving Party agrees to:
(a) Hold Confidential Information in strict confidence;
(b) Not disclose Confidential Information to any third party without prior written consent;
(c) Use Confidential Information solely for the Purpose;
(d) Limit access to employees and contractors with a need to know who are bound by
    confidentiality obligations no less restrictive than those herein;
(e) Protect Confidential Information using the same degree of care used for its own
    confidential information, but no less than reasonable care.

4. TERM AND TERMINATION
This Agreement shall remain in effect for two (2) years from the Effective Date.
Either Party may terminate this Agreement with thirty (30) days prior written notice.
The confidentiality obligations shall survive termination for a period of three (3) years.

5. RETURN OF MATERIALS
Upon termination or written request, the Receiving Party shall promptly return or destroy
all copies of Confidential Information and certify such destruction in writing.

6. NO LICENSE GRANTED
Nothing in this Agreement grants either Party any rights in the other Party's Confidential
Information except the limited right to use it for the Purpose.

7. REMEDIES
The Parties acknowledge that breach of this Agreement may cause irreparable harm for which
monetary damages would be inadequate. The non-breaching Party shall be entitled to seek
equitable relief, including injunction, in addition to all other remedies available at law.

8. GOVERNING LAW
This Agreement shall be governed by the laws of the State of California, without regard to
its conflict of laws principles.

9. ENTIRE AGREEMENT
This Agreement constitutes the entire agreement between the Parties concerning the subject
matter hereof and supersedes all prior agreements and understandings.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the Effective Date.

TechCorp Solutions Inc.                    DataFlow Analytics LLC
By: _________________________              By: _________________________
Name: Sarah Chen                           Name: Michael Rodriguez
Title: VP of Business Development          Title: Chief Technology Officer
Date: January 15, 2025                     Date: January 15, 2025
""",
    "saas_agreement.txt": """SOFTWARE AS A SERVICE (SaaS) AGREEMENT

This Software as a Service Agreement ("Agreement") is entered into as of March 1, 2025
("Effective Date"), by and between:

Provider: CloudPlatform Technologies Inc., a Delaware corporation ("Provider")
Address: 2500 Tech Park Way, Austin, TX 78701

Customer: GlobalRetail Enterprises Corp., a New York corporation ("Customer")
Address: 888 Fifth Avenue, New York, NY 10019

1. DEFINITIONS
1.1 "Service" means the cloud-based enterprise resource planning platform provided by
    Provider, including all updates and upgrades made generally available.
1.2 "Subscription Term" means the initial term of twelve (12) months from the Effective Date,
    automatically renewing for successive twelve (12) month periods unless terminated.
1.3 "Users" means individuals authorized by Customer to access the Service.
1.4 "Customer Data" means all data submitted to the Service by or on behalf of Customer.

2. SERVICE AND LICENSE
2.1 Provider grants Customer a non-exclusive, non-transferable right to access and use the
    Service during the Subscription Term for Customer's internal business operations.
2.2 Provider shall make the Service available 99.9% of the time measured monthly, excluding
    scheduled maintenance windows communicated at least 48 hours in advance.

3. FEES AND PAYMENT
3.1 Customer shall pay Provider the fees set forth in the Order Form attached as Exhibit A.
3.2 Annual subscription fee: $240,000 USD ($20,000/month) for up to 500 Users.
3.3 Additional Users: $40 per User per month.
3.4 Payment Terms: Net 30 from date of invoice.
3.5 Late payments shall accrue interest at 1.5% per month or the maximum rate permitted by law.
3.6 Provider may suspend access to the Service if payment is more than 30 days overdue after
    written notice.

4. DATA PROTECTION AND SECURITY
4.1 Provider shall implement and maintain appropriate technical and organizational security
    measures to protect Customer Data, including:
    (a) Encryption of data at rest (AES-256) and in transit (TLS 1.2+);
    (b) Multi-factor authentication;
    (c) Regular penetration testing and vulnerability assessments;
    (d) SOC 2 Type II compliance maintained annually.
4.2 Provider processes Customer Data as a data processor on behalf of Customer as controller,
    pursuant to the Data Processing Agreement attached as Exhibit B.
4.3 Provider shall notify Customer of any security breach affecting Customer Data within
    48 hours of becoming aware of such breach.
4.4 Upon termination, Provider shall return Customer Data in a standard format within 30 days
    and delete all copies within 90 days, unless retention is required by law.

5. SERVICE LEVEL AGREEMENT
5.1 Uptime Guarantee: 99.9% monthly availability.
5.2 Measurement: Availability = (Total Minutes - Downtime Minutes) / Total Minutes × 100.
5.3 Exclusions: Scheduled maintenance, force majeure events, Customer's internet connectivity.
5.4 Service Credits:
    - 99.0% to 99.9%: 5% credit of monthly fee
    - 95.0% to 99.0%: 10% credit of monthly fee
    - Below 95.0%: 25% credit of monthly fee
5.5 Service credits are Customer's sole remedy for failure to meet uptime guarantees.
5.6 Support Response Times:
    - Critical (service down): 1 hour response, 4 hour resolution target
    - High (major feature impacted): 4 hour response, 1 business day resolution target
    - Medium (minor feature impacted): 8 hour response, 3 business day resolution target
    - Low (general inquiry): 1 business day response

6. INTELLECTUAL PROPERTY
6.1 Provider retains all rights in the Service, including all improvements and modifications.
6.2 Customer retains all rights in Customer Data.
6.3 Customer grants Provider a limited license to use Customer Data solely to provide the Service.
6.4 Any feedback or suggestions provided by Customer may be freely used by Provider without
    obligation or restriction.

7. INDEMNIFICATION
7.1 Provider Indemnification: Provider shall indemnify Customer against third-party claims
    that the Service infringes any valid patent or copyright, provided Customer:
    (a) promptly notifies Provider of the claim;
    (b) grants Provider sole control of the defense and settlement;
    (c) provides reasonable cooperation at Provider's expense.
7.2 Customer Indemnification: Customer shall indemnify Provider against claims arising from
    Customer's use of the Service in violation of this Agreement or applicable law.

8. LIMITATION OF LIABILITY
8.1 NEITHER PARTY SHALL BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL,
    OR PUNITIVE DAMAGES ARISING FROM THIS AGREEMENT.
8.2 EACH PARTY'S TOTAL AGGREGATE LIABILITY SHALL NOT EXCEED THE FEES PAID OR PAYABLE BY
    CUSTOMER IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM.
8.3 The foregoing limitations shall not apply to: (a) breaches of confidentiality;
    (b) indemnification obligations; (c) willful misconduct or gross negligence.

9. TERMINATION
9.1 Either Party may terminate this Agreement for convenience upon ninety (90) days prior
    written notice, effective at the end of the then-current Subscription Term.
9.2 Either Party may terminate for cause if the other Party materially breaches and fails
    to cure within thirty (30) days of written notice specifying the breach.
9.3 Either Party may terminate immediately if the other Party becomes insolvent, files for
    bankruptcy, or ceases operations.
9.4 Upon termination: (a) all licenses granted hereunder terminate; (b) Customer shall pay
    all fees accrued through the termination date; (c) data return per Section 4.4.

10. CONFIDENTIALITY
Both Parties shall maintain the confidentiality of the other Party's proprietary information
for the duration of this Agreement and for three (3) years thereafter.

11. FORCE MAJEURE
Neither Party shall be liable for delays or failures due to causes beyond its reasonable
control, including natural disasters, war, terrorism, pandemics, or government actions,
provided the affected Party gives prompt notice and uses reasonable efforts to mitigate.
If the force majeure event continues for more than 120 days, either Party may terminate.

12. GOVERNING LAW AND DISPUTE RESOLUTION
12.1 This Agreement shall be governed by the laws of the State of Delaware.
12.2 Any dispute shall be resolved through binding arbitration administered by the American
     Arbitration Association under its Commercial Arbitration Rules.

13. GENERAL PROVISIONS
13.1 This Agreement constitutes the entire agreement between the Parties.
13.2 Amendments must be in writing signed by both Parties.
13.3 Neither Party may assign this Agreement without prior written consent, except in
     connection with a merger, acquisition, or sale of all or substantially all assets.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the Effective Date.

CloudPlatform Technologies Inc.            GlobalRetail Enterprises Corp.
By: _________________________              By: _________________________
Name: David Park                           Name: Jennifer Walsh
Title: Chief Executive Officer             Title: Chief Information Officer
Date: March 1, 2025                        Date: March 1, 2025
""",
    "employment_contract.txt": """EMPLOYMENT AGREEMENT

This Employment Agreement ("Agreement") is entered into as of February 1, 2025
("Effective Date"), by and between:

Employer: InnovateTech Labs Inc., a California corporation ("Company")
Address: 300 Artificial Intelligence Blvd, Palo Alto, CA 94301

Employee: Alexandra Kim ("Employee")
Address: 1455 Elm Street, Mountain View, CA 94040

1. POSITION AND DUTIES
1.1 The Company hereby employs Employee as Senior Machine Learning Engineer, reporting
    to the VP of Engineering.
1.2 Employee shall devote full-time professional efforts to the Company and perform duties
    as reasonably assigned.
1.3 Employee's primary work location shall be the Company's Palo Alto office, with the
    option to work remotely up to three (3) days per week.

2. TERM
2.1 This Agreement is for at-will employment. Either party may terminate the employment
    relationship at any time, with or without cause, subject to the provisions herein.
2.2 The first ninety (90) days shall constitute a probationary period.

3. COMPENSATION
3.1 Base Salary: $195,000 per year, payable semi-monthly.
3.2 Annual Bonus: Target bonus of 15% of base salary, based on individual and company
    performance, payable within 60 days of fiscal year end.
3.3 Equity: Employee shall receive a stock option grant of 50,000 shares, vesting over
    four (4) years with a one-year cliff (25% vests after 12 months, remainder monthly).
3.4 Benefits: Employee is eligible for the Company's standard benefits package including
    health insurance, dental, vision, 401(k) with 4% match, and unlimited PTO.

4. INTELLECTUAL PROPERTY ASSIGNMENT
4.1 Employee agrees that all inventions, discoveries, designs, code, documentation, and
    other work product created during employment and related to the Company's business
    or created using Company resources ("Work Product") are the sole property of the Company.
4.2 Employee hereby assigns to the Company all rights, title, and interest in Work Product.
4.3 Employee shall promptly disclose all Work Product to the Company and execute any
    documents necessary to perfect the Company's ownership.
4.4 This assignment does not apply to inventions developed entirely on Employee's own time
    without Company resources, unrelated to Company's business, as protected under
    California Labor Code Section 2870.

5. CONFIDENTIALITY
5.1 Employee shall not disclose or use any Confidential Information except as required
    to perform duties under this Agreement.
5.2 "Confidential Information" includes trade secrets, algorithms, models, datasets,
    customer information, business strategies, and any non-public business information.
5.3 Confidentiality obligations survive termination of employment indefinitely for trade
    secrets and for three (3) years for other Confidential Information.

6. NON-SOLICITATION
6.1 During employment and for twelve (12) months following termination, Employee shall not:
    (a) Solicit or hire any Company employee or contractor;
    (b) Solicit any Company customer or prospective customer with whom Employee had
        material contact during the last twelve months of employment.

7. NON-COMPETE
7.1 [Note: This section is generally unenforceable in California per Business and
    Professions Code Section 16600. Included for reference in other jurisdictions.]
7.2 During employment and for twelve (12) months following termination, Employee shall
    not engage in any business that directly competes with the Company within the
    United States.

8. TERMINATION
8.1 By Company Without Cause: Company may terminate Employee's employment at any time
    upon two (2) weeks' written notice. Upon such termination, Employee shall receive:
    (a) Accrued salary and unused PTO through the termination date;
    (b) Severance of three (3) months' base salary, subject to execution of a release;
    (c) COBRA premium reimbursement for three (3) months.
8.2 By Company For Cause: Company may terminate immediately for cause, including:
    (a) Material breach of this Agreement;
    (b) Conviction of a felony;
    (c) Willful misconduct or gross negligence;
    (d) Continued failure to perform duties after written warning.
    No severance shall be payable upon termination for cause.
8.3 By Employee: Employee may resign at any time upon two (2) weeks' written notice.
8.4 Upon termination, Employee shall return all Company property, including equipment,
    documents, and access credentials within five (5) business days.

9. DISPUTE RESOLUTION
9.1 Any dispute arising from this Agreement shall be resolved through binding arbitration
    in Santa Clara County, California, under JAMS Employment Arbitration Rules.
9.2 Each Party shall bear its own attorneys' fees unless the arbitrator determines otherwise.

10. GOVERNING LAW
This Agreement shall be governed by the laws of the State of California.

11. ENTIRE AGREEMENT
This Agreement, together with any exhibits, constitutes the entire agreement between the
Parties and supersedes all prior negotiations and agreements.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the Effective Date.

InnovateTech Labs Inc.                     Employee
By: _________________________              _________________________
Name: Robert Nakamura                      Alexandra Kim
Title: Chief Executive Officer
Date: February 1, 2025                     Date: February 1, 2025
""",
    "vendor_agreement.txt": """VENDOR SERVICES AGREEMENT

This Vendor Services Agreement ("Agreement") is entered into as of April 1, 2025
("Effective Date"), by and between:

Client: MegaCorp International Inc., a New York corporation ("Client")
Address: 600 Madison Avenue, New York, NY 10022

Vendor: SmartOps Consulting Group LLC, a Texas limited liability company ("Vendor")
Address: 1800 Commerce Street, Suite 400, Dallas, TX 75201

RECITALS
WHEREAS, Client desires to engage Vendor to provide certain data engineering and analytics
consulting services; and
WHEREAS, Vendor has the expertise and capacity to perform such services;
NOW, THEREFORE, the Parties agree as follows:

1. SCOPE OF SERVICES
1.1 Vendor shall provide the data engineering and analytics consulting services described
    in each Statement of Work ("SOW") executed by both Parties.
1.2 Initial SOW: Data pipeline modernization and dashboard development, as detailed in
    Exhibit A attached hereto.
1.3 Vendor shall assign qualified personnel with relevant expertise and experience.
1.4 Client may request changes to the scope via a written Change Order, subject to
    mutual agreement on adjusted fees and timelines.

2. TERM
2.1 Initial Term: This Agreement shall commence on the Effective Date and continue for
    twenty-four (24) months.
2.2 Renewal: The Agreement shall automatically renew for successive twelve (12) month
    periods unless either Party provides sixty (60) days written notice of non-renewal.

3. FEES AND PAYMENT
3.1 Vendor shall be compensated as specified in each SOW.
3.2 Initial SOW Fees:
    - Senior Consultant: $250/hour
    - Consultant: $175/hour
    - Analyst: $125/hour
    - Estimated total: $480,000 for Phase 1 (6 months)
3.3 Expenses: Client shall reimburse Vendor for pre-approved travel and expenses per
    the Client's travel policy, not to exceed $5,000 per month.
3.4 Invoicing: Vendor shall submit monthly invoices with detailed time records.
3.5 Payment Terms: Net 45 from receipt of invoice.
3.6 Disputed Invoices: Client shall notify Vendor within 15 days of receipt. Undisputed
    portions must be paid per standard terms.

4. PERSONNEL AND PERFORMANCE
4.1 Vendor's Key Personnel: Lead Consultant — Maria Santos; Technical Architect — James Liu.
4.2 Vendor shall not replace Key Personnel without Client's prior written consent.
4.3 Client may request removal of Vendor personnel who fail to meet reasonable performance
    standards, and Vendor shall provide a suitable replacement within 10 business days.

5. INTELLECTUAL PROPERTY
5.1 Pre-existing IP: Each Party retains ownership of its pre-existing intellectual property.
5.2 Work Product: All deliverables, code, documentation, and materials created by Vendor
    specifically for Client under this Agreement ("Work Product") shall be owned by Client
    upon full payment.
5.3 Vendor Tools: Vendor retains ownership of proprietary tools, methodologies, and
    frameworks ("Vendor Tools") used in performing services. Vendor grants Client a
    perpetual, non-exclusive license to use Vendor Tools embedded in Work Product.
5.4 Open Source: Vendor shall not incorporate open-source software into Work Product without
    Client's prior written approval and shall disclose all open-source components and
    their licenses.

6. CONFIDENTIALITY
6.1 Each Party shall protect the other's Confidential Information with reasonable care.
6.2 Confidentiality obligations survive for five (5) years after disclosure.
6.3 Vendor acknowledges that access to Client's systems and data is subject to Client's
    information security policies.

7. DATA PROTECTION
7.1 To the extent Vendor processes personal data on Client's behalf, the Parties shall
    execute a Data Processing Agreement in accordance with applicable data protection laws.
7.2 Vendor shall comply with GDPR, CCPA, and all applicable data privacy regulations.
7.3 Vendor shall not transfer personal data outside the United States or European Economic
    Area without Client's prior written consent and adequate safeguards.

8. REPRESENTATIONS AND WARRANTIES
8.1 Vendor represents and warrants that:
    (a) Services shall be performed in a professional and workmanlike manner;
    (b) Vendor has the right and authority to enter into this Agreement;
    (c) Work Product shall not infringe any third-party intellectual property rights;
    (d) Vendor shall comply with all applicable laws and regulations.
8.2 Vendor warrants deliverables for sixty (60) days following acceptance by Client.

9. INDEMNIFICATION
9.1 Vendor shall indemnify and hold harmless Client from any third-party claims arising from:
    (a) Vendor's negligence or willful misconduct;
    (b) Infringement of intellectual property rights by Work Product;
    (c) Vendor's violation of applicable laws.
9.2 Client shall indemnify Vendor from claims arising from Client's use of Work Product
    in a manner not contemplated by this Agreement.

10. LIMITATION OF LIABILITY
10.1 VENDOR'S TOTAL LIABILITY SHALL NOT EXCEED THE FEES PAID BY CLIENT IN THE TWELVE (12)
     MONTHS PRECEDING THE CLAIM.
10.2 NEITHER PARTY SHALL BE LIABLE FOR INDIRECT, CONSEQUENTIAL, OR PUNITIVE DAMAGES.
10.3 THE FOREGOING LIMITATIONS DO NOT APPLY TO: (A) INDEMNIFICATION OBLIGATIONS;
     (B) BREACHES OF CONFIDENTIALITY; (C) INTELLECTUAL PROPERTY INFRINGEMENT;
     (D) GROSS NEGLIGENCE OR WILLFUL MISCONDUCT.

11. TERMINATION
11.1 For Convenience: Either Party may terminate upon sixty (60) days written notice.
     Client shall pay for services rendered through the termination date.
11.2 For Cause: Either Party may terminate if the other Party materially breaches and
     fails to cure within thirty (30) days of written notice.
11.3 Immediate Termination: Either Party may terminate immediately upon the other Party's
     insolvency, bankruptcy filing, or assignment for the benefit of creditors.
11.4 Transition: Upon termination, Vendor shall provide reasonable transition assistance
     for a period not to exceed thirty (30) days at standard hourly rates.

12. INSURANCE
Vendor shall maintain the following insurance during the term:
(a) Commercial General Liability: $2,000,000 per occurrence
(b) Professional Liability (E&O): $5,000,000 per claim
(c) Cyber Liability: $3,000,000 per claim
(d) Workers' Compensation: As required by applicable law

13. INDEPENDENT CONTRACTOR
Vendor is an independent contractor. Nothing in this Agreement creates an employment,
partnership, or joint venture relationship. Vendor is responsible for its own taxes,
benefits, and employment obligations.

14. GOVERNING LAW
This Agreement shall be governed by the laws of the State of New York.

15. DISPUTE RESOLUTION
Any dispute shall first be subject to good-faith negotiation for thirty (30) days,
followed by mediation, and if unresolved, binding arbitration under AAA Commercial Rules
in New York, NY.

16. GENERAL PROVISIONS
16.1 Entire Agreement: This Agreement and all SOWs constitute the entire agreement.
16.2 Amendments: Must be in writing signed by authorized representatives of both Parties.
16.3 Assignment: Neither Party may assign without written consent, except in connection
     with a merger or acquisition.
16.4 Notices: All notices shall be in writing, sent to the addresses above.
16.5 Waiver: Failure to enforce any provision is not a waiver of future enforcement rights.
16.6 Severability: If any provision is unenforceable, the remaining provisions continue.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the Effective Date.

MegaCorp International Inc.                SmartOps Consulting Group LLC
By: _________________________              By: _________________________
Name: Patricia Gonzalez                    Name: Thomas Anderson
Title: Chief Procurement Officer           Title: Managing Partner
Date: April 1, 2025                        Date: April 1, 2025
""",
}


def generate_sample_contracts():
    """Write all sample contracts to the data/contracts/ directory."""
    contracts_path = Path(CONTRACTS_DIR)
    contracts_path.mkdir(parents=True, exist_ok=True)

    for filename, content in SAMPLE_CONTRACTS.items():
        filepath = contracts_path / filename
        filepath.write_text(content.strip())
        print(f"Generated: {filepath}")

    print(f"\n{len(SAMPLE_CONTRACTS)} sample contracts written to {contracts_path}")


if __name__ == "__main__":
    generate_sample_contracts()
