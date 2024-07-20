# Sales-Team-Performance-Analysis-Using-LLM

## Overview

This project is designed to develop a backend system that leverages a Large Language Model (LLM) to analyze unit price data and provide feedback on individual units and overall team buildings. The system processes the data and generates insights through various API endpoints.

## Features

- **Data Ingestion**: Flexible mechanism to ingest sales data from multiple sheets in an Excel file.
- **LLM Integration**: Utilizes GPT to analyze data and generate insights.
- **API Endpoints**: Provides performance feedback, assesses overall team performance, and evaluates sales performance trends.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/sales-team-performance-analysis.git
   cd sales-team-performance-analysis
   
2. **Install the required dependencies**:
    ```bash
   pip install -r requirements.txt
    
3. **Run the application**:
     ```bash
     uvicorn app:app --host 0.0.0.0 --port 8000 --reload

  # Endpoints

## 1. Best Priced Unit

### Endpoint: 
`/api/top_unit`

### Method: 
`GET`

### Parameters: 
- `unit_id`: Unique identifier for the sales representative.

### Function: 
Returns detailed performance analysis and feedback for the specified sales representative.

### Example Request:
```http
GET /api/top_unit?unit_id=10
```
### Postman Screenshot1
![Testing of 1st endpoint](https://github.com/komal-akhlaq/Sales-Team-Performance-Analysis-Using-LLM/blob/main/1.PNG) 

## 2. Best Historical Units

### Endpoint: 
`/api/unit_price_history`

### Method: 
`GET`

### Parameters: 
- `unit_type`: Type of unit.

### Function: 
Finds the units of the type you are describing with the biggest price changes downwards.

### Example Request:
```http
GET /api/unit_price_history?unit_type=1%20Bed
```

### Postman Screenshot2
![Testing of 2nd endpoint](https://github.com/komal-akhlaq/Sales-Team-Performance-Analysis-Using-LLM/blob/main/2.PNG) 

## 3. Best Building Deals

### Endpoint: 
`/api/building_deals`

### Method: 
`GET`

### Parameters: 
- `neighborhood`: Specific neighborhood.

### Function: 
Find the buildings that are the best deals in a particular neighborhood or type.

### Example Request:
```http
GET /api/building_deals?neighborhood=South%20Loop
```

### Postman Screenshot3
![Testing of 3rd endpoint](https://github.com/komal-akhlaq/Sales-Team-Performance-Analysis-Using-LLM/blob/main/3.PNG) 


