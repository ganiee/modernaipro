
"""
Cricket Intelligence Agent - T20, ODI & Test (Men & Women)
Provides live odds, news aggregation, and AI-driven analysis for men's and women's cricket formats.
"""

import streamlit as st
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from langchain_groq import ChatGroq
from tavily import TavilyClient

# Load environment variables
load_dotenv()
ODDS_API_KEY = os.getenv("ODDS_API_KEY")
ODDS_BASE_URL = os.getenv("ODDS_BASE_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Cricket-specific analyst personas
ANALYST_PERSONAS = {
    "Cricket Statistician": "You are a cricket statistician. Use advanced stats, player form, pitch reports, and historical T20 data. Express uncertainty and cite stats.",
    "Ex-Player": "You are a former international cricketer. Share insights on team strategies, player mindset, and matchups. Use anecdotes and expert opinion.",
    "Fan": "You are a passionate cricket fan. Focus on excitement, star players, and big moments. Keep it fun and engaging.",
    "Contrarian": "You are a contrarian analyst. Look for upsets, underdog value, and challenge popular opinion.",
    "Coach": "You are a cricket coach. Analyze tactics, team balance, and key matchups. Offer practical advice."
}


# ============== API FUNCTIONS ==============

@st.cache_data(ttl=300)
def get_cricket_events(format_key):
    """Fetch cricket events (men's and women's) from The Odds API for a given format.

    The Odds API may use different sport keys for women's competitions depending on provider
    or API version. Try a list of candidate sport keys for the requested format and return
    the first non-empty successful response.
    """
    if not ODDS_API_KEY or not ODDS_BASE_URL:
        print("[DEBUG] ODDS_API_KEY or ODDS_BASE_URL not configured.")
        return []

    candidates = {
        "T20": ["cricket_international_t20", "cricket_t20_men", "cricket_t20"],
        "Women T20": [
            "cricket_womens_t20",
            "cricket_women_t20",
            "cricket_international_women_t20",
            "cricket_t20_women",
            "cricket_t20_womens",
            # Fallback to general T20 keys when a women-specific sport key isn't available
            "cricket_international_t20",
            "cricket_t20_men",
            "cricket_t20"
        ],
        "ODI": ["cricket_odi", "cricket_international_odi", "cricket_test_match"],
        "Test": ["cricket_test_match"]
    }

    keys_to_try = candidates.get(format_key, ["cricket_international_t20"]) 
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us,uk,eu,au",
        "markets": "h2h,spreads,totals",
        "oddsFormat": "decimal"
    }

    for sport_key in keys_to_try:
        url = f"{ODDS_BASE_URL}/sports/{sport_key}/odds/"
        try:
            print(f"[DEBUG] Trying sport key: {sport_key}")
            response = requests.get(url, params=params, timeout=10)
        except Exception as e:
            print(f"[DEBUG] Request exception for {sport_key}: {e}")
            continue

        print(f"[DEBUG] Requesting: {url}")
        print(f"[DEBUG] Params: {params}")
        print(f"[DEBUG] Status Code: {response.status_code}")
        try:
            print(f"[DEBUG] Response (truncated): {response.text[:500]}")
        except Exception as e:
            print(f"[DEBUG] Error printing response: {e}")

        if response.status_code == 200:
            try:
                data = response.json()
            except Exception as e:
                print(f"[DEBUG] JSON decode error for {sport_key}: {e}")
                continue
            if data:
                print(f"[DEBUG] Returning data for sport key: {sport_key}")
                return {"sport_key": sport_key, "events": data}
            else:
                print(f"[DEBUG] Empty data for sport key: {sport_key}")
        else:
            print(f"[DEBUG] API Error for {sport_key}: {response.status_code} - {getattr(response, 'text', '')}")

    print("[DEBUG] No events found for any candidate sport key.")
    return {"sport_key": None, "events": []}

@st.cache_data(ttl=60)
def get_news(query, max_results=5):
    if TAVILY_API_KEY:
        try:
            tavily = TavilyClient(api_key=TAVILY_API_KEY)
            response = tavily.search(query, max_results=max_results, search_depth="basic")
            results = []
            for r in response.get("results", []):
                results.append({
                    "title": r.get("title", ""),
                    "body": r.get("content", ""),
                    "source": r.get("url", "")
                })
            return results
        except Exception:
            pass
    try:
        results = DDGS().news(query, region='in-en', max_results=max_results)
        return list(results)
    except Exception:
        return []

def analyze_with_llm(prompt):
    try:
        llm = ChatGroq(model_name="openai/gpt-oss-120b", api_key=GROQ_API_KEY)
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"LLM Error: {e}"


def is_womens_event(event: dict) -> bool:
    """Heuristic to detect whether an event pertains to a women's match.

    Checks `sport_title` for 'women' and looks for 'women' markers in team names.
    This is best-effort and may miss cases where providers don't label gender.
    """
    try:
        sport_title = (event.get("sport_title") or "").lower()
        if "women" in sport_title:
            return True
        # Check team names for common markers
        for team in (event.get("home_team", ""), event.get("away_team", "")):
            t = team.lower()
            if "women" in t or "women's" in t or "womens" in t:
                return True
            # common suffix like 'W' (e.g., 'India Women' sometimes 'India W')
            if t.endswith(" w") or t.endswith(" women") or t.endswith(" women\""):
                return True
        return False
    except Exception:
        return False

# ============== STREAMLIT UI ==============


def main():
    st.set_page_config(
        page_title="Cricket Intelligence Agent (T20, ODI & Test — Men & Women)",
        page_icon="🏏",
        layout="wide"
    )
    st.title("🏏 Cricket Intelligence Agent - T20, ODI & Test (Men & Women)")
    st.caption("Live odds + News + AI Analysis for men's and women's cricket worldwide")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        format_key = st.selectbox("Select Format", ["T20", "Women T20", "ODI", "Test"], index=0)
        persona = st.selectbox("Select Analyst Persona", list(ANALYST_PERSONAS.keys()))
        custom_persona = st.text_area("Or create custom persona", placeholder="You are a cricket expert...", height=80)

    # Main tabs
    tab1, tab2, tab3 = st.tabs(["🏏 Live Odds", "📰 News + Analysis", "🔍 Source Data"])

    # Tab 1: Live Odds
    with tab1:
        st.header(f"Live Odds: {format_key} Cricket")
        with st.spinner(f"Fetching {format_key} events..."):
            result = get_cricket_events(format_key)
        sport_key_used = result.get("sport_key")
        events = result.get("events", [])

        # If user requested Women T20, apply heuristic filter to try to keep only women's matches
        if format_key == "Women T20":
            filtered = [e for e in events if is_womens_event(e)]
            # Show note when filtering applied
            if filtered:
                st.caption(f"Filtering applied: showing {len(filtered)} events detected as women's matches (sport_key: {sport_key_used})")
                events = filtered
            else:
                st.caption(f"No explicit women's labels found — showing all events from sport_key: {sport_key_used}")

        if events:
            st.success(f"Found {len(events)} upcoming matches")
            for event in events[:10]:
                with st.expander(f"{event['away_team']} @ {event['home_team']} | {datetime.fromisoformat(event['commence_time'].replace('Z', '+00:00')).strftime('%m/%d %I:%M %p')}"):
                    for bookmaker in event.get('bookmakers', [])[:4]:
                        st.markdown(f"**{bookmaker['title']}**")
                        for market in bookmaker.get('markets', []):
                            if market['key'] == 'h2h':
                                for outcome in market['outcomes']:
                                    st.markdown(f"{outcome['name']}: {outcome['price']}")
        else:
            st.warning(f"No {format_key} events found.")

    # Tab 2: News + Analysis
    with tab2:
        st.header("📰 News + AI Analysis")
        if events:
            match_options = [f"{e['away_team']} @ {e['home_team']}" for e in events[:10]]
            selected_match = st.selectbox("Select match to analyze", match_options)
            selected_event = events[match_options.index(selected_match)]
            teams = f"{selected_event['away_team']} {selected_event['home_team']}"
            analyze_btn = st.button("🔍 Analyze Match", type="primary")
            if analyze_btn:
                with st.spinner("Fetching news..."):
                    news = get_news(f"{teams} {format_key} cricket news", max_results=6)
                news_text = ""
                for article in news:
                    with st.expander(f"📄 {article.get('title', 'No title')[:60]}..."):
                        st.write(article.get('body', 'No content'))
                        st.caption(f"Source: {article.get('source', 'Unknown')}")
                    news_text += f"Title: {article.get('title')}\nContent: {article.get('body')}\n\n"
                odds_context = ""
                for bookmaker in selected_event.get('bookmakers', [])[:2]:
                    odds_context += f"\n{bookmaker['title']}:\n"
                    for market in bookmaker.get('markets', []):
                        if market['key'] == 'h2h':
                            for outcome in market['outcomes']:
                                odds_context += f"  {outcome['name']}: {outcome['price']}\n"
                active_persona = custom_persona if custom_persona else ANALYST_PERSONAS[persona]
                prompt = f"""
{active_persona}

Analyze this upcoming {format_key} match: {selected_match}
Game Time: {selected_event['commence_time']}

CURRENT BETTING ODDS:
{odds_context}

LATEST NEWS & INFORMATION:
{news_text}

Provide:
1. Key factors that will influence this match
2. Your prediction with confidence level
3. Betting recommendation (if appropriate)
4. Any concerns or things to watch

Be specific and reference the actual news/odds data provided.
"""
                with st.spinner("Generating AI analysis..."):
                    analysis = analyze_with_llm(prompt)
                st.subheader(f"🤖 {persona} Analysis")
                st.markdown(analysis)
                with st.expander("🔍 View Full Prompt (Transparency)"):
                    st.code(prompt, language="text")
        else:
            st.info("No matches to analyze.")

    # Tab 3: Source Data
    with tab3:
        st.header("🔍 Raw Source Data")
        if events:
            st.subheader("Raw API Response")
            st.json(events[:3])
            st.subheader("Data Summary")
            st.write(f"- Total events: {len(events)}")
            if events:
                st.write(f"- Bookmakers: {len(events[0].get('bookmakers', []))}")
                st.write(f"- Markets available: {[m['key'] for m in events[0].get('bookmakers', [{}])[0].get('markets', [])]}")
        else:
            st.info("No data loaded.")

        # Show which sport key was used for the last fetch
        try:
            st.caption(f"Sport key used for last fetch: {sport_key_used}")
        except Exception:
            pass
        else:
            st.info("No data loaded.")

if __name__ == "__main__":
    main()
