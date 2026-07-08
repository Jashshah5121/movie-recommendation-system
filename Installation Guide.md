## 🚀 Quick Start (Plug & Play)

This application is completely containerized. You do not need to install Python, Node.js, or any ML libraries on your local machine.

## ⚙️ Set-up & Execution

### Prerequisites
* **Git** installed on your local machine.
* **Docker Desktop** installed and running.

### Steps

1. **Open Git Bash or Terminal** and navigate to the folder where you want to store the project:
```bash
   cd path/to/your/folder
   ```
   
2. **Clone the repository:**
```bash
  git clone https://github.com/Jashshah5121/movie-recommendation-system.git
  ```
  
3. **Navigate into the project directory:**
```bash
  cd movie-recommendation-system
```

4. **Verify Docker is running:**
Make sure Docker Desktop is open and wait until it shows "Engine running". You can verify it's available from your terminal by running:
```bash
docker --version
docker compose version
```
6. **Boot the Containers:**
Run the following command to build the images, automatically fetch the ML models & environment configurations, and start the network:
```bash
docker-compose up --build
```
7. **Explore the Application:**
Once the terminal indicates both containers are running (and the backend has finished downloading the required ML models and `.env` file), open your web browser to start exploring!

**Frontend Interface:** http://localhost:5173

**Backend API Documentation:** http://localhost:8000/docs`
