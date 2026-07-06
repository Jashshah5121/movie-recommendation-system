# frontend/Dockerfile

FROM node:20-alpine

WORKDIR /app

# Copy package files and install dependencies
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

# Copy the rest of the frontend code
COPY frontend/ .

# Expose the Vite default port
EXPOSE 5173

# Run the dev server and expose to network
CMD ["npm", "run", "dev", "--", "--host"]