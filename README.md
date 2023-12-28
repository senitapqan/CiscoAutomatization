# Network Tester

Network Tester is a Python application built for testing and analyzing network configurations through a graphical user interface (GUI). The main application, `main.py`, provides a user-friendly interface using the Tkinter GUI toolkit. Additionally, the `api.py` module facilitates communication with network switches via Telnet.

## Features

- **IP Configuration Check**: Verify and display IP configurations for selected switches.
- **Routing Analysis**: Examine and present routing information from network switches.
- **VLAN Inspection**: Conduct VLAN-related checks and display relevant information.
- **Switch Addition**: Dynamically add network switches to the application.
- **Save Results**: Save the results of network checks to a CSV file for future reference.
- **Answer Comparison**: Upload answers for comparison and validation of obtained results.

## Usage

1. **Add Switch**: Click the "Add Switch" button to dynamically add network switches.
2. **Select Category**: Choose a category (IP, Routing, VLAN) for specific network checks.
3. **Show Info**: Display results for the selected switches and category.
4. **Check Info**: Compare obtained information against uploaded answers.
5. **Save Info**: Save the results to a CSV file for later analysis.

## Switch API

The `api.py` module includes a `Switch` class that facilitates communication with network switches. It establishes a Telnet connection, retrieves switch configurations using the `get_parse` method, and performs specific checks based on user-selected categories using methods like `check_ip_configuration`, `check_routing`, and `check_vlan`.
