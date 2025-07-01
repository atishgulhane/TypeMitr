# Comprehensive document types based on uploaded files
DOCUMENT_TYPES = {
    # Academic & Educational Applications
    "University/College Admission Application": {
        "category": "Academic & Educational",
        "description": "Application for admission to university or college programs",
        "fields": ["program_name", "academic_year", "previous_qualifications"]
    },
    "Scholarship Application": {
        "category": "Academic & Educational", 
        "description": "Application for financial aid and scholarships",
        "fields": ["scholarship_name", "financial_need", "academic_achievements"]
    },
    "Bonafide Certificate Application": {
        "category": "Academic & Educational",
        "description": "Request for student bonafide certificate",
        "fields": ["student_id", "academic_year", "purpose_of_certificate"]
    },
    "Migration Certificate Application": {
        "category": "Academic & Educational",
        "description": "Application for migration certificate for transferring institutions",
        "fields": ["current_institution", "new_institution", "course_details"]
    },
    "Character Certificate Application": {
        "category": "Academic & Educational",
        "description": "Request for character certificate from educational institution",
        "fields": ["institution_name", "academic_period", "purpose"]
    },
    "Leave Application": {
        "category": "Academic & Educational",
        "description": "Application for leave from school, college or work",
        "fields": ["leave_type", "leave_duration", "reason_for_leave"]
    },
    
    # Corporate & Business Applications
    "Job Application": {
        "category": "Corporate & Business",
        "description": "Application for employment position",
        "fields": ["position_title", "company_name", "qualifications", "experience"]
    },
    "Business Proposal": {
        "category": "Corporate & Business",
        "description": "Proposal for business partnership or venture",
        "fields": ["business_type", "proposal_details", "partnership_terms"]
    },
    "Vendor Registration Application": {
        "category": "Corporate & Business",
        "description": "Application to register as vendor or supplier",
        "fields": ["company_details", "services_offered", "registration_requirements"]
    },
    "Tender Application": {
        "category": "Corporate & Business",
        "description": "Application for participating in business tenders",
        "fields": ["tender_number", "project_details", "company_capabilities"]
    },
    "Franchise Application": {
        "category": "Corporate & Business",
        "description": "Application for franchise opportunity",
        "fields": ["franchise_brand", "location_details", "investment_capacity"]
    },
    
    # Government & Public Service Applications
    "RTI Application": {
        "category": "Government & Public Service",
        "description": "Right to Information application to government departments",
        "fields": ["department_name", "information_requested", "purpose_of_request"]
    },
    "Aadhaar Card Application": {
        "category": "Government & Public Service",
        "description": "Application for Aadhaar card enrollment or correction",
        "fields": ["application_type", "demographic_details", "documents_submitted"]
    },
    "PAN Card Application": {
        "category": "Government & Public Service",
        "description": "Application for PAN card or corrections",
        "fields": ["application_type", "personal_details", "supporting_documents"]
    },
    "Passport Application": {
        "category": "Government & Public Service",
        "description": "Application for passport issuance or renewal",
        "fields": ["passport_type", "travel_purpose", "supporting_documents"]
    },
    "Driving License Application": {
        "category": "Government & Public Service",
        "description": "Application for driving license (new, renewal, or duplicate)",
        "fields": ["license_type", "vehicle_category", "test_center_preference"]
    },
    "Voter ID Application": {
        "category": "Government & Public Service",
        "description": "Application for voter ID card registration or correction",
        "fields": ["constituency_details", "address_proof", "application_type"]
    },
    "Income Certificate Application": {
        "category": "Government & Public Service",
        "description": "Application for income certificate from revenue department",
        "fields": ["family_income", "purpose_of_certificate", "occupation_details"]
    },
    "Caste Certificate Application": {
        "category": "Government & Public Service",
        "description": "Application for caste certificate",
        "fields": ["caste_category", "family_details", "purpose_of_certificate"]
    },
    "Domicile Certificate Application": {
        "category": "Government & Public Service",
        "description": "Application for domicile/residence certificate",
        "fields": ["residence_duration", "address_details", "purpose_of_certificate"]
    },
    
    # Court & Judicial Applications
    "Bail Application": {
        "category": "Court & Judicial",
        "description": "Application for bail in criminal proceedings",
        "fields": ["case_number", "charges", "grounds_for_bail", "surety_details"]
    },
    "Petition": {
        "category": "Court & Judicial",
        "description": "General petition to court (writ, divorce, etc.)",
        "fields": ["petition_type", "relief_sought", "facts_of_case", "legal_grounds"]
    },
    "Application for Adjournment": {
        "category": "Court & Judicial",
        "description": "Request for postponement of court hearing",
        "fields": ["case_details", "reason_for_adjournment", "proposed_date"]
    },
    "Application for Stay": {
        "category": "Court & Judicial",
        "description": "Application for stay of proceedings or execution",
        "fields": ["case_details", "order_to_stay", "grounds_for_stay"]
    },
    "Caveat Application": {
        "category": "Court & Judicial",
        "description": "Application to be heard before any order is passed",
        "fields": ["case_nature", "interest_in_matter", "legal_basis"]
    },
    
    # General & Personal Applications
    "Complaint Letter": {
        "category": "General & Personal",
        "description": "Letter of complaint for services or products",
        "fields": ["complaint_against", "incident_details", "resolution_sought"]
    },
    "Request Letter": {
        "category": "General & Personal",
        "description": "General request letter for various purposes",
        "fields": ["request_details", "justification", "expected_outcome"]
    },
    "Resignation Letter": {
        "category": "General & Personal",
        "description": "Letter of resignation from job or position",
        "fields": ["current_position", "last_working_day", "reason_for_resignation"]
    },
    "Cover Letter": {
        "category": "General & Personal",
        "description": "Cover letter for job applications",
        "fields": ["position_applied", "relevant_experience", "key_qualifications"]
    },
    "Recommendation Letter": {
        "category": "General & Personal",
        "description": "Letter of recommendation for someone",
        "fields": ["person_being_recommended", "relationship", "qualities_achievements"]
    },
    "Invitation Letter": {
        "category": "General & Personal",
        "description": "Letter of invitation for events or visits",
        "fields": ["event_details", "invitee_details", "purpose_of_invitation"]
    },
    "Apology Letter": {
        "category": "General & Personal",
        "description": "Letter of apology for mistakes or misunderstandings",
        "fields": ["incident_details", "acknowledgment_of_fault", "corrective_measures"]
    },
    "Thank You Letter": {
        "category": "General & Personal",
        "description": "Letter expressing gratitude and appreciation",
        "fields": ["reason_for_thanks", "specific_actions_appreciated", "future_relationship"]
    }
}

# Categories for easier navigation
CATEGORIES = {
    "Academic & Educational": [
        "University/College Admission Application",
        "Scholarship Application", 
        "Bonafide Certificate Application",
        "Migration Certificate Application",
        "Character Certificate Application",
        "Leave Application"
    ],
    "Corporate & Business": [
        "Job Application",
        "Business Proposal",
        "Vendor Registration Application", 
        "Tender Application",
        "Franchise Application"
    ],
    "Government & Public Service": [
        "RTI Application",
        "Aadhaar Card Application",
        "PAN Card Application",
        "Passport Application",
        "Driving License Application",
        "Voter ID Application",
        "Income Certificate Application",
        "Caste Certificate Application", 
        "Domicile Certificate Application"
    ],
    "Court & Judicial": [
        "Bail Application",
        "Petition",
        "Application for Adjournment",
        "Application for Stay",
        "Caveat Application"
    ],
    "General & Personal": [
        "Complaint Letter",
        "Request Letter", 
        "Resignation Letter",
        "Cover Letter",
        "Recommendation Letter",
        "Invitation Letter",
        "Apology Letter",
        "Thank You Letter"
    ]
}
