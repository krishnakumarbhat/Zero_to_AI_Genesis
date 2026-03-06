def get_weather(city: str) -> str:
    return f"Weather in {city}: 72°F and sunny"


def calculate_shipping(weight: float) -> float:
    return round(weight * 1.5, 2)


def route_query(user_query: str) -> str:
    q = user_query.lower()
    if "weather" in q:
        return get_weather("San Francisco")
    if "shipping" in q:
        return f"Shipping cost: ${calculate_shipping(12.0)}"
    return "No matching tool found."


def main():
    print("\nSeason 1 / Ep 01 - Level 1 Tool Router")
    print(route_query("What is the weather today?"))
    print(route_query("Calculate shipping for weight 12"))


if __name__ == "__main__":
    main()
