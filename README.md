\# Secure B2B Data Sharing \& Federated Learning Prototype



This project aims to demonstrate how two companies can collaborate, and compute joint metrics securely \*\*without exposing or transferring their raw data\*\*.



\---



\## 🛠️ Prerequisites \& Installation



To run these scripts locally, you need Python installed on your computer. 



Open your terminal or command prompt and install the required lightweight libraries (FastAPI, Uvicorn, and Requests):



Bash

**pip install fastapi uvicorn requests**





Step-by-Step Usage Guide

Step 1: Run the Data Provider (provider.py)

The provider acts as the secure server holding the database (datasharing.db).



Open a terminal window in your project folder.



Start the server with Uvicorn:



Bash

**python -m uvicorn provider:app --reload**



You should see a message indicating that the server is running on http://127.0.0.1:8000.





Step 2: Run the Data Consumer (consumer.py)

The consumer script requests data from the running provider using a secure token.



Open a second, separate terminal window 



Open consumer.py in your code editor and choose your access token (e.g., token-logistics for basic access or token-admin for full access).



Run the consumer script:



Bash

**python consumer.py**

The script will contact the provider, authenticate via token, receive the authorized data package, and display the results cleanly in the terminal.



Step 3: Run the Federated Learning Demo (federated\_demo.py)

If you want to see how multiple companies collaborate without sharing raw data at all, run the federated demo.





Run the demo script:



Bash

**python federated\_demo.py**



What happens here:



The script creates two mock databases simulating Plant A and Plant B.



Each plant computes its local metrics internally (keeping raw secrets safe).



Only the aggregated summary and sample sizes are sent to a central coordinator.



The coordinator calculates a unified Global Average, proving that secure cross-company collaboration is possible while maintaining data privacy.



\---

\## 🧭 Core Principles (The Big Picture)



In traditional data sharing, Company A sends its sensitive raw files or database records directly to Company B. This creates significant risks regarding privacy, data leaks, and loss of control.



This project demonstrates two modern approaches to solve this problem:



1\. \*\*Controlled Direct Sharing (Access Control):\*\*

&#x20;  The data provider exposes an API protected by secure tokens. Depending on the consumer's access level (`basic` or `advanced`), only authorized data rows are returned.

2\. \*\*Federated Learning / Privacy-Preserving Computation:\*\*

&#x20;  Instead of moving raw data, \*\*the code goes to the data\*\*. Each company computes summaries or model weights locally on its own private database and shares \*only\* the mathematical results (or aggregated metrics) with a coordinator. Raw data never leaves its origin.



\---



\## 📂 Project Structure



The project consists of three main Python scripts:



\*   `provider.py`: A secure FastAPI server representing a manufacturing plant. It manages an SQLite database, enforces token-based authentication, controls access levels, and provides endpoints for both direct data and model weights.

\*   `consumer.py`: A client script representing a partner company or coordinator that securely requests authorized information from the provider using authentication tokens.

\*   `federated_demo.py`: A standalone simulation script that demonstrates how two separate factories can calculate a joint average metric without sharing their proprietary product lists or quantities with each other.






