# LLM-FAQ-Expert

LLM-FAQ-Expert is a project demonstrating the integration of Large Language Models (LLMs) for question-answering tasks in educational settings. It is designed to assist students enrolled in DataTalksClub's free courses by providing a system to search for answers within FAQ documents. We utilize the FAQ documents provided by DataTalksClub, making the system directly applicable to the courses offered by the platform.


## Project Components

### 1. `course_assistant_LLM.ipynb`

**Description:**
This Jupyter Notebook implements a question-answering system using OpenAI's GPT-3.5 model and Elasticsearch. It allows students to retrieve relevant information from FAQ documents of DataTalksClub's courses.

### 2. `extract_faq_to_json.ipynb`

**Description:**
This Jupyter Notebook reads the FAQ documents of DataTalksClub's courses and converts them into JSON format. It serves as a preprocessing step to organize the FAQ data for later use in the question-answering system.

### 3. `Dockerfile`

**Description:**
The Dockerfile defines the specifications for building a Docker image of Elasticsearch. It sets up Elasticsearch with the necessary configurations to host the FAQ documents and enable efficient search functionalities.

### 4. `docker-compose.yml`

**Description:**
The docker-compose file orchestrates the deployment of Elasticsearch using Docker containers. It specifies the Elasticsearch service and any required configurations, enabling easy setup and management of Elasticsearch within a Dockerized environment.

## Usage

1. Ensure Docker and Docker Compose are installed on your system.
2. Clone the repository and navigate to the project directory.
3. Run the following command to start Elasticsearch using Docker Compose:

```bash
docker-compose up -d
```

4. Execute the Jupyter Notebooks `extract_faq_to_json.ipynb` and `course_assistant_LLM.ipynb` to perform FAQ data extraction and question-answering tasks, respectively. Alternatively, Python scripts `extract_faq_to_json.py` and `course_assistant_LLM.py` are available as alternatives.


## Requirements

- Python 3.x
- Jupyter Notebook
- `elasticsearch` Python library
- `openai` Python library
- `tqdm` Python library

## License

This project is licensed under the Apache License. See the [LICENSE](./LICENSE) file for details.
