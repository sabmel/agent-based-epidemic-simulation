from mesa import Model
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
import networkx as nx
from mesa.datacollection import DataCollector

from .agents import PersonAgent

class EpidemicModel(Model):
    def __init__(self, num_agents, initial_infected, transmission_prob, recovery_prob, vaccination_rate=0.1):
        self.num_agents = num_agents
        self.transmission_prob = transmission_prob
        self.recovery_prob = recovery_prob
        self.schedule = RandomActivation(self)
        self.G = nx.erdos_renyi_graph(n=num_agents, p=0.1)
        self.grid = NetworkGrid(self.G)
        self.running = True
        self.datacollector = DataCollector(
            {
                "Susceptible": lambda m: self.count_state(m, "Susceptible"),
                "Infected": lambda m: self.count_state(m, "Infected"),
                "Recovered": lambda m: self.count_state(m, "Recovered"),
            }
        )

        # Create agents
        for i in range(self.num_agents):
            agent = PersonAgent(i, self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, i)

        # Infect initial agents
        infected_agents = self.random.sample(self.schedule.agents, initial_infected)
        for agent in infected_agents:
            agent.state = "Infected"

        vaccinated_agents = self.random.sample(self.schedule.agents, int(self.num_agents * vaccination_rate))
        for agent in vaccinated_agents:
            agent.state = "Recovered"  # Assume Recovered agents are immune

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    @staticmethod
    def count_state(model, state):
        return sum([1 for agent in model.schedule.agents if agent.state == state])
