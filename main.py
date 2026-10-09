from jarvis.coordinator import JARVISCoordinator
from jarvis.session import SessionManager


def main() -> None:
    coordinator = JARVISCoordinator()
    session = SessionManager()
    print("JARVIS Agent System ready.")
    print(f"Session ID: {session.current_session_id}")
    print("Type 'exit' to quit, 'sessions' to list history, 'agents' to list all agents.\n")

    while True:
        try:
            command = input("JARVIS> ")
        except EOFError:
            print("\nSession closed.")
            break

        if not command.strip():
            continue

        cmd = command.strip().lower()

        if cmd in {"exit", "quit", "bye"}:
            session.close_session()
            print("Goodbye. Session saved.")
            break

        if cmd == "sessions":
            sessions = SessionManager.list_sessions()
            if not sessions:
                print("No previous sessions found.")
            else:
                print(f"\n{len(sessions)} session(s) found:\n")
                for s in sessions:
                    status_indicator = "●" if s["status"] == "active" else "○"
                    print(
                        f"  {status_indicator} {s['session_id'][:8]}... | {s['created_at']} | {s['command_count']} commands | {s['status']}"
                    )
            print()
            continue

        if cmd == "agents":
            agents = coordinator.list_agents()
            print(f"\nTotal agents: {len(agents)}\n")
            for agent in agents[:15]:
                print(f"  [{agent['id']}] {agent['name']} - {agent['role']} ({agent['specialization']})")
            if len(agents) > 15:
                print(f"  ... and {len(agents) - 15} more agents")
            print()
            continue

        if cmd == "dashboard":
            from jarvis.dashboard import run_dashboard
            run_dashboard()
            break

        result = coordinator.handle(command)
        print(result)
        print()

        # Parse the response to extract agent names for logging
        agent_names = []
        for line in result.split("\n"):
            if line.startswith("[JARVIS"):
                agent_name = line.split("]")[0].strip("[")
                agent_names.append(agent_name)

        parsed = coordinator.router.parse_command(command)
        session.log_command(
            command=command,
            intent=parsed["intent"],
            selected_agents=agent_names,
            response=result,
        )


if __name__ == "__main__":
    main()
