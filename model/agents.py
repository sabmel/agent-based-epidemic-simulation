from mesa import Agent

class PersonAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = "Susceptible"  # Possible states: Susceptible, Infected, Recovered

    def step(self):
        if self.state == "Infected":
            # Attempt to infect neighbors
            neighbors = self.model.grid.get_neighbors(self.pos, include_center=False)
            for neighbor in neighbors:
                if neighbor.state == "Susceptible":
                    if self.random.random() < self.model.transmission_prob:
                        neighbor.state = "Infected"

            # Attempt to recover
            if self.random.random() < self.model.recovery_prob:
                self.state = "Recovered"

