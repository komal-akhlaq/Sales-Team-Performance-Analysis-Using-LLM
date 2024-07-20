
# Sales-Team-Performance-Analysis-Using-LLM

This project aims to develop a sophisticated backend system that leverages a Large Language Model (LLM) to analyze unit price data and provide insightful feedback on individual units and overall team performance. Designed as an automated advisory tool, the system will aid users in making informed decisions in real estate dealings by considering various factors that impact property prices and values. By processing data and generating insights through multiple API endpoints, the system ensures the delivery of the best possible advice for real estate transactions.


## Features

### Data Ingestion:
- Implements a flexible mechanism to ingest sales data from multiple sheets in an Excel file.
- Ensures data validation and transformation to maintain consistency and accuracy.
### LLM Integration:
- Utilizes GPT to analyze data and generate actionable insights.
### API Endpoints:
- Provides performance feedback on individual sales units.
- Assesses overall team performance.
- Evaluates sales performance trends and forecasts.

## Deployment

Our first step is to clone the repository, that can be done by running the following command in terminal or console of your choice

### 1. Setup
```bash
git clone https://github.com/yourusername/sales-team-performance-analysis.git 
```
Now, navigate to the directory of repository you just cloned
```bash
cd sales-team-performance-analysis
```
### 2. Installing dependencies
If you wish, you can install the latest versions of dependencies, but to make things easier and prevent incompatibilities I have included the `requirements.txt`. You can install all required dependencies with running this one single command.
```bash
pip install -r requirements.txt
```
**Note: Ensure that `pip` is installed for this to work, if you are using a virtual environment**

### 3. Finally, Running the project
Just run this command and if everything is installed properly you should have the app up and running.
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
Here's a breakdown of what each argument is doing (for the nerds that wish to tinker around)
| Argument         | Required/Optional | Description                                               |
| :--------------- | :---------------- | :-------------------------------------------------------- |
| `app:app`        | Required          | ASGI application to run (module:application format).      |
| `host 0.0.0.0` | Optional          | IP address to bind to, 0.0.0.0 means accessible from any IP.           |
| `port 8000`    | Optional          | Port number for the server to listen on.                 |
| `reload`       | Optional          | Enables auto-reloading if any changes are made.                 |

Now that everything is running let's see how this API works and what parameters should be passed to obtain fruitful results from the end-points.





## API Reference

### 1. Best Priced Unit

**Endpoint:** 
`/api/top_unit`

**Method:** 
`GET`

**Parameters:** 

| Parameter | Required | Description                           |
| :-------- | :------- | :------------------------------------ |
| `unit_id` | **Yes**  | Unique identifier for the sales rep    |

**Function:** 
Returns detailed performance analysis and feedback for the specified sales representative.

**Example Request:**
```http
GET /api/top_unit?unit_id=10
```
**Response (Postman)**:
![Testing of 1st endpoint](https://github.com/komal-akhlaq/Sales-Team-Performance-Analysis-Using-LLM/blob/main/1.png)

### 2. Best Historical Units

**Endpoint:** 
`/api/unit_price_history`

**Method:** 
`GET`

**Parameters:** 

| Parameter | Required | Description                           |
| :-------- | :------- | :------------------------------------ |
| `unit_type` | **Optional**  | Type of unit to filter by    |

**Function:** 
Finds units with the biggest price decreases for the specified type.

**Example Request:**
```http
GET /api/unit_price_history?unit_type=1%20Bed
```
**Response (Postman)**:
![Testing of 2nd endpoint](https://github.com/komal-akhlaq/Sales-Team-Performance-Analysis-Using-LLM/blob/main/2.png)

### 3. Best Building Deals

**Endpoint:** 
`/api/building_deals`

**Method:** 
`GET`

**Parameters:** 

| Parameter | Required | Description                           |
| :-------- | :------- | :------------------------------------ |
| `neighborhood` | **Optional**  | Specific neighborhood to filter by    |
| `unit_type` | **Optional**  | Type of unit to filter by    |

**Function:** 
Finds the best building deals in the specified neighborhood or unit type.

**Example Request:**
```http
GET /api/building_deals?neighborhood=South%20Loop
```
**Response (Postman)**:
![Testing of 3rd endpoint](https://github.com/komal-akhlaq/Sales-Team-Performance-Analysis-Using-LLM/blob/main/3.png)

## Author

- [@Komal Akhlaq](https://www.github.com/komal-akhlaq)

