
# Assignment 2 — Transit AI Study Assistant

## Overview

This project implements a conversational AI system called Transit AI Study Assistant.

The assistant is designed to support questions related to transit analytics, AI systems, predictive modelling, data governance, weather, and project planning.

The interface is implemented using Gradio.

## Chatbot Personality

The assistant has a professional and practical personality. It responds clearly and concisely, with a focus on helping users understand AI and transit analytics concepts.

## Services

### Service 1: API Calls

The chatbot includes a weather service using the Open-Meteo API.

When the user asks about the weather, the system:
1. Uses the Open-Meteo geocoding API to find the city.
2. Uses the Open-Meteo forecast API to retrieve current weather.
3. Rewrites the structured API response into natural language.

The API output is not returned verbatim.

### Service 2: Semantic Query

The chatbot includes a semantic search service using ChromaDB with file persistence.

The local knowledge base is stored in:

```text
data/transit_ai_knowledge.md
```

## Chatbot Demo

The following screenshot demonstrates interactions with all three services using the Transit AI Study Assistant:

- **API Service** :  Weather query
- **Semantic Search** :  Knowledge base question
- **Function Calling** :  Checklist generation

![Chat Demo](image/chat_exchange.jpg)
