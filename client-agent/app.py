import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

# 🎨 Page Config
st.set_page_config(page_title="Freelance Job Finder", page_icon="💼", layout="wide")

# 🎨 Custom Styling
st.markdown("""
<style>
body {
    background-color: #0e1117;
}

.card {
    background-color: #1e1e1e;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    border: 1px solid #333;
    transition: 0.3s;
}

.card:hover {
    border: 1px solid #4CAF50;
    transform: scale(1.01);
}

.title {
    color: white;
    font-size: 18px;
    font-weight: bold;
}

.button {
    display: inline-block;
    padding: 10px 15px;
    background-color: #4CAF50;
    color: white !important;
    text-decoration: none;
    border-radius: 8px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# 🧠 Title
st.title("💼 Freelance Job Finder AI")
st.markdown("Find freelance jobs across India with a modern UI 🚀")

# Inputs
service = st.text_input("💼 Your Skill", "web developer")

location = st.selectbox(
    "📍 Location",
    ["India", "Remote", "Chennai", "Bangalore", "Mumbai", "Delhi", "Hyderabad"]
)

platform = st.selectbox(
    "🌐 Platform",
    ["All", "Upwork", "Freelancer", "Internshala"]
)

# 🔧 Clean redirect links
def clean_link(href):
    try:
        parsed = urllib.parse.urlparse(href)
        query = urllib.parse.parse_qs(parsed.query)

        if "uddg" in query:
            return query["uddg"][0]
        return href
    except:
        return href

# 🔍 Search jobs
def search_jobs(service, location, platform):
    if platform == "Upwork":
        query = f"{service} freelance jobs {location} site:upwork.com"
    elif platform == "Freelancer":
        query = f"{service} freelance jobs {location} site:freelancer.com"
    elif platform == "Internshala":
        query = f"{service} jobs {location} site:internshala.com"
    else:
        query = f"{service} freelance jobs {location}"

    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    results = []

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.find_all("a", class_="result__a", limit=10)

        for link in links:
            title = link.text
            raw_href = link.get("href")
            clean_url = clean_link(raw_href)

            results.append({
                "title": title,
                "link": clean_url
            })

    except Exception as e:
        st.error(f"Error: {e}")

    return results

# 🚀 Button Action
if st.button("🔍 Find Jobs"):
    if service:
        st.success(f"Searching jobs in {location}... 🔍")

        jobs = search_jobs(service, location, platform)

        if jobs:
            st.subheader("📋 Job Opportunities")

            for job in jobs:
                st.markdown(f"""
                <div class="card">
                    <div class="title">{job['title']}</div>
                    <a href="{job['link']}" target="_blank" class="button">
                        🔗 Open Job
                    </a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No jobs found. Try different keywords.")
    else:
        st.warning("Please enter your skill!")