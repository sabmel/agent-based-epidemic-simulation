
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
import networkx as nx

from .agents import PersonAgent
from mesa.datacollection import DataCollector

class EpidemicModel(Model):
    def __init__(self, num_agents, initial_infected, transmission_prob, recovery_prob,
                 vaccination_rate=0.0, network_prob=0.1):
        self.num_agents = num_agents
        self.initial_infected = initial_infected
        self.transmission_prob = transmission_prob
        self.recovery_prob = recovery_prob
        self.vaccination_rate = vaccination_rate
        self.schedule = RandomActivation(self)
        self.G = nx.erdos_renyi_graph(n=num_agents, p=network_prob)
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
        for i, node in enumerate(self.G.nodes()):
            agent = PersonAgent(i, self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, node)

        # Infect initial agents
        infected_agents = self.random.sample(self.schedule.agents, self.initial_infected)
        for agent in infected_agents:
            agent.state = "Infected"

        # Vaccinate agents
        num_vaccinated = int(self.num_agents * self.vaccination_rate)
        susceptible_agents = [agent for agent in self.schedule.agents if agent.state == "Susceptible"]
        vaccinated_agents = self.random.sample(susceptible_agents, num_vaccinated)
        for agent in vaccinated_agents:
            agent.state = "Recovered"  # Vaccinated agents are immune

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

    @staticmethod
    def count_state(model, state):
        return sum([1 for agent in model.schedule.agents if agent.state == state])
