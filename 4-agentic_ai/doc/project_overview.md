# Sports Intelligence Agent - Project Overview

## High-Level Summary

The Sports Intelligence Agent is a Streamlit-based web application designed for real-time sports betting analysis, news aggregation, and AI-powered insights. It integrates multiple APIs to provide:
- Live odds from various bookmakers
- Detection of value bets (arbitrage opportunities)
- Customizable analyst personas for tailored analysis
- Aggregated sports news from multiple sources
- Transparent access to raw data and sources

## User Experience

Users interact with a modern, multi-tabbed web interface:
- **Sidebar**: Configure sport, region, and analyst persona
- **Live Odds Tab**: View real-time odds for upcoming games
- **Value Finder Tab**: Discover significant odds discrepancies across bookmakers
- **News + Analysis Tab**: Get the latest news and AI-generated game analysis
- **Source Data Tab**: Inspect raw API data for full transparency

The app is designed for both casual fans and professional bettors, offering both simple storylines and deep statistical insights.

## Main Components

### 1. API Integration
- **Odds API**: Fetches available sports, live odds, and scores
- **Tavily & DuckDuckGo News**: Aggregates recent news articles
- **Groq LLM**: Provides AI-powered analysis using custom prompts

### 2. Analyst Personas
- Pre-built personas (ESPN Analyst, Vegas Sharp, Statistical Guru, Casual Fan, Contrarian Analyst)
- Option for custom persona input

### 3. Value Bet Detection
- Compares odds across bookmakers
- Highlights games with significant discrepancies (potential arbitrage)

### 4. News Aggregation
- Fetches and displays recent news for selected games
- Shows source transparency for each article

### 5. AI Analysis
- Combines odds, news, and persona to generate tailored game analysis
- Offers predictions, key factors, and betting recommendations

### 6. Streamlit UI
- Sidebar for configuration
- Tabs for different features
- Expanders and containers for detailed data display

## Transparency & Source Data
- Users can view raw API responses and the full prompt sent to the LLM for maximum transparency.

---

For a detailed breakdown of the `sports_agent.py` implementation, see `sports_agent_explained.md` in this folder.
