# Google Docs Clone
This project is a Google Docs clone application that allows users to edit documents in real-time. It is built using FastAPI for the backend and ReactJS for the frontend. The app is deployed on an AWS EC2 instance using Docker, with DynamoDB as the backend database. Additionally, the project includes a CI/CD pipeline configured via GitHub Actions, which automates the deployment process.

## Features
Real-time Collaboration: Multiple users can edit documents simultaneously with updates reflected in real-time.
FastAPI Backend: The backend is powered by FastAPI, providing a high-performance API for handling document operations.
ReactJS Frontend: The frontend is built with ReactJS, offering a responsive and dynamic user interface.
AWS Deployment: The app is containerized using Docker and deployed on an AWS EC2 instance.
DynamoDB Integration: All document data is stored in AWS DynamoDB, ensuring scalability and reliability.
CI/CD Pipeline: Automated CI/CD pipeline configured with GitHub Actions to build, push Docker images to AWS ECR, and deploy to EC2 instances.

## Tech Stack
- **Frontend**: ReactJS
- **Backend**: FastAPI (Python)
- **Database**: AWS DynamoDB
- **Deployment**: AWS EC2, Docker
- **CI/CD**: GitHub Actions, AWS ECR

# Deployment
The application is deployed on an AWS EC2 instance. The CI/CD pipeline automatically handles the following:

- Builds Docker images for the frontend and backend.
- Pushes the Docker images to AWS Elastic Container Registry (ECR).
- SSHs into the EC2 instance to pull the latest Docker images from ECR.
- Restarts the application with the updated images.


# Demo

Click [here](http://ec2-54-236-89-70.compute-1.amazonaws.com/editor/default) for demo.

# Contact
For any questions or feedback, feel free to reach out:

Email: raj.madhu0406@gmail.com
GitHub: rajmadhu0406
