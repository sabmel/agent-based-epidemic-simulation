# Assumptions

This document outlines the key assumptions made in the agent-based epidemic simulation model.

## Epidemiological Assumptions

- **Disease Transmission**
  - Transmission occurs through contact between an infected agent and a susceptible agent.
  - The probability of transmission per contact is constant (`transmission_prob`).

- **Recovery**
  - Infected agents have a constant probability of recovery per time step (`recovery_prob`).
  - Recovered agents gain immunity and cannot be reinfected.

- **Vaccination**
  - Vaccinated agents are considered immune from the start (modeled as `Recovered` state).
  - Vaccination is randomly distributed among the population based on `vaccination_rate`.

## Network Assumptions

- **Social Network**
  - Agents are connected via an Erdős-Rényi random graph.
  - The probability of an edge between any two agents is constant (`p` in `nx.erdos_renyi_graph`).

- **Social Distancing**
  - Modeled by decreasing the probability `p`, leading to fewer connections.

## Agent Behavior Assumptions

- **Movement**
  - Agents do not move; they interact with their network neighbors.

- **Contact**
  - All connected agents interact each time step.
  - Contacts are symmetrical; if Agent A interacts with Agent B, the reverse is also true.

## General Assumptions

- **Time Steps**
  - Each simulation step represents a discrete time unit (e.g., one day).

- **Population Homogeneity**
  - All agents have the same probability parameters (no age groups, health statuses).

- **No Births or Deaths**
  - The population size remains constant; agents do not die or reproduce.

- **No External Infections**
  - The only source of infection is through interactions within the modeled population.

## Limitations

- **Simplified Disease Model**
  - Does not account for incubation periods, asymptomatic carriers, or varying infectivity over time.

- **Network Model**
  - Real-world social networks may not be accurately represented by an Erdős-Rényi graph.

- **Lack of Demographics**
  - Does not include demographic factors like age, occupation, or behavior patterns.

