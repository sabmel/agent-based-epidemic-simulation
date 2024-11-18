import matplotlib.pyplot as plt
import pandas as pd
from model.model import EpidemicModel
import os

# Create a directory to save plots if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

def run_simulation(num_agents, initial_infected, transmission_prob, recovery_prob,
                   vaccination_rate, network_prob, max_steps):
    """
    Run the epidemic simulation with the specified parameters.
    """
    model = EpidemicModel(
        num_agents=num_agents,
        initial_infected=initial_infected,
        transmission_prob=transmission_prob,
        recovery_prob=recovery_prob,
        vaccination_rate=vaccination_rate,
        network_prob=network_prob  # New parameter for network connectivity
    )
    for _ in range(max_steps):
        model.step()
    data = model.datacollector.get_model_vars_dataframe()
    return data

def plot_results(data_frames, labels, title, filename):
    """
    Plot the simulation results from multiple data frames.
    """
    plt.figure(figsize=(10, 6))
    for data, label in zip(data_frames, labels):
        plt.plot(data['Infected'], label=label)
    plt.xlabel('Time Step')
    plt.ylabel('Number of Infected Agents')
    plt.title(title)
    plt.legend()
    plt.savefig(f'data/{filename}')
    plt.close()

def main():
    # Common parameters
    num_agents = 100
    initial_infected = 5
    transmission_prob = 0.1
    recovery_prob = 0.05
    max_steps = 100

    # 1. Baseline Scenario (No Interventions)
    print("Running Baseline Scenario...")
    baseline_data = run_simulation(
        num_agents=num_agents,
        initial_infected=initial_infected,
        transmission_prob=transmission_prob,
        recovery_prob=recovery_prob,
        vaccination_rate=0.0,
        network_prob=0.1,
        max_steps=max_steps
    )

    # 2. Impact of Vaccination
    vaccination_rates = [0.1, 0.3, 0.5]
    vaccination_data = []
    for rate in vaccination_rates:
        print(f"Running Vaccination Scenario with rate {rate*100}%...")
        data = run_simulation(
            num_agents=num_agents,
            initial_infected=initial_infected,
            transmission_prob=transmission_prob,
            recovery_prob=recovery_prob,
            vaccination_rate=rate,
            network_prob=0.1,
            max_steps=max_steps
        )
        vaccination_data.append(data)

    # 3. Impact of Social Distancing
    print("Running Social Distancing Scenario...")
    social_distancing_data = run_simulation(
        num_agents=num_agents,
        initial_infected=initial_infected,
        transmission_prob=transmission_prob,
        recovery_prob=recovery_prob,
        vaccination_rate=0.0,
        network_prob=0.05,  # Reduced network connectivity
        max_steps=max_steps
    )

    # 4. Combined Interventions
    print("Running Combined Interventions Scenario...")
    combined_data = run_simulation(
        num_agents=num_agents,
        initial_infected=initial_infected,
        transmission_prob=transmission_prob,
        recovery_prob=recovery_prob,
        vaccination_rate=0.3,
        network_prob=0.05,  # Reduced network connectivity
        max_steps=max_steps
    )

    # Plotting Results
    print("Plotting Results...")

    # Plot Baseline vs. Vaccination Scenarios
    plot_results(
        data_frames=[baseline_data] + vaccination_data,
        labels=['Baseline'] + [f'Vaccination {int(rate*100)}%' for rate in vaccination_rates],
        title='Impact of Vaccination Rates on Disease Spread',
        filename='vaccination_impact.png'
    )

    # Plot Baseline vs. Social Distancing
    plot_results(
        data_frames=[baseline_data, social_distancing_data],
        labels=['Baseline', 'Social Distancing (p=0.05)'],
        title='Impact of Social Distancing on Disease Spread',
        filename='social_distancing_impact.png'
    )

    # Plot Combined Interventions
    plot_results(
        data_frames=[baseline_data, combined_data],
        labels=['Baseline', 'Vaccination 30% + Social Distancing'],
        title='Combined Interventions Impact on Disease Spread',
        filename='combined_interventions.png'
    )

    print("All simulations and plotting completed. Check the 'data' directory for results.")

if __name__ == '__main__':
    main()