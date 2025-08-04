# USQuantAgent

This project is a stock analysis application with a React frontend and a Python Flask backend.

## Getting Started

### Prerequisites

- Python 3.x
- Node.js and npm

### Installation and Running

1.  **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd USQuantAgent
    ```

2.  **Backend Setup (Recommended: Use a Virtual Environment):**
    - Create and activate a virtual environment from the root directory:
      ```sh
      python3 -m venv venv
      source venv/bin/activate  # On Windows use `venv\Scripts\activate`
      ```
    - Install Python dependencies into the virtual environment:
      ```sh
      pip3 install -r backend/requirements.txt
      ```
    - Run the backend server:
      ```sh
      python3 backend/app.py
      ```
    The backend will be running at `http://127.0.0.1:5000`.

3.  **Frontend Setup:**
    - Install Node.js dependencies from the root directory:
      ```sh
      npm install --prefix frontend
      ```
    - Run the frontend development server from the root directory:
      ```sh
      npm start --prefix frontend
      ```
    The frontend will be running at `http://localhost:3000`.
