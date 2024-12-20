from model.model import EpidemicModel
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

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

# Retrieve data
data = model.datacollector.get_model_vars_dataframe()
data.reset_index(inplace=True)
data_melted = data.melt(id_vars=["index"], value_vars=["Susceptible", "Infected", "Recovered"],
                        var_name="State", value_name="Count")

# Seaborn Plot
sns.set(style="darkgrid")
plt.figure(figsize=(12, 6))
sns.lineplot(data=data_melted, x="index", y="Count", hue="State", marker="o")
plt.xlabel("Time Step")
plt.ylabel("Number of Agents")
plt.title("Epidemic Simulation Over Time")
plt.legend(title="Agent State")
plt.tight_layout()
plt.show()
