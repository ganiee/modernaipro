# sports_agent.py - Detailed Explanation

## High-Level Summary

`sports_agent.py` is a Streamlit web app that combines real-time sports odds, news aggregation, and AI-powered analysis. It is designed for sports fans and bettors to:
- View live odds from multiple bookmakers
- Detect value bets (arbitrage opportunities)
- Get news and AI analysis for upcoming games
- Customize the analysis style via personas
- Inspect raw data for transparency

## User Experience

- **Sidebar**: Configure sport, region, and analyst persona (or create a custom one)
- **Tabs**:
  - **Live Odds**: See odds for upcoming games, broken down by bookmaker
  - **Value Finder**: Find games with significant odds discrepancies
  - **News + Analysis**: Get latest news and AI-generated analysis for selected games
  - **Source Data**: Inspect raw API responses and data summaries

## Detailed Component Breakdown

### 1. API Functions
- **get_sports**: Fetches available sports from The Odds API
- **get_odds**: Retrieves odds for a selected sport and region
- **get_scores**: Gets recent scores for a sport
- **get_news**: Aggregates news using Tavily (primary) and DuckDuckGo (fallback)
- **analyze_with_llm**: Uses Groq LLM to generate analysis based on a custom prompt

### 2. Analyst Personas
- Five pre-built personas (ESPN Analyst, Vegas Sharp, Statistical Guru, Casual Fan, Contrarian Analyst)
- Users can select or write a custom persona to influence the AI's analysis style

### 3. Value Bet Detection
- **find_value_bets**: Scans odds from multiple bookmakers for each event
- Identifies games where the spread between best and worst odds is significant (potential arbitrage)
- Displays details for both home and away teams, including best/worst odds and spread

### 4. Odds Table Formatting
- **format_odds_table**: Prepares odds data for display in tabular format
- Shows odds from up to four bookmakers per game

### 5. News Aggregation & Analysis
- Fetches news articles relevant to selected games
- Displays news with source transparency
- Builds a prompt combining persona, odds, and news for LLM analysis
- AI analysis includes key factors, predictions, recommendations, and concerns

### 6. Streamlit UI Structure
- **Sidebar**: Sport, region, persona selection, API usage tracking
- **Tabs**:
  - **Live Odds**: Odds breakdown by bookmaker
  - **Value Finder**: Value bet opportunities
  - **News + Analysis**: News articles and AI analysis
  - **Source Data**: Raw API data and summary
- Uses expanders, containers, and columns for organized display

### 7. Transparency Features
- Users can view the full prompt sent to the LLM
- Raw API responses are available for inspection

## Summary

`sports_agent.py` provides a comprehensive, interactive experience for sports analysis, betting insights, and news aggregation, powered by real-time data and AI. It is designed for transparency, flexibility, and user customization.
