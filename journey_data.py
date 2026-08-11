from portfolio_store import load_content


def get_journey_steps():
    return load_content().get("journey", [])
