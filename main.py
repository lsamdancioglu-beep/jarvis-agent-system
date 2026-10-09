from jarvis.coordinator import JARVISCoordinator


def main() -> None:
    coordinator = JARVISCoordinator()
    print("JARVIS Agent System ready.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            command = input("JARVIS> ")
        except EOFError:
            print("\nSession closed.")
            break

        if not command.strip():
            continue

        if command.strip().lower() in {"exit", "quit", "bye"}:
            print("Goodbye.")
            break

        result = coordinator.handle(command)
        print(result)
        print()


if __name__ == "__main__":
    main()
