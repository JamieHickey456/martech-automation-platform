import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta


def generate_customer_events(num_customers=5000, months=6):

    customers = []
    events = []

    acquisition_channels = ["Organic", "Paid Ads", "Referral", "Email"]
    regions = ["North America", "Europe", "APAC"]

    base_date = datetime(2024, 1, 1)

    for i in range(num_customers):
        customer_id = f"CUST_{i+1}"
        signup_date = base_date + timedelta(days=random.randint(0, 30))

        customers.append({
            "customer_id": customer_id,
            "region": random.choice(regions),
            "acquisition_channel": random.choice(acquisition_channels),
            "signup_date": signup_date
        })

        persona = np.random.choice(
            ["power", "normal", "at_risk", "dormant"],
            p=[0.12, 0.63, 0.20, 0.05]
        )

        for month in range(months):
            event_date = signup_date + timedelta(days=30 * month)

            if persona == "power":
                login_count = np.random.poisson(18)
                purchases = np.random.binomial(3, 0.55)
            elif persona == "normal":
                login_count = np.random.poisson(10)
                purchases = np.random.binomial(2, 0.30)
            elif persona == "at_risk":
                login_count = np.random.poisson(4)
                purchases = np.random.binomial(1, 0.10)
            else:
                login_count = np.random.poisson(1)
                purchases = np.random.binomial(1, 0.03)

            spend = purchases * random.uniform(40, 220)

            events.append({
                "customer_id": customer_id,
                "month_index": month,
                "event_date": event_date,
                "logins": int(login_count),
                "purchases": int(purchases),
                "spend": float(spend)
            })

    return pd.DataFrame(customers), pd.DataFrame(events)