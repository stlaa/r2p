import re
from typing import Dict

import PyPDF2
import docx

class ResumeParser:
    """
    Parse resume from PDF or DOCX files.
    Extracts content while filtering out personal data like phone numbers and addresses.
    """

    # Regex patterns for personal data to filter
    PHONE_PATTERN = re.compile(
        r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    )
    # Address pattern - lines with street numbers, apartment numbers, zip codes
    ADDRESS_PATTERN = re.compile(
        r'\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|'
        r'Lane|Ln|Boulevard|Blvd|Way|Court|Ct|Circle|Cir|Place|Pl)\b',
        re.IGNORECASE
    )
    ZIP_PATTERN = re.compile(r'\b\d{5}(-\d{4})?\b')

    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """Extract text content from PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")

    @staticmethod
    def parse_docx(file_path: str) -> str:
        """Extract text content from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {str(e)}")

    @staticmethod
    def parse_doc(file_path: str) -> str:
        """
        Extract text content from DOC file
        Note: DOC format is legacy, conversion may require additional libraries
        For now, we'll raise an informative error
        """
        raise NotImplementedError(
            "Legacy .doc format is not fully supported. "
            "Please convert to .docx or .pdf format."
        )

    @staticmethod
    def filter_personal_data(text: str) -> str:
        """
        Remove personal information like phone numbers and addresses from text
        """
        # Remove phone numbers
        text = ResumeParser.PHONE_PATTERN.sub('[PHONE NUMBER REMOVED]', text)

        # Remove addresses
        text = ResumeParser.ADDRESS_PATTERN.sub('[ADDRESS REMOVED]', text)

        # Remove ZIP codes
        text = ResumeParser.ZIP_PATTERN.sub('[ZIP REMOVED]', text)

        return text

    @staticmethod
    def extract_sections(text: str) -> Dict[str, str]:
        """
        Extract common resume sections for structured data
        """
        sections = {}

        # Common section headers
        section_patterns = {
            'summary': r'(?i)(professional\s+summary|summary|profile|objective)',
            'experience': r'(?i)(work\s+experience|professional\s+experience|experience|employment)',
            'education': r'(?i)(education|academic\s+background)',
            'skills': r'(?i)(skills|technical\s+skills|core\s+competencies)',
            'projects': r'(?i)(projects|portfolio)',
            'certifications': r'(?i)(certifications|certificates|licenses)',
            'achievements': r'(?i)(achievements|awards|accomplishments)'
        }

        # Simple section extraction
        for section_name, pattern in section_patterns.items():
            match = re.search(pattern, text)
            if match:
                sections[section_name] = True

        return sections

    @classmethod
    def parse(cls, file_path: str) -> Dict[str, any]:
        """
        Main parsing method that handles different file formats
        Returns a dictionary with parsed content and metadata
        """
        file_extension = file_path.rsplit('.', 1)[1].lower()

        # Parse based on file type
        if file_extension == 'pdf':
            raw_text = cls.parse_pdf(file_path)
        elif file_extension == 'docx':
            raw_text = cls.parse_docx(file_path)
        elif file_extension == 'doc':
            raw_text = cls.parse_doc(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

        # Filter personal data
        filtered_text = cls.filter_personal_data(raw_text)

        # Extract sections
        sections = cls.extract_sections(filtered_text)

        return {
            'raw_text': raw_text,
            'filtered_text': filtered_text,
            'sections': sections,
            'has_content': bool(filtered_text.strip())
        }
