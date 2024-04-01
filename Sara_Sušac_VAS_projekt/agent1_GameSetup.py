# agent1_GameSetup.py
import spade
from common import start_new_level
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class GameSetupAgent(spade.agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)

    class GameSetupBehaviour(OneShotBehaviour):
        async def run(self):
            while True:
                level = 1
                symbol, duration = start_new_level(level)
                while True:
                    print(f"Level {level}: Pripremite se, slovo koje trebate pritisnuti glasi: {symbol}")
                    await self.send_symbol_to_agent2(symbol, duration=duration)

                    message = await self.receive(timeout=100)
                    if message:
                        if message.metadata.get("ontology") == "result":
                            elapsed_time = float(message.body.split(" ")[0])
                            flag = int(message.body.split(" ")[1])

                            if flag == 1:
                                print(f"Točno! Vaše vrijeme je: {elapsed_time:.2f} sekundi.")
                                level += 1
                                if level == 6:
                                    print(f"\nČestitamo!!! Pobijedili ste :)")
                                    await self.send_break_to_agent2()
                                    break
                                else:
                                    print("Prelazite na novi level.\n")

                            elif flag == 0:
                                print(f"Krivo ste odgovorili ili Vam je trebalo previše vremena. Vraćate se na prvi level.\n")
                                level = 1

                    symbol, duration = start_new_level(level)

                break
            await self.agent.stop()

        async def send_symbol_to_agent2(self, symbol, duration):
            msg = Message(to="agent2@laptop-rfc8bfqq")
            msg.set_metadata("ontology", "symbol")
            msg.body = symbol + " " + str(duration)
            await self.send(msg)

        async def send_break_to_agent2(self):
            msg = Message(to="agent2@laptop-rfc8bfqq")
            msg.set_metadata("ontology", "break")
            await self.send(msg)

    async def setup(self):
        print("Agent 1 started")
        self.add_behaviour(self.GameSetupBehaviour())
