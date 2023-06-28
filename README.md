# Group and Projects optimizer

Here is a tool that solves the following optimization problem. Given:
- A set of poeple and their teammate preferences
- A set of projects and the people's interest on each project
- A set of constraints: min / max number of people per project, couples that can't work together, minimum experience required for certain projects....
Find the group distribution and project assignments that maximizes overall welfare.

The two main blocks are an **optimization engine** built with ORTools, and a **user interface** to input the data and visualize results built with Streamlit.

### How to use
The app is deployed on the Streamlit cloud service. Can be accessed on this URL: https://groups-and-projects.streamlit.app/

### Functionality and quick tutorial
**Project definition and min/max number of members**: here we are asked to input the different projects and the min/max number of people that will work in project. Reset removes all the current projects. 
![image](https://user-images.githubusercontent.com/38510928/217017582-70d29d59-2e83-48b7-9111-d7fa12c1a537.png)

**Persons definition, experience, and gender**: here we are asked to input all the people that will be assigned to projects. We are asked about the experience years (just a value that measures experience), and this is related to a constraint in the optimization engine that forces all groups to have a minimum of experience. We are also asked about the gender, and that's because there's a constrain that forces all groups to have diversity (not all males or all females).
![image](https://user-images.githubusercontent.com/38510928/217017518-94911390-12c1-40b7-a8fc-124f6e0985bf.png)

**Project preferences**: Here we are asked to input, for each person, the project that they would like to work on (positive preferences) and projects wouln't like to work on (negative preferences). This has an impact on the objective function cost.
![image](https://user-images.githubusercontent.com/38510928/217017837-d0f14f63-b706-47c8-bc85-bdd4ad07648d.png)

**Personal preferences**: Here we are asked to input, for each person, the persons that he/she would like to work with, and the persons he/she wouldn't. This has an impact on the objective function cost.
![image](https://user-images.githubusercontent.com/38510928/217018677-7e8a6684-2dcd-441a-a514-ccf3b2d33b17.png)

**Optimization results**: There's an option to predefine some poeple in groups (that is a hard constraint that the optimizer will respect). After clicking on Run (Fes els equips!), the optimization engine is called and the solution is displayed. There's a warning if the problem is infeasible (has no solution). The percentage of team contribution into the objective optimal cost is displayed on the Happiness score under each team.
![image](https://user-images.githubusercontent.com/38510928/217018810-d2bdc397-d80e-4ed7-89f4-1e28fc2a2784.png)


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
