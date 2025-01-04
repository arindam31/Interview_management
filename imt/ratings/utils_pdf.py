"""Pdf reading and info processing related function."""

import re
import pdfplumber
from pathlib import Path
import spacy
from pprint import pprint

nlp = spacy.load("en_core_web_sm")
# Regex for contact details
EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
PHONE_REGEX = r"\+?[0-9\s\-\(\)]+"


def read_resume_pdf(file_path):
    """read resume only in PDF format."""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    text = " ".join(text.split())
    return text


def analyze_resume(text):
    # Initialize fields
    extracted_data = {
        "Name": None,
        "Email": None,
        "Phone": None,
        "LinkedIn": None,
        "Experience": [],
        "Skills": [],
        "Education": [],
    }
    doc = nlp(text)

    # tokenization..breaks text into words or sentense.
    tokens = [token.text for token in doc]

    # Names Entity Recognition (NER)
    # Identifying entities like names, skills, or locations in text
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not extracted_data["Name"]:
            print(repr(ent.text))
            print("********")
            extracted_data["Name"] = ent.text.strip()

    # Extract LinkedIn URL
    if "linkedin.com" in text.lower():
        start_idx = text.lower().find("linkedin.com")
        extracted_data["LinkedIn"] = text[start_idx:].split()[0]

    # Extract Email
    email = re.search(EMAIL_REGEX, text)
    extracted_data["Email"] = email.group(0) if email else None

    # Extract Phone
    phone = re.search(PHONE_REGEX, text)
    extracted_data["Phone"] = phone.group(0).strip() if phone else None

    # Extract Experience (Job Titles, Companies)
    for sent in doc.sents:
        if "worked" in sent.text.lower() or "experience" in sent.text.lower():
            extracted_data["Experience"].append(sent.text.strip())

    # Extract Skills (use a predefined skill list for matching)
    skill_list = [
        "Python",
        "Django",
        "React",
        "Machine Learning",
        "SQL",
        "Java",
        "Testing",
        "QA",
    ]
    for token in doc:
        if token.text in skill_list:
            extracted_data["Skills"].append(token.text)

    # Deduplicate Skills
    extracted_data["Skills"] = list(set(extracted_data["Skills"]))

    # # Identify nouns or verbs
    # pos_tags = [(token.text, token.pos_) for token in doc]
    # print("POS Tags:", pos_tags)

    # Extract Education
    for sent in doc.sents:
        if any(
            keyword in sent.text.lower()
            for keyword in [
                "b.sc.",
                "m.sc.",
                "ph.d.",
                "degree",
                "university",
                "college",
                "b.tech",
                "Btech",
            ]
        ):
            extracted_data["Education"].append(sent.text.strip())

    return extracted_data


if __name__ == "__main__":
    filepath = (
        Path(__file__).resolve().parent.parent / "static" / "files" / "Profile.pdf"
    )
    text = read_resume_pdf(filepath)

    resume_text = """
    John Doe
    Python Developer with 5 years of experience. He worked at Google.
    Contact: john.doe@gmail.com, +1234567890
    LinkedIn: linkedin.com/in/johndoe
    Skills: Python, Django, React, SQL
    Education: B.Sc. in Computer Science from MIT, 2015.
    """
    result = analyze_resume(text)
    pprint(result)
