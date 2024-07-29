### Book Summarizer
#### Overview
Book Summarizer is a web application that allows users to search for the summary of preceding books.

Features
Search for books by title.
View detailed summaries of selected books.
Modern, responsive design built with React.
Getting Started
You can quickly set up and deploy the project using the provided CI/CD pipeline and Docker configurations.

Prerequisites
Docker: Install Docker
Docker Compose: Install Docker Compose
Running Locally with Docker
Clone the Repository

```
git clone https://github.com/your-username/AIPI561Book.git
cd AIPI561Book
Build and Run with Docker Compose
```

bash
Copy code
docker-compose up --build
This command will build the Docker images and start the containers for both the frontend and backend (if applicable). The application will be accessible at http://localhost:3000.


#### File Structure
/AIPI561Book
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── summary/
│   │   ├── __init__.py
│   │   ├── bart_summarizer.py
│   │   ├── openai_summarizer.py
│   └── tests/
│       ├── __init__.py
│       ├── test_summary.py
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── App.js
│   │   │   ├── Header.js
│   │   │   ├── Search.js
│   │   ├── pages/
│   │   │   ├── HomePage.js
│   │   ├── App.test.js
│   ├── package.json
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── .github/
│   └── workflows/
│       └── ci_cd.yml
└── README.md

#### Major Folders and Files
1. backend/
The backend folder contains the server-side code for your application, primarily built with Flask and responsible for interacting with APIs and handling business logic.

app.py: The main entry point for the Flask application. It initializes and configures the Flask app, sets up routes, and handles incoming requests.

requirements.txt: Lists the Python packages required to run the backend. This includes Flask, any libraries for connecting to the LLMs, and other dependencies.

summary/: Contains modules for summarization tasks.

__init__.py: Initializes the summary package.
bart_summarizer.py: Contains functions or classes to perform summarization using the BART model.
openai_summarizer.py: Contains functions or classes to perform summarization using OpenAI's LLM.
tests/: Contains test files for the backend.

__init__.py: Initializes the tests package.
test_summary.py: Contains unit tests for the summarization functions in the summary module.
2. frontend/
The frontend folder contains the client-side code, typically built with React, and responsible for the user interface of the application.

public/: Contains static assets and the main HTML file (index.html) for the React application.

src/: Contains the source code for the React application.

components/: Contains reusable React components.
App.js: The root component of your React app.
Header.js: Component for the application header.
Search.js: Component for the search functionality.
pages/: Contains page components.
HomePage.js: Component for the home page.
App.test.js: Contains tests for the App.js component.
package.json: Manages the dependencies, scripts, and metadata for the React project. It lists packages such as react, react-dom, and react-scripts.

Dockerfile: Contains instructions for building a Docker image for the frontend application. It typically includes steps for installing dependencies and setting up the environment.

docker-compose.yml: Defines and runs multi-container Docker applications. It specifies services, networks, and volumes for both frontend and backend, if needed.

3. .github/
The .github folder contains GitHub-specific configurations, including workflows for CI/CD.

workflows/ci_cd.yml: Defines the CI/CD pipeline for the project. It automates processes such as checking out code, setting up environments, installing dependencies, running tests, and building the application.
4. README.md
The README.md file provides an overview of the project, including setup instructions, usage guidelines, and contribution information.
