# Model Details

This document provides a detailed explanation of the components and logic used in the agent-based epidemic simulation.

## Overview

The simulation models the spread of a contagious disease within a fixed population using agent-based modeling. Agents represent individuals who can be in one of three states: Susceptible, Infected, or Recovered. Agents interact based on a predefined social network.

## Components

### 1. Agents

#### PersonAgent

- **Attributes**
  - `unique_id`: A unique identifier for the agent.
  - `state`: The current state of the agent (`Susceptible`, `Infected`, `Recovered`).
  - `pos`: The position of the agent in the network graph.

- **Methods**
  - `step()`: Defines the agent's behavior at each time step.

- **Behavior**
  - **Infected Agents**
    - Attempt to infect all susceptible neighbors.
    - Recover with probability `recovery_prob`.
  - **Susceptible Agents**
    - Can become infected if contacted by an infected neighbor.
  - **Recovered Agents**
    - Do nothing; they are immune.

### 2. Environment

- **Network Graph**
  - Modeled using an Erdős-Rényi graph (`nx.erdos_renyi_graph`).
  - Nodes represent agents; edges represent social connections.
  - Edge creation probability `p` determines the network density.

### 3. Model

#### EpidemicModel

- **Attributes**
  - `num_agents`: Total number of agents.
  - `initial_infected`: Number of agents initially infected.
  - `transmission_prob`: Probability of disease transmission per contact.
  - `recovery_prob`: Probability of recovery per time step.
  - `vaccination_rate`: Proportion of agents vaccinated at the start.
  - `schedule`: Scheduler to manage agent activation (`RandomActivation`).
  - `grid`: Network grid representing the social network.
  - `datacollector`: Collects data at each time step.

- **Methods**
  - `__init__()`: Initializes the model with the specified parameters.
  - `step()`: Advances the model by one time step.
  - `count_state()`: Static method to count agents in a given state.

- **Initialization Steps**
  1. **Create Agents**
     - Instantiate `PersonAgent` for each agent.
     - Place agents on nodes in the network graph.
  2. **Set Initial States**
     - Infect a random sample of agents based on `initial_infected`.
     - Vaccinate a random sample of agents based on `vaccination_rate` by setting their state to `Recovered`.

### 4. Data Collection

- **DataCollector**
  - Tracks the number of agents in each state at every time step.
  - Stores data in a pandas DataFrame for analysis and visualization.

## Simulation Flow

1. **Initialization**
   - The model is set up with the specified parameters.
   - Agents are created and assigned initial states.

2. **Time Steps**
   - For each time step up to `max_steps`:
     - The model's `step()` method is called.
     - Each agent executes its `step()` method in random order.
     - Data is collected after each step.

3. **Agent Interactions**
   - Infected agents attempt to infect susceptible neighbors.
   - Recovery is attempted for infected agents.

4. **Termination**
   - The simulation runs for the specified number of time steps.
   - Alternatively, it could be modified to stop when no infected agents remain.

## Customization Options

- **Transmission Probability (`transmission_prob`)**
  - Adjusts how contagious the disease is.

- **Recovery Probability (`recovery_prob`)**
  - Changes the average duration of infection.

- **Vaccination Rate (`vaccination_rate`)**
  - Simulates preemptive immunity in the population.

- **Network Density (`p` in `nx.erdos_renyi_graph`)**
  - Models the level of social connectivity.
  - Lower `p` simulates social distancing.

## Extending the Model

- **Incubation Period**
  - Introduce a `latent` state to model incubation.

- **Asymptomatic Carriers**
  - Add agents who are infected but less likely to transmit.

- **Dynamic Networks**
  - Allow the network graph to change over time.

- **Demographics**
  - Incorporate age, health status, or behavior patterns.

