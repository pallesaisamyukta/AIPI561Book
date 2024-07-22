# Use the official Node.js image from the Docker Hub
FROM node:12.22.9

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files into the container at /app
COPY package.json package-lock.json /app/

# Install the dependencies
RUN npm install

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory to where you usually run `npm start`
WORKDIR /app/src/components

# Expose port 3000 for the React app
EXPOSE 3000

# Define the command to run the React app
CMD ["npm", "start"]