from __future__ import annotations

from jarvis.coordinator import JARVISCoordinator


if __name__ == "__main__":
    coordinator = JARVISCoordinator()
    print("JARVIS coordinator ready.")
    print(coordinator.handle("analyze the repository and plan the next sprint"))
