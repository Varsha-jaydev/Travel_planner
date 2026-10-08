# ✈️ AI Travel Planner

A multi-agent travel planner built with **CrewAI** and **Ollama (Qwen3)** that generates personalized travel itineraries based on destination, trip length, budget, and interests.

## Features

* 🔎 Destination research
* 🗓️ Day-by-day itinerary planning
* 💰 Budget estimation
* ❤️ Personalized interests
* 🤖 Local LLM with Ollama

## Setup

```bash
git clone <your-repo-url>
cd travel-planner

pip install -r requirements.txt
```

Make sure Ollama is running and the model is available:

```bash
ollama pull qwen3:8b
ollama serve
```

## Run

### CLI

```bash
python agent.py \
  --destination "Tokyo, Japan" \
  --days 5 \
  --budget 2000 \
  --interests "food, culture, history"
```

### Streamlit

```bash
streamlit run app.py
```

## Tech Stack

* Python
* CrewAI
* Ollama / Qwen3
* Streamlit
