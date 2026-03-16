def get_weather(city: str) -> str:
    return f"{city}: 72°F and sunny"


def react_agent(question: str) -> str:
    thought_1 = "Need external weather data."
    action = "get_weather('Austin')"
    observation = get_weather("Austin")
    thought_2 = "Now I can answer with the observation."
    final = f"The current weather is {observation}."
    return (
        f"Thought: {thought_1}\n"
        f"Action: {action}\n"
        f"Observation: {observation}\n"
        f"Thought: {thought_2}\n"
        f"Final Answer: {final}"
    )


def main():
    print("\nSeason 1 / Ep 02 - Level 2 ReAct")
    print(react_agent("Do I need a jacket in Austin today?"))


if __name__ == "__main__":
    main()
