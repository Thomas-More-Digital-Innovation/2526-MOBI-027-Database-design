# Mobilab & Care - Jobtakels Project

## 📋 Project Overview

This project is a continuation and enhancement of the **sense to eXion** initiative, now transitioning into the **Jobtakels** project. The goal is to revisit and improve the existing database infrastructure that stores information about exoskeletons, sensors, and risk assessment tools used to aid workplace movement and reduce physical strain on employees.

## 🎯 Project Goals

Mobilab & Care, a research group within Thomas More University of Applied Sciences' Care and Well-being Centre of Expertise, aims to improve quality of life for people with care or support needs. This project specifically focuses on:

- Storing and managing data about exoskeletons, sensors, and workplace risk assessment tools
- Enabling efficient querying (e.g., "Which exoskeletons support shoulder movement?")
- Making findings publicly accessible through a web interface
- Visualizing data relationships in an intuitive graph format
- Providing comprehensive data dashboards

## 📊 Background

### Previous Implementation
- A graph database (Neo4j) was built by DI-students for the sense to eXion project
- Data was stored and a front-end was developed for querying
- Example queries included finding exoskeletons by type or recommendations based on workplace needs
- The website was completed but never went live
- Both the database and source Excel files are available

### Current Status
- The sense to eXion project has concluded
- The **Jobtakels** project will build upon and extend this work
- Time to reevaluate technology choices and decisions

## 🛣️ Project Roadmap

### Phase 1: Database Technology Decision
**Objective**: Determine the optimal database solution

- Review available data from Excel files
- Build proof-of-concept implementations in multiple database technologies:
  - Neo4j (existing solution evaluation)
  - MongoDB (document-based approach)
  - Relational databases (PostgreSQL/MySQL)
- Consider web frontend requirements
- Deliver findings with cost estimates and recommendations

### Phase 2: Database Rebuilding
**Objective**: Implement production-ready database

- Build the chosen database solution
- Create efficient data import mechanisms
- Develop database administration interface
- Determine optimal hosting strategy for public access
- Ensure scalability and maintainability

### Phase 3: Public Website
**Objective**: Share findings with the public

- Develop a public-facing website (government-funded requirement)
- Implement filtering and search functionality
- Choose and justify web technology stack
- Ensure client approval of technology choices
- Make data easily accessible and explorable

### Phase 4: Graph Visualization
**Objective**: Visualize data relationships

- Create a graph-view plugin for the website
- Display relationships (e.g., joints → supported exoskeletons)
- Enable interactive exploration of connections
- Maintain the original vision of relationship-based data exploration

### Phase 5: Data Dashboard
**Objective**: Provide comprehensive data overview

- Develop a standalone dashboard component
- Present data without requiring complex queries
- Design will be refined based on client feedback and relationship development
- Focus on actionable insights and data overview

## 📅 Timeline

**Semester 1** - All phases to be completed

## 🛠️ Technologies

The project will involve:
- **Database Design** - Choosing and implementing the optimal database solution
- **Data Engineering** - Import mechanisms and data management
- **Web Development** - Public-facing website and interfaces
- **Data Visualization** - Graph views and dashboards

## 📍 Workspace

- **Analysis**: P200
- **Development**: On campus at school