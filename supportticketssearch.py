import sys
import pysqlite3
sys.modules["sqlite3"] = pysqlite3
sys.modules["pysqlite3"] = pysqlite3

import os
import pandas as pd
import streamlit as st
from openai import OpenAI
import chromadb
from chroma_setup import load_chroma_collection

# Load OpenAI key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Load CSV
github_url = "https://raw.githubusercontent.com/pqhunter15/supportticketchromasimilarity/main/support_cleaned_1.csv"
df = pd.read_csv(github_url)

# Load Chroma collection (only once)
if "collection" not in st.session_state:
    st.session_state.collection = load_chroma_collection()
collection = st.session_state.collection

# Query input


#pulling list of eligible tags
# Extract all unique tech tags from all 3 columns
tech_tag_columns = ["tech_tag_1", "tech_tag_2", "tech_tag_3"]
all_tags_series = pd.concat([df[col].dropna() for col in tech_tag_columns])
tech_tags = sorted(set(tag.strip() for tag in all_tags_series if isinstance(tag, str)))



with st.form(key="query_form"):
    query = st.text_input("Enter Ticket Body Text Here:")
    selected_tags = st.multiselect("Select Tags (Optional):", tech_tags)
    submit = st.form_submit_button(
    label="Submit",
    help="Click to submit your search request"
)

st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #D9534F;
    color: white;
    font-weight: 600;
    border: none;
    border-radius: 4px;
    padding: 0.5rem 1.2rem;
    transition: background-color 0.2s ease;
}
div.stButton > button:first-child:hover {
    background-color: #C9302C;
}
</style>
""", unsafe_allow_html=True)

# --- Filter construction ---
filters = []
for tag in selected_tags:
    filters.append({
        "$or": [
            {"tech_tag_1": tag},
            {"tech_tag_2": tag},
            {"tech_tag_3": tag}
        ]
    })

if len(filters) == 1:
    where_clause = filters[0]
elif len(filters) > 1:
    where_clause = {"$and": filters}
else:
    where_clause = None


# Rewrite query using OpenAI
def rewrite_query_openai(original_query, num_rewrites=2):
    reworded = []
    for _ in range(num_rewrites):
        prompt = (
            "Rewrite the following question with different phrasing, structure, and length, "
            "but keep the meaning the same:\n\n"
            f"{original_query}"
        )
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=200
            )
            rewritten = response.choices[0].message.content.strip()
            reworded.append(rewritten)
        except Exception as e:
            st.warning(f"OpenAI rewrite failed: {e}")
    return reworded

# Run search
top_k = 3
if query and collection:
    with st.spinner("Rewriting and searching..."):
        reworded_queries = rewrite_query_openai(query, num_rewrites=2)
        all_queries = [query] + reworded_queries

        results_by_doc = {}

        for q in all_queries:
            results = collection.query(
                query_texts=[q],
                n_results=top_k,
                where=where_clause,
                include=["documents", "metadatas", "distances"]
            )

            for doc, meta, dist in zip(*[results[k][0] for k in ["documents", "metadatas", "distances"]]):
                doc_id = int(meta["original_doc_id"])
                if doc_id not in results_by_doc or dist < results_by_doc[doc_id]["dist"]:
                    results_by_doc[doc_id] = {
                        "meta": meta,
                        "doc": doc,
                        "dist": dist
                    }

        sorted_results = sorted(results_by_doc.items(), key=lambda x: x[1]["dist"])
        top_results = sorted_results[:top_k]

if submit and query and top_results:
    st.markdown("### Results:")

    for doc_id, entry in top_results:
        row = df[df["doc_id"] == doc_id].iloc[0]

        similarity = f"{entry['dist']:.4f}"
        body = row['body']
        answer = row['answer']
        topic = row['topic_label']

        st.markdown(f"""
        <div style="
        border: 2px solid #32CD32;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 24px;
        background-color: #FFFFFF;
        box-shadow: 0 4px 8px rgba(0,0,0,0.03);
        font-family: 'Segoe UI', sans-serif;
    ">
        <div style="font-weight: 600; font-size: 16px; margin-bottom: 12px; color: #1A1A1A;">
            Similarity Score: {similarity}
        </div>
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="background-color: #F3F3F3;">
                <th style="text-align: left; width: 50%; padding: 10px; border-bottom: 1px solid #32CD32;">Ticket</th>
                <th style="text-align: left; width: 50%; padding: 10px; border-bottom: 1px solid #32CD32;">Response</th>
            </tr>
            <tr>
                <td style="padding: 10px; vertical-align: top; color: #333333;">{body[:800]}</td>
                <td style="padding: 10px; vertical-align: top; color: #333333;">{answer}</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)






