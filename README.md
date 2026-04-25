# Anomaly Detector in PCBs

## Description
This is a web application that uses deep learning to detect anomalies in printed circuit boards (PCBs). It uses autoencoders and variational autoencoders to learn the normal patterns of PCBs and detect anomalies in new ones.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Run the application - Local:
```bash
cd frontend && npm install && npm start
```
```bash
cd backend && uv sync && uv run uvicorn main:app --reload
```

2. Run the application - Docker:
```bash
./docker compose up -d --build
```

## Usage

1. Open the application in your browser:
```
http://localhost:4200
```

2. Upload an image of a PCB:
```
http://localhost:4200/upload
```

3. The application will detect anomalies in the PCB and display the results:
```
http://localhost:4200/results
```
