# IntelliChat: An Advanced Information Retrieval Chatbot Powered by Web Scraping and Topic Classification

### Team Members:
- **Sai Venkat Reddy Sheri** (ssheri@buffalo.edu)
- **Praneeth Posina** (leelasat@buffalo.edu)
- **Swetha Reddy Ganta** (sganta3@buffalo.edu)

---

## Introduction

This project involves building an **end-to-end Information Retrieval chatbot** capable of handling both general conversations (chit-chat) and answering factual queries using information retrieved from Wikipedia documents. The chatbot integrates **web scraping, document indexing, query classification, and retrieval techniques** to provide accurate and intelligent responses.

### Key Features:
- **Web Scraper**: Extracts and indexes data from Wikipedia (~60,000 documents).
- **SVM Classifier**: Differentiates between chit-chat and Wiki-based queries.
- **TF-IDF & Cosine Similarity**: Used for document retrieval and ranking.
- **OpenAI API Integration**: Handles chit-chat conversations.
- **Summarization & Prompt Engineering**: Provides concise and accurate responses.
- **Real-time Analytics**: Tracks chatbot performance and user interactions.

---

## Methodology

### 1. **Preprocessing**
- **Tokenization, Stemming, and Lemmatization** using NLTK.
- **Stop-word Removal** to filter out unimportant words.
- **Python Regular Expressions** for text cleaning.
- **Semantic Analysis** with NLTK to understand text context.
- **Linguistic Corpora Access** for improved language modeling.

### 2. **Chit-chat vs. Wiki Classification**
- Implemented an **SVM Classifier** to classify user queries.
- Manual selection through **UI dropdown** for mode selection:
  - General Conversation (Chit-chat)
  - Self-Operating Classifier (Auto-detect query type)
  - Multi-Topic (Handles multiple topics)
  - Specific Topic Selection

### 3. **Chit-chat Handling**
- Uses **OpenAI API** for human-like responses.
- Supports **engaging, friendly, and context-aware** conversations.
- Adapts to different user interaction styles.

### 4. **Topic Classification**
- Further classification of informational queries using **SVM**.
- Recognizes specific topics like **Health, Technology, Environment, Food**.
- Enables topic-specific document retrieval for precise results.

### 5. **Document Retrieval with Inverted Index**
- Uses **TF-IDF (Term Frequency-Inverse Document Frequency)** to determine word importance.
- **Cosine Similarity** for comparing query-document relevance.
- **Inverted Index** for fast and efficient document lookup.

### 6. **Re-ranking Retrieved Documents**
- Initial retrieval is **refined** by recalculating relevance scores.
- Ensures the most pertinent documents are prioritized.

### 7. **Post-processing**
- **Summarization**: Extracts key points from retrieved documents using **OpenAI API**.
- **Prompt Engineering**: Provides **precise answers** rather than generic summaries.
- Example: Query "What is the capital of France?" directly returns **"Paris"**.

---

## Analytics
The chatbot includes real-time analytics with the following visualizations:
1. **Bar Graph**: Distribution of questions asked on different topics.
2. **Pie Chart**: Ratio of chit-chat vs. topic-specific queries.
3. **Line Graph**: Queries per second to monitor traffic and performance.

---

## Conclusion
The system efficiently **tokenizes, pre-processes, and retrieves** relevant information using **TF-IDF and Cosine Similarity**. Retrieved documents are **ranked**, summarized, and refined to provide users with **accurate, topic-specific, and user-friendly** responses. The chatbot balances **chit-chat and factual answering**, ensuring an engaging and informative user experience.

---

## Team Contributions
| Team Member | Contribution |
|-------------|-------------|
| **Sai Venkat Reddy Sheri** | TF-IDF, Scraping, Indexing, UI Development |
| **Praneeth Posina** | SVM Classifier, OpenAI Integration, Analytics |
| **Swetha Reddy Ganta** | Cosine Similarity, Document Summarization, Prompt Engineering |

---

## Setup & Installation
### Prerequisites:
- Python 3.x
- Required Libraries: `pip install -r requirements.txt`
- OpenAI API Key (for chit-chat and summarization)

### Run Instructions:
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the chatbot:
   ```bash
   python chatbot.py
   ```

---

## Future Improvements
- Expand dataset beyond Wikipedia for more diverse responses.
- Improve topic classification accuracy beyond 80%.
- Optimize document ranking with advanced NLP techniques.
- Enhance real-time analytics with interactive dashboards.
