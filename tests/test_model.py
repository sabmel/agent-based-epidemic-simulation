import unittest
from model.agents import PersonAgent
from model.model import EpidemicModel

class TestPersonAgent(unittest.TestCase):
    def test_initial_state(self):
        model = EpidemicModel(10, 0, 0.1, 0.1)
        agent = PersonAgent(1, model)
        self.assertEqual(agent.state, "Susceptible")

class TestStateTransitions(unittest.TestCase):
    def test_infection(self):
        # Initialize the model with 2 agents
        model = EpidemicModel(num_agents=2, initial_infected=0, transmission_prob=1.0, recovery_prob=0)

        # Access agents from the model
        agent1 = model.schedule.agents[0]
        agent2 = model.schedule.agents[1]

        # Set their states
        agent1.state = "Infected"
        agent2.state = "Susceptible"

        # Ensure they are neighbors
        if not model.grid.G.has_edge(agent1.pos, agent2.pos):
            model.grid.G.add_edge(agent1.pos, agent2.pos)

        # Perform the agent's step
        agent1.step()

        # Assert that the second agent is now infected
        self.assertEqual(agent2.state, "Infected")

    def test_recovery(self):
        # Initialize the model with 1 agent
        model = EpidemicModel(num_agents=1, initial_infected=0, transmission_prob=0, recovery_prob=1.0)

        # Access the agent from the model
        agent = model.schedule.agents[0]
        agent.state = "Infected"

        # Perform the agent's step
        agent.step()

        # Assert that the agent has recovered
        self.assertEqual(agent.state, "Recovered")