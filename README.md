# DU RA Stable Matching Algorithm

This project implements a modified Gale–Shapley algorithm to perform stable matching between Resident Assistants (RAs) and Residence Halls at the University of Denver. The algorithm is **Residence Hall-optimal**, meaning Residence Halls act as the proposers and the resulting matches favor their preferences.

## Project Overview

The goal is to assign ~80 RAs to 6 Residence Halls using ranked preference lists from both applicants and Residence Directors (RDs).

### Residence Hall Details

- **6 Total Halls**
  - 3 First-Year
  - 3 Upper-Classman
- Some halls include:
  - Living-Learning Communities (LLCs)
  - Gender-specific RA requirements

These factors introduce additional complexity to the matching process.

## Tech Stack

### Backend
- **Python**
- **FastAPI**
- **MongoDB** (for data storage)

### Frontend
- **React** with **TypeScript**
- **Tailwind CSS** (for styling)
- **Axios** (for API calls)
- **Vite** (build tool)

## Getting Started

### Prerequisites
- Node.js + npm
- Python 3.8+
- A Python virtual environment tool (e.g., `venv`, `virtualenv`)

### Running the App Locally

#### 1. Clone the repository:

```bash
git clone https://github.com/DU-Stable-Matching/stable-matching.git
```


#### 2. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# install Python dependencies
pip install -r requirements.txt

# Create a virtual environment
python -m venv venv

# Activate your Python virtual environment
source venv/bin/activate  

# Run the backend server
fastapi run api/main.py
```

#### 3. Frontend Setup

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
```
