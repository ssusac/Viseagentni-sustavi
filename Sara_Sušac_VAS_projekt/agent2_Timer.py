# agent2_Timer.py
import random

import spade
import time
from common import check_answer, measure_time
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class TimerAgent(spade.agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)

    class TimerBehaviour(OneShotBehaviour):
        async def run(self):
            while True:
                message = await self.receive(timeout=100)

                if message:
                    if message.metadata.get("ontology") == "symbol":
                        symbol = message.body.split(" ")[0]
                        duration = message.body.split(" ")[1]

                    if message.metadata.get("ontology") == "break":
                        break

                while True:
                    symbols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
                    test = random.choice(symbols)

                    print(test)

                    if test == symbol:
                        start_time = time.time()

                    user_input = input("Pritisnite 'y' kada vidite ispravan simbol ili 'n' ako je simbol neispravan: ")

                    if user_input == 'y' and check_answer(test, symbol):
                        elapsed_time = measure_time(start_time)
                        if elapsed_time <= float(duration):
                            await self.send_result_to_agent1(elapsed_time, 1)  # 1 oznacava da je tocno odgovorio
                            break

                        elif elapsed_time > float(duration):
                            await self.send_result_to_agent1(elapsed_time, 0)  # 0 oznacava da je krivo odgovorio
                            break

                    elif user_input == 'y' and not check_answer(test, symbol):
                        await self.send_result_to_agent1(0, 0)  # 0 oznacava da je krivo odgovorio
                        break

                    elif user_input == 'n' and test == symbol:
                        await self.send_result_to_agent1(0, 0)  # 0 oznacava da je krivo odgovorio
                        break

                    elif user_input == 'n':
                        continue

                    else:
                        await self.send_result_to_agent1(0, 0)  # 0 oznacava da je krivo odgovorio
                        break

            await self.agent.stop()

        async def send_result_to_agent1(self, elapsed_time, flag):
            msg = Message(to="agent1@laptop-rfc8bfqq")
            msg.set_metadata("ontology", "result")
            msg.body = str(elapsed_time) + " " + str(flag)
            await self.send(msg)

    async def setup(self):
        print("Agent 2 started")
        self.add_behaviour(self.TimerBehaviour())
