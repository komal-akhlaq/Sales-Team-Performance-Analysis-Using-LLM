import os
import pandas as pd
import json
import openai
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime

# Function to load data from Excel file containing multiple sheets
def load_data(file_path):
    try:
        df = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')  # Load all sheets
        print("Excel file loaded successfully")
        return df
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None

# Load the data from the Excel file
data = load_data('data/data.xlsx')
if data is None:
    raise Exception("Failed to load the data. Ensure the file path is correct and the file is a valid Excel file.")

# Print the columns of each sheet for debugging
for sheet_name, df in data.items():
    print(f"Columns in {sheet_name}: {df.columns.tolist()}")

# OpenAI API key setup
openai.api_key = os.getenv('OPENAI_API_KEY', '<ur_API_Key')
print(f"OpenAI API Key: {openai.api_key[:4]}****{openai.api_key[-4:]}")

def analyze_data_with_llm(prompt):
    try:
        print(f"Prompt: {prompt}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a highly trained AI capable of understanding complex topics and providing insights."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return f"Error processing the request: {str(e)}"

# Utility function to convert Timestamp and datetime objects to string
def convert_dates_to_strings(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (pd.Timestamp, datetime)):
                data[key] = value.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(data, list):
        for item in data:
            convert_dates_to_strings(item)
    return data

# FastAPI setup
app = FastAPI()

class SalesData(BaseModel):
    unit_id: str

@app.get("/")
async def root():
    return {"message": "Welcome to the Sales Team Performance Analysis API"}

@app.get("/api/top_unit")
async def get_top_unit(unit_id: str):
    unit_table = data['unit_table']
    
    # Debug: Log the unit IDs in the unit_table
    print("Available unit IDs in unit_table:", unit_table['id'].values)

    try:
        unit_id_int = int(unit_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid unit_id format. Must be an integer.")

    if unit_id_int not in unit_table['id'].values:
        raise HTTPException(status_code=404, detail="Unit not found")

    unit_info = unit_table[unit_table['id'] == unit_id_int].to_dict(orient='records')[0]
    unit_info = convert_dates_to_strings(unit_info)
    prompt = f"Provide detailed performance analysis for sales representative {unit_id}. Here is the unit information: {json.dumps(unit_info)}."
    insights = analyze_data_with_llm(prompt)

    # Format the insights in a user-friendly and fancy way
    formatted_insights = f"""
    <h2>Performance Analysis for Sales Representative {unit_id}</h2>
    <h3>Unit Details:</h3>
    <ul>
        <li><strong>Building ID:</strong> {unit_info.get('building_id')}</li>
        <li><strong>Floor Name:</strong> {unit_info.get('floorname')}</li>
        <li><strong>Unit Number:</strong> {unit_info.get('unit')}</li>
        <li><strong>Number of Bedrooms:</strong> {unit_info.get('beds')}</li>
        <li><strong>Number of Bathrooms:</strong> {unit_info.get('baths')}</li>
        <li><strong>Square Footage:</strong> {unit_info.get('sqft')}</li>
        <li><strong>Price:</strong> ${unit_info.get('price')}</li>
        <li><strong>Available Date:</strong> {unit_info.get('available date', 'Not Available')}</li>
    </ul>
    <h3>Key Performance Metrics:</h3>
    <ul>
        <li><strong>Listing Prospects:</strong> Actively seek out potential buyers or renters for this unit considering its unique features like a studio layout, 1 bathroom, and its price point.</li>
        <li><strong>Conversion Rate:</strong> Assess the conversion rate of prospects into actual buyers or renters for this unit. If the conversion rate is low, it may be necessary to review the selling approach or adjust pricing strategies.</li>
        <li><strong>Average Days on Market:</strong> Determine how long the unit has been on the market. If it has been available for an extended period, it may be worth reassessing marketing strategies or pricing.</li>
        <li><strong>Competitive Analysis:</strong> Compare the pricing and features of this unit with similar units in the area to ensure it remains competitive in the market.</li>
    </ul>
    <h3>Actionable Insights:</h3>
    <ul>
        <li><strong>Marketing Strategies:</strong> Evaluate the effectiveness of current marketing efforts for this unit. Consider implementing targeted marketing campaigns to reach potential buyers or renters.</li>
        <li><strong>Price Adjustment:</strong> If the unit has been on the market for a while without much interest, it may be beneficial to consider adjusting the price to attract more buyers.</li>
        <li><strong>Customer Feedback:</strong> Gather feedback from potential clients who viewed the unit to understand any common concerns or objections that can be addressed to improve its market appeal.</li>
    </ul>
    <h3>Performance Improvement:</h3>
    <ul>
        <li>Encourage sales representative {unit_id} to actively engage with potential clients, provide comprehensive information about the unit, and highlight its unique selling points to increase interest and drive sales.</li>
        <li>Regularly review and adjust sales strategies based on market feedback and performance data to optimize sales outcomes for the unit.</li>
    </ul>
    """

    return HTMLResponse(content=formatted_insights)
@app.get("/api/unit_price_history", response_class=HTMLResponse)
async def get_unit_price_history(unit_type: str = Query(None)):
    try:
        history_table = data['history_table']
        unit_table = data['unit_table']
        print("History table columns:", history_table.columns)
        print("Unit table columns:", unit_table.columns)

        # Merge history table with unit table to get unit details
        merged_data = pd.merge(history_table, unit_table, left_on='unit_id', right_on='id', suffixes=('_history', '_unit'))

        # Filter by unit type if provided
        if unit_type:
            merged_data = merged_data[merged_data['unit'].str.contains(unit_type, case=False, na=False)]

        # Calculate price changes
        merged_data['price_change'] = merged_data.groupby('unit_id')['price_history'].diff().fillna(0)

        # Filter out rows where there is no downward change
        merged_data = merged_data[merged_data['price_change'] < 0]

        # Find units with the biggest price changes downwards
        largest_drops = merged_data.sort_values(by='price_change',ascending=False).tail(5).to_dict(orient='records')
        largest_drops = convert_dates_to_strings(largest_drops)

        # convering to positive
        # largest_drops['price_change'] = largest_drops['price_change'].astype(int).apply(lambda x: x*-1)

        # Format the response
        insights_html = "<h2>Units with the Biggest Price Changes Downwards</h2>"
        for unit in largest_drops:
            unit_info = json.dumps(unit, indent=2)
            prompt = f"Based on the following unit details, provide insights and explain why these units have significant price changes downwards:\n{unit_info}"
            llm_insight = analyze_data_with_llm(prompt)
            insights_html += f"""
            <h3>Unit ID: {unit.get('unit_id')}</h3>
            <ul>
                <li><strong>Price Change:</strong> {unit.get('price_change')}</li>
                <li><strong>Building ID:</strong> {unit.get('building_id')}</li>
                <li><strong>Floor Name:</strong> {unit.get('floorname')}</li>
                <li><strong>Unit Number:</strong> {unit.get('unit')}</li>
                <li><strong>Number of Bedrooms:</strong> {unit.get('beds')}</li>
                <li><strong>Number of Bathrooms:</strong> {unit.get('baths')}</li>
                <li><strong>Square Footage:</strong> {unit.get('sqft')}</li>
                <li><strong>Current Price:</strong> ${unit.get('price')}</li>
                <li><strong>Available Date:</strong> {unit.get('available date', 'Not Available')}</li>
            </ul>
            <h4>LLM Insights</h4>
            <p>{llm_insight}</p>
            """
        
        return HTMLResponse(content=insights_html)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Column not found: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

def convert_dates_to_strings(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (pd.Timestamp, datetime)):
                data[key] = value.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(data, list):
        for item in data:
            convert_dates_to_strings(item)
    return data

def analyze_data_with_llm(prompt):
    try:
        print(f"Prompt: {prompt}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a highly trained AI capable of understanding complex topics and providing insights."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return f"Error processing the request: {str(e)}"


@app.get("/api/building_deals", response_class=HTMLResponse)
async def get_building_deals(neighborhood: str = Query(None), unit_type: str = Query(None)):
    try:
        building_table = data['building_table']
        unit_table = data['unit_table']

        # Print columns for debugging
        print("Building table columns:", building_table.columns)
        print("Unit table columns:", unit_table.columns)

        # Merge building and unit tables to find deals
        merged_data = pd.merge(unit_table, building_table, left_on='building_id', right_on='id', suffixes=('_unit', '_building'))

        # Debug merged_data columns
        print("Merged table columns:", merged_data.columns)

        # Ensure 'id' is present in the DataFrame
        if 'id_unit' not in merged_data.columns:
            raise ValueError("'id' column is missing from the merged DataFrame")

        # Calculate price per square foot for each unit
        merged_data['price_per_sqft'] = merged_data['price'] / merged_data['sqft']

        # Filter out units with price 0 and those not meeting basic criteria
        filtered_units = merged_data[
            (merged_data['price'] > 0) &
            (merged_data['sqft'] > 500) &  # Minimum area
            (merged_data['washer dryer'] == 'Yes') &  # Basic amenities
            (merged_data['parking'] == 'Yes') &  # Basic amenities
            (merged_data['balcony'] == 'Yes')  # Basic amenities
        ]

        # Filter by neighborhood if provided
        if neighborhood:
            filtered_units = filtered_units[filtered_units['neighborhood'].str.contains(neighborhood, case=False, na=False)]

        # Filter by unit type if provided
        if unit_type:
            filtered_units = filtered_units[filtered_units['unit'].str.contains(unit_type, case=False, na=False)]

        # Handle missing 'available_date' if it doesn't exist
        if 'available_date' in filtered_units.columns:
            # Filter available units
            available_units = filtered_units[filtered_units['available_date'].notna()]
        else:
            available_units = filtered_units

        # Select the latest records for each unit to avoid duplicates
        available_units = available_units.sort_values(by='id_unit').drop_duplicates(subset=['unit'], keep='last')

        # Find the best deals based on price per square foot
        best_deals = available_units.sort_values(by='price_per_sqft').head(5).to_dict(orient='records')
        best_deals = convert_dates_to_strings(best_deals)

        # Group best deals by building
        grouped_deals = {}
        for deal in best_deals:
            building_name = deal.get('name')
            if building_name not in grouped_deals:
                grouped_deals[building_name] = {
                    'address': deal.get('address'),
                    'neighborhood': deal.get('neighborhood'),
                    'description': deal.get('description'),
                    'units': []
                }
            grouped_deals[building_name]['units'].append(deal)

        # Generate insights using LLM for each unit
        insights_html = "<h2>Best Building Deals</h2>"
        for building, details in grouped_deals.items():
            insights_html += f"<h3>{building}</h3>"
            insights_html += f"<p><strong>Address:</strong> {details['address']}</p>"
            insights_html += f"<p><strong>Neighborhood:</strong> {details['neighborhood']}</p>"
            insights_html += f"<p><strong>Description:</strong> {details['description']}</p>"
            for unit in details['units']:
                prompt = f"Based on the following building deal, provide insights and explain why this is considered a best deal:\n{json.dumps(unit, indent=2)}"
                llm_insights = analyze_data_with_llm(prompt)
                
                insights_html += f"<p><strong>Unit ID:</strong> {unit.get('id_unit')}<br>"
                insights_html += f"<strong>Unit:</strong> {unit.get('unit')}<br>"
                insights_html += f"<strong>Beds:</strong> {unit.get('beds')}<br>"
                insights_html += f"<strong>Baths:</strong> {unit.get('baths')}<br>"
                insights_html += f"<strong>Square Feet:</strong> {unit.get('sqft')}<br>"
                insights_html += f"<strong>Price:</strong> {unit.get('price')}<br>"
                insights_html += f"<strong>Price per Square Foot:</strong> {unit.get('price_per_sqft')}</p>"
                insights_html += f"<p><strong>Amenities:</strong><br>"
                insights_html += f"Parking: {unit.get('parking')}<br>"
                insights_html += f"Washer Dryer: {unit.get('washer dryer')}<br>"
                insights_html += f"Balcony: {unit.get('balcony')}<br>"
                insights_html += f"Pet Policy: {unit.get('pet policy')}</p>"
                insights_html += f"<h3>LLM Insights</h3><p>{llm_insights}</p>"
                insights_html += "<hr>"

        # Add a note about excluded units
        excluded_units_count = len(merged_data) - len(filtered_units)
        if excluded_units_count > 0:
            insights_html += f"<p><em>Note: {excluded_units_count} units with a price of 0 were excluded from this analysis.</em></p>"

        return insights_html
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
