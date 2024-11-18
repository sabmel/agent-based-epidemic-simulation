import unittest
from model.agents import PersonAgent
from model.model import EpidemicModel
import networkx as nx

class TestPersonAgent(unittest.TestCase):
    def setUp(self):
        self.model = EpidemicModel(
            num_agents=10,
            initial_infected=0,
            transmission_prob=0.1,
            recovery_prob=0.05,
            vaccination_rate=0.0,
            network_prob=0.1
        )
        self.agent = PersonAgent(1, self.model)
        self.agent.state = "Susceptible"

    def test_initial_state(self):
        self.assertEqual(self.agent.state, "Susceptible", "Agent should start as Susceptible")

    def test_infection(self):
        # Mock an infected neighbor
        infected_agent = PersonAgent(2, self.model)
        infected_agent.state = "Infected"
        # Place both agents in the same node for testing
        self.model.grid.place_agent(self.agent, 0)
        self.model.grid.place_agent(infected_agent, 0)
        # Force interaction
        infected_agent.model.transmission_prob = 1.0  # Ensure transmission
        infected_agent.step()
        self.assertEqual(self.agent.state, "Infected", "Agent should become Infected after contact with an Infected neighbor")

    def test_recovery(self):
        self.agent.state = "Infected"
        # Ensure recovery
        self.agent.model.recovery_prob = 1.0
        self.agent.step()
        self.assertEqual(self.agent.state, "Recovered", "Agent should become Recovered after recovery")

class TestEpidemicModel(unittest.TestCase):
    def test_model_initialization(self):
        model = EpidemicModel(
            num_agents=100,
            initial_infected=5,
            transmission_prob=0.1,
            recovery_prob=0.05,
            vaccination_rate=0.1,
            network_prob=0.1
        )
        self.assertEqual(len(model.schedule.agents), 100, "Model should have 100 agents")
        infected_agents = [agent for agent in model.schedule.agents if agent.state == "Infected"]
        self.assertEqual(len(infected_agents), 5, "Model should have 5 initially infected agents")
        vaccinated_agents = [agent for agent in model.schedule.agents if agent.state == "Recovered"]
        expected_vaccinated = int(100 * 0.1)
        self.assertEqual(len(vaccinated_agents), expected_vaccinated, "Model should have correct number of vaccinated agents")

    def test_data_collection(self):
        model = EpidemicModel(
            num_agents=10,
            initial_infected=2,
            transmission_prob=0.0,  # Prevent spread
            recovery_prob=0.0,      # Prevent recovery
            vaccination_rate=0.0,
            network_prob=0.1
        )
        model.step()
        data = model.datacollector.get_model_vars_dataframe()
        self.assertEqual(data['Susceptible'].iloc[0], 8, "There should be 8 susceptible agents")
        self.assertEqual(data['Infected'].iloc[0], 2, "There should be 2 infected agents")
        self.assertEqual(data['Recovered'].iloc[0], 0, "There should be 0 recovered agents")

    def test_social_distancing(self):
        # Test that reducing network_prob reduces average node degree
        model_high = EpidemicModel(
            num_agents=100,
            initial_infected=0,
            transmission_prob=0.0,
            recovery_prob=0.0,
            vaccination_rate=0.0,
            network_prob=0.1
        )
        model_low = EpidemicModel(
            num_agents=100,
            initial_infected=0,
            transmission_prob=0.0,
            recovery_prob=0.0,
            vaccination_rate=0.0,
            network_prob=0.05
        )
        avg_degree_high = sum(dict(nx.degree(model_high.G)).values()) / 100
        avg_degree_low = sum(dict(nx.degree(model_low.G)).values()) / 100
        self.assertTrue(avg_degree_low < avg_degree_high, "Average degree should be lower with reduced network probability")

    def test_vaccination_effectiveness(self):
        model = EpidemicModel(
            num_agents=10,
            initial_infected=1,
            transmission_prob=1.0,  # Ensure transmission
            recovery_prob=0.0,
            vaccination_rate=0.5,
            network_prob=1.0  # Fully connected
        )
        model.step()
        vaccinated_agents = [agent for agent in model.schedule.agents if agent.state == "Recovered"]
        infected_agents = [agent for agent in model.schedule.agents if agent.state == "Infected"]
        # Vaccinated agents should remain Recovered
        for agent in vaccinated_agents:
            self.assertEqual(agent.state, "Recovered", "Vaccinated agent should remain Recovered")
        # Only non-vaccinated susceptible agents should become Infected
        self.assertLessEqual(len(infected_agents), 4, "At most 4 agents should be infected")

if __name__ == '__main__':
    unittest.main()