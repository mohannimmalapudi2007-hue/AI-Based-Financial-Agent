import os
import sys
import argparse
import pandas as pd

sys.path.insert(
    0,
    os.path.dirname(os.path.abspath(__file__))
)

from data_loader import DataLoader
from profile_lookup import ProfileLookup
from event_lookup import EventLookup
from financial_timeline import FinancialTimeline


DATASET = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "dataset"
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--requests-file",
        default=os.path.join(DATASET, "requests.csv")
    )

    parser.add_argument(
        "--output",
        default=os.path.join(ROOT, "output.csv")
    )

    args = parser.parse_args()

    loader = DataLoader(DATASET)

    requests = pd.read_csv(args.requests_file)
    profiles = loader.load_profiles()
    events = loader.load_events()
    payment_options = loader.load_payment_options().to_dict("records")

    # Load supporting datasets so the application is ready
    # for the complete financial-agent pipeline.
    exchange_rates = loader.load_exchange_rates()
    messages = loader.load_messages()
    images = loader.load_images()

    profile_lookup = ProfileLookup(profiles)
    event_lookup = EventLookup(events)

    # FinancialTimeline currently accepts exchange_rates only.
    # Convert the exchange-rate dataframe into the lookup format
    # expected by FinancialTimeline.
    exchange_rate_lookup = {}

    for _, row in exchange_rates.iterrows():
        key = (
            str(row["rate_date"]),
            str(row["from_currency"]),
            str(row["to_currency"])
        )

        exchange_rate_lookup[key] = float(row["rate"])

    timeline = FinancialTimeline(
    exchange_rates=exchange_rate_lookup,
    messages=messages,
    images=images
   )

    results = []

    for _, request in requests.iterrows():

        user_id = request["user_id"]

        profile = profile_lookup.get_profile(user_id)

        user_events = event_lookup.get_user_events(
            user_id
        ).to_dict("records")

        if profile is None:
            continue

        result = timeline.process_request(
            request=request,
            profile=profile,
            events=user_events,
            payment_options=payment_options
        )

        results.append(result)

    output = pd.DataFrame(results)

    required_columns = [
        "request_id",
        "amount_safe_to_pay",
        "affordability_status",
        "recommended_payment_method",
        "payment_plan",
        "earliest_date_for_full_payment",
        "spending_changes_needed",
        "decision_explanation"
    ]

    output = output[required_columns]

    output.to_csv(
        args.output,
        index=False
    )

    print(f"Generated {len(output)} predictions.")
    print(f"Output: {args.output}")


if __name__ == "__main__":
    main()