from agent import build_agent_executor


def main():
    print("=" * 50)
    print(" Order Assistant  (type 'exit' to quit)")
    print("=" * 50)

    try:
        executor = build_agent_executor()
    except RuntimeError as exc:
        print(f"\nSetup error: {exc}")
        return

    chat_history = []

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not user_input:
            continue

        result = executor.invoke({"input": user_input, "chat_history": chat_history})
        answer = result["output"]
        print(f"\nAssistant: {answer}")

        chat_history.append(("human", user_input))
        chat_history.append(("ai", answer))


if __name__ == "__main__":
    main()
