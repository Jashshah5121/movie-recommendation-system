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

8. **Stopping the Application:**
To shut down the application gracefully, press `Ctrl + C` in the terminal where Docker is running.
To completely remove the containers and clear the network, run:
```bash
docker-compose down
```
## 🛠️ Troubleshooting Common Issues

### Issue: "Ports are not available" or "bind: An attempt was made to access a socket in a way forbidden by its access permissions"
If you have multiple projects running, or if your operating system (especially Windows Hyper-V) has reserved certain ports, Docker may fail to bind to the assigned port (e.g., 5173, 3000, or 8000).

**Step 1: Identify which service is blocked**
Look closely at the port number mentioned at the very end of the terminal error message (e.g., `listen tcp 0.0.0.0:5173`).
* If the error mentions **`5173`**, your **frontend** service is blocked.
* If the error mentions **`8000`**, your **backend** service is blocked.

**Solution A: Change the Port Mapping (Universal Fix)**

You can easily route the application to any open port on your machine by editing the `docker-compose.yml` file. 
1. Open `docker-compose.yml`.
2. Locate the `ports` section under the failing service (e.g., `frontend` or `backend`).
3. Change the **first** number (your host port) to any available port of your choice (e.g., `4000`, `8080`, or `3000`).
   ```yaml
   ports:
     - "4000:5173" # Routes your localhost:4000 to the container's 5173
4. Run docker-compose up --build again and access the app at your newly chosen port (e.g., http://localhost:4000).

**Solution B: Free up the blocked ports (Windows Only)**

Windows occasionally blocks large ranges of ports automatically. You can restart the Host Network Service to clear this blockage.
1. Open a new terminal as an Administrator.
2. Run the following commands:
   ```
   net stop winnat
   net start winnat
   ```
3. Return to your project terminal and run `docker-compose up --build`.
