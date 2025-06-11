In this project, I utilized n8n to develop a Telegram bot capable of reading a file containing **Omani legal texts** and answering questions related to the articles within the document.

The bot is integrated with **Google Drive** for file storage and retrieval, and is also connected to Telegram for user interaction. Additionally, **Supabase** was used as a vector database to store the embeddings of the legal documents.

The bot is built using a contextual Retrieval-Augmented Generation (RAG) approach. It employs **OpenAI’s GPT-4** model as the main conversational engine and uses **OpenAI’s text-embedding-3-small** model to generate embeddings for the legal texts. To enhance context handling, **Gemini-1.5-Flash-8B-Latest** was incorporated into the retrieval pipeline.
