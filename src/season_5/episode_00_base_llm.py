def base_llm(prompt: str) -> str:
    return (
        "[Mock LLM Output]\n"
        "You asked: " + prompt + "\n"
        "This demonstrates Level 0 prompt engineering without external tools."
    )


def main():
    prompt = "Summarize the remote work policy in 3 bullet points."
    print("\nSeason 1 / Ep 00 - Level 0 Base LLM")
    print(base_llm(prompt))


if __name__ == "__main__":
    main()
