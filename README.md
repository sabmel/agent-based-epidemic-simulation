# agent-based-epidemic-simulation
A simulation of infectious disease spread using agent-based modeling with Mesa.

## Overview
This project simulates the spread of a contagious disease within a population using agent-based modeling. It allows for the evaluation of intervention strategies such as vaccination and social distancing to understand their effectiveness in controlling the epidemic.

## Features
* Simulate disease spread among agents in a networked environment
* Customize parameters like transmission probability, recovery probability, and initial infected count
* Implement intervention strategies:
    * Vaccination: A percentage of the population is immune from the start
    * Social Distancing: Modify the contact network to reduce interactions
* Collect and visualize data on the number of susceptible, infected, and recovered agents over time

## Project Structure
agent-based-epidemic-simulation/
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── run.py
├── model/
│   ├── __init__.py
│   ├── agents.py
│   ├── model.py
│   └── server.py
├── data/
└── docs/

## Installation
### Prerequisites
* Python 3.x
* Git (for cloning the repository)

### Clone the Repository
```bash
git clone https://github.com/your_username/agent-based-epidemic-simulation.git
cd agent-based-epidemic-simulation
```

### Set Up Virtual Environment
```bash
python -m venv venv
# On macOS/Linux
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

### Install Requirements
```bash
pip install -r requirements.txt
```

## Usage
### Running the Simulation
Exectute the simulation using:
```bash
python run.py
```
This will run the model with default parameters and display a graph showing the number of susceptible, infected, and recovered agents over time.

### Adjusting Parameters
You can modify simulation parameters directly in run.py:
```python
# run.py

# Set model parameters
num_agents = 100
initial_infected = 5
transmission_prob = 0.1
recovery_prob = 0.05
vaccination_rate = 0.1  # Adjust vaccination rate here
max_steps = 100
```
* num_agents: Total number of agents in the simulation
* initial_infected: Number of agents initially infected
* transmission_prob: Probability of disease transmission upon contact
* recovery_prob: Probability of an infected agent recovering
* vaccination_rate: Proportion of the population vaccinated (immune from start)
* max_steps: Number of time steps to simulate

## Model Explanation
### Agents
* PersonAgent: Represents an individual in the population.
    * States:
        * Susceptible: Healthy and can be infected
        * Infected: Currently infected and can transmit the disease
        * Recovered: Recovered from infection and is immune
### Environment
* Agents are placed on a network graph representing social connections.
* Uses a random Erdős-Rényi graph to model interactions.
### Rules
* Movement: Agents do not move but interact with neighbors in the network.
* Infection:
    * Infected agents attempt to infect susceptible neighbors each time step.
    * Transmission occurs based on the transmission_prob.
* Recovery:
    * Infected agents have a chance to recover each time step based on the recovery_prob.
* Vaccination:
    * A portion of agents are set to Recovered state at initialization based on vaccination_rate.
### Data Collection
* The model tracks the number of agents in each state over time.
* Uses mesa.datacollection.DataCollector for data aggregation.
* Results are plotted using matplotlib.
### Intervention Strategies
#### Vaccinatino
* Implemented by setting a fraction of agents to the Recovered state at the start.
* Adjust the vaccination_rate parameter to simulate different vaccination levels.
#### Social Distancing
* Can be modeled by altering the network graph to reduce the average number of connections.
* Decrease the probability p in the Erdős-Rényi graph nx.erdos_renyi_graph(n=num_agents, p=0.1) to simulate social distancing.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any changes or enhancements.

## Licence
This project is licensed under the MIT License.

## Acknowledgements
* Mesa library for agent-based modeling in Python
* Inspired by epidemiological models and the need to understand infectious disease dynamics

## Documentation

- [Assumptions](docs/assumptions.md)
- [Model Details](docs/model_details.md)
- [Findings](docs/findings.md)