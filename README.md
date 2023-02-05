# Group and Projects optimizer

Here is a tool that solves the following optimization problem. Given:
- A set of poeple and their teammate preferences
- A set of projects and the people's interest on each project
- A set of constraints: min / max number of people per project, couples that can't work together, minimum experience required for certain projects....
Find the group distribution and project assignments that maximizes overall welfare.

The two main blocks are an **optimization engine** built with ORTools, and a **user interface** to input the data and visualize results built with Streamlit.

### How to use
The app is deployed on the Streamlit cloud service. Can be accessed on this URL: 
https://jsalva9-group-and-projects-optimi-srcstreamlit-dashboard-wrtuc3.streamlit.app/

### Functionality and quick tutorial


### How to install and run
If you want to contribute to the project or modify it for personal use, follow the next steps.
Clone the repository on a local environment. Install dependencies listed in *requirements.txt*. 
Run the following Console commands:
`cd group_and_projects_optimizer`   (move to the base level of the repository)
`streamlit run main.py`             (deploy Streamlit app locally)

### Modules of the project
**Data Transform**: in charge of transforming the input provided by the user (tables) into the data model format required by the Optimizer (maps of constraint coefficients). 

**Optimizer**: optimization engine that solves the optimization problem calling the ORTools *cpmodel* solver

**Streamlit App**: defines the UI using the Streamlit package dashboarding tools. 
