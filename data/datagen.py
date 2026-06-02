import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_multi_year_dataset(num_rows=1000):
    np.random.seed(101)
    random.seed(101)

    # Messy, uncleaned structural variables
    categories = ['electronics', 'Electronics', 'furniture', 'Furniture', 'HOME APPLIANCES', 'Home Appliances', 'nan', 'None']
    years = [2022, 2023, 2024, 2025, 2026]
    
    # Pre-generate a pool of unique Order IDs to allow multi-item orders (same ID across rows)
    # 1000 rows will map to roughly ~750 unique orders, creating realistic transactional velocity
    order_id_pool = [f"ORD-{year}{random.randint(10000, 99999)}" for year in years for _ in range(150)]
    
    data = {
        'Order ID': [random.choice(order_id_pool) for _ in range(num_rows)], # Injected true Order ID tracking vector
        'Product Category': [random.choice(categories) for _ in range(num_rows)],
        'Profit': [],
        'Revenue': [],
        'Cost ': [], # Intentionally included trailing blank space in header string 
        'Date': []
    }

    for i in range(num_rows):
        # 1. Scaling financial tracking variables across random bounds
        base_revenue = random.randint(15000, 300000)
        base_cost = int(base_revenue * random.uniform(0.65, 0.95))
        base_profit = base_revenue - base_cost

        # Introduce a 5% chance of negative margins or data logging adjustments
        if random.random() < 0.05:
            base_profit = -abs(base_profit)

        # 2. Textual Pollution Layer: Inject dollar markers and string commas randomly
        rand_val = random.random()
        if rand_val < 0.35:
            revenue_str = f"${base_revenue:,}"
            profit_str = f"${base_profit:,}"
            cost_str = f"{base_cost:,}"
        elif rand_val < 0.70:
            revenue_str = f"{base_revenue}"
            profit_str = f"{base_profit}"
            cost_str = f"{base_cost}"
        else:
            revenue_str = f"${base_revenue}"
            profit_str = f"{base_profit}"
            cost_str = f"${base_cost:,}"

        # 3. Structural Null Layer: Missing data configurations (approx 5%)
        if random.random() < 0.05:
            profit_str = random.choice(['None', 'nan', 'Null', ''])

        # 4. Multi-Year Chronological Chaos: Pick a year from 2022 to 2026
        target_year = random.choice(years)
        start_day = datetime(target_year, 1, 1)
        random_days_offset = random.randint(0, 364)
        current_date = start_day + timedelta(days=random_days_offset)
        
        # Randomly shuffle date format styles to stress-test pd.to_datetime(format='mixed')
        date_style = random.random()
        if date_style < 0.25:
            date_str = current_date.strftime('%m/%d/%Y')  # e.g., 04/15/2023
        elif date_style < 0.50:
            date_str = current_date.strftime('%Y-%m-%d')  # e.g., 2024-11-23
        elif date_style < 0.75:
            date_str = current_date.strftime('%d-%m-%Y')  # e.g., 02-08-2022
        else:
            date_str = current_date.strftime('%Y/%m/%d')  # e.g., 2026/06/02

        data['Revenue'].append(revenue_str)
        data['Profit'].append(profit_str)
        data['Cost '].append(cost_str)
        data['Date'].append(date_str)

    # Transpile dictionary parameters to DataFrame object instance
    df = pd.DataFrame(data)

    # Final explicit local disk commit
    output_filename = "customer_sales_5years_uncleaned.csv"
    df.to_csv(output_filename, index=False)
    print(f"✨ Successfully compiled '{output_filename}' with Order IDs across parameters (2022-2026)!")

if __name__ == "__main__":
    generate_multi_year_dataset(1000)