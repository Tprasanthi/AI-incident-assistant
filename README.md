# AI Incident Root Cause Assistant

## Overview

This project is an MVP for an AI-powered Incident Root Cause Assistant. It helps engineering and operations teams analyze production incidents faster by ingesting logs, metrics, alerts, incident tickets, and deployment events.

The assistant uses RAG, LangGraph, Qdrant, AWS Lambda, S3, DynamoDB, SNS, OpenTelemetry, and LangSmith to summarize incidents, infer probable root causes, recommend remediation, and highlight correlated anomalies.

## Features

- Ingest operational telemetry from S3
- Mask PII and secrets before indexing
- Chunk and embed logs, tickets, metrics, alerts, and deployments
- Store embeddings in Qdrant
- Track incident metadata in DynamoDB
- Analyze incidents using a LangGraph workflow
- Generate incident summary, timeline, root cause, confidence, and remediation
- Publish notifications through SNS
- Trace LLM calls with LangSmith
- Trace infrastructure calls using OpenTelemetry
- Dockerized local development

## Tech Stack

- Python 3.11
- AWS Lambda
- Amazon S3
- Amazon DynamoDB
- Amazon SNS
- Qdrant
- LangChain
- LangGraph
- LangSmith
- OpenTelemetry
- Docker
- FastAPI

## Architecture

See `docs/architecture.md`.

## Local Setup

### 1. Clone repository

```bash
git clone [github.com](https://github.com/YOUR_USERNAME/ai-incident-rca-assistant.git)
cd ai-incident-rca-assistant
