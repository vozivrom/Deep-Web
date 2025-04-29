# Deep Web Data Retrieval Project

## Introduction
This project focuses on **deep web** data retrieval, specifically simulating a web application where data is fetched through a **form-based interface**. These web applications, often used in the **deep web**, do not display information directly via search engines and require form submission to retrieve results. The first part of the project involves creating a web application that simulates this interface, allowing users to send queries to the database. The second part is a script that extracts data and reconstructs the original database.

## Method of Solution

### Form Design
- A **form interface** was designed using **Streamlit** to access the database. This form allows the user to select different filters for the query.

### Database Design
- The **database** was obtained from **Kaggle**, containing over 20,000 Spotify songs.

### Simulated Form Access via REST API
- The form access is **simulated** using a **REST API**. The interface always returns a limited number of results, defined by the constant **k_max**.

### Virtual Tree Structure
- During data retrieval, the form fields are progressively filled, creating a **virtual tree** that we navigate through recursion. Each level of the tree corresponds to a different form field.

### Traversing the Tree
- While traversing the tree, we examine how many results the base application returned. If **k ≥ k_max**, we fill the corresponding form field and move to the next level. If **k < k_max**, we store the results in the reconstructed database and return to the previous level.

### Order of Form Fields
- The order of filling the form fields is important. Internal nodes in the tree correspond to elements with limited selection options (e.g., checkboxes, radio buttons). The leaves correspond to text fields where we try to enter words from a chosen dictionary.

## Implementation

### Backend
- **Python (FastAPI)**: Used for handling the backend API requests.

### Frontend
- **JavaScript, Python (Streamlit)**: Used to create the user interface where the user can input their queries.

### Libraries Used
Pandas, NumPy, JSON, Requests

### How to Run the Application
- Install required libraries:
  ```bash
  pip install -r requirements.txt
- run in the terminal:
  ```bash
  python3 main.py  
