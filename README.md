# Technical Support Ticket Semantic Similarity Search- An efficiency tool for technical support agents
This is a semantic similarity search system that uses vector embeddings of support ticket text, stored and indexed in a ChromaDB vector database, with optional metadata filtering, and a Streamlit front‑end.
The system improves retrieval accuracy by query rewriting via the OpenAI API, runs evaluation in Google Colab, and is deployed with storage on Hugging Face Datasets for persistence.

This is meant to be a proof of concept for an application which could be integrated with a support ticketing software, to be used as an internal tool for technical support agents. 

This can assist agents with:
1. Keeping track of bugs that have already been identified by other agents
2. Quickly answering FAQs without the need for many macros
3. Training new support agents
  
How it works:
1. Input your support ticket 'body' into the query.
2. Filter by the technologies mentioned in the ticket using the tag field.
3. It is reccomended to first search without tags, and then, if the search doesn't yeild meaningful results, apply tags.
4. Choose the most appropriate ticket response to copy and paste back into your response to the customer.

You can access the application here: https://supportticketchromasimilarity-gqeuyq44wkvxnovui8jbf4.streamlit.app/


Because the collection was created from a dataset of sample support tickets, only certain query topics will yeild actionable results.

Below is a list of sample queries to try, but you can also look through the technology tags to find a tech to ask a question about:

  Users are experiencing issues with the Evernote and Shopify apps. Can you confirm the problem and let us know what the error messages say and what’s been done so far? If needed, we’re happy to set up a call to work through the issue. Let us know what time works best.

  Our digital marketing campaign failed to deploy across several platforms. We’ve already reviewed network settings and refreshed our security tools, but no improvement. It could be a firewall rule or even hidden malware. Can you dig in and help us resolve it?

  Several users are experiencing crashes and lag across Malwarebytes 4.4, Microsoft Teams, and Slack. We think recent updates may be conflicting. So far we’ve tried device restarts, cache clearing, and rolling back patches, but no improvement. Could you assist us with a more permanent fix?

  The website for our agency has been going down occasionally, and we suspect the hosting server may be at fault. We tried restarting the server and clearing its cache, but the problem hasn’t gone away. Please look into this as soon as possible so we can avoid further disruptions.

We're having trouble maintaining a stable connection with the Google Nest Wifi Router, which is disrupting our marketing efforts. The issue might’ve been triggered by a firmware update or a misconfiguration. We’ve already tried basic troubleshooting like restarting and checking all the physical connections, but no luck so far.
  
  
