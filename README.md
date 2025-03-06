# AI-Based Legal Document Analyzer

This project analyzes legal contracts for risks, loopholes, and compliance issues using a fine-tuned LegalBERT model on the CUAD dataset. It includes a full CI/CD pipeline with GitHub Actions, Jenkins, and Docker.

## Repository Structure

- **app/**: Contains the Flask API and its dependencies.
- **data/**: Instructions for downloading and using the CUAD dataset.
- **model/**: Scripts for fine-tuning LegalBERT on the CUAD dataset.
- **tests/**: Unit tests for the Flask API.
- **.github/workflows/**: GitHub Actions for linting and testing.
- **Dockerfile**: Docker configuration to containerize the Flask app.
- **Jenkinsfile**: Jenkins pipeline definition for CI/CD.

## Setup Instructions

### Local Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/legal-doc-analyzer.git
   cd legal-doc-analyzer
