from model.model import EpidemicModel
import matplotlib.pyplot as plt

# Set model parameters
num_agents = 100
initial_infected = 5
transmission_prob = 0.1
recovery_prob = 0.05
max_steps = 100

# Initialize and run the model
model = EpidemicModel(num_agents, initial_infected, transmission_prob, recovery_prob)
for i in range(max_steps):
    model.step()

# Retrieve and plot data
data = model.datacollector.get_model_vars_dataframe()
data.plot()
plt.xlabel("Time Step")
plt.ylabel("Number of Agents")
plt.title("Epidemic Simulation Over Time")
plt.show()
