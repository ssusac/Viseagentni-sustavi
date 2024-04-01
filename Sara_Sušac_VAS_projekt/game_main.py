import spade
from agent1_GameSetup import GameSetupAgent
from agent2_Timer import TimerAgent


async def main():
    primatelj = GameSetupAgent("agent1@laptop-rfc8bfqq", "tajna")
    posiljatelj = TimerAgent("agent2@laptop-rfc8bfqq", "tajna")

    await posiljatelj.start()
    await primatelj.start()

    await spade.wait_until_finished(primatelj)
    await posiljatelj.stop()
    print("Gotovo")


if __name__ == "__main__":
    spade.run(main())
