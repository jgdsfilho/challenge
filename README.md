## Project Setup

This project requires the following tools to run correctly:

- **Python 3.12 or higher**
- **Docker**
- **Docker Compose**
- **Poetry**

## Prerequisites

### 1. Install Python 3.12 or Higher

This project requires Python 3.12 or higher. To facilitate the installation and management of Python versions, we recommend using `pyenv`.

#### How to Install Python 3.12 with `pyenv`:

1. **Install `pyenv`**:
   - Follow the installation instructions for `pyenv` in the [official link](https://github.com/pyenv/pyenv#installation).

2. **Install Python 3.12**:
   After installing `pyenv`, you can install Python 3.12 with the following command:
   ```bash
   pyenv install 3.12.0

3. **Set Python 3.12 as the Default Version**:
To set version 3.12 as the default, run the following command inside the project repository:
   ```bash
   pyenv local 3.12.0
   ```

### 2.  Install Docker and Docker Compose

1. **Install  `docker`**:
   - Follow the installation instructions for docker in the [official link](https://docs.docker.com/get-docker/).

2. **Install  `docker-compose`**:
    - Follow the installation instructions for `docker-compose` in th[official link](https://docs.docker.com/compose/install/).
  
### 3. Install Poetry

Poetry will be required locally to run commands like migrations without needing to run `docker-compose`, or even to run the project outside of Docker to facilitate debugging.

1. **Install `poetry`**:
   - Follow the installation instructions for `poetry` in the [official link](https://python-poetry.org/docs/#installation).


