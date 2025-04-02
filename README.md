# EnergyForecasting

Machine Learning models for electricity price, load, generation and weather forecasting.

# Table of Contents

Coming soon...

## Introduction

This project is focused on energy modelling, more specifically on the development of forecasting models for several quantities of interest, such as electrical loads, electricity prices, power generation, and weather variables. Additional analyses, such as load profiling and anomaly detection studies, will also be conducted.

## Installation

A project configuration file will soon be added to the repository. When that happens, installation instructions via Github will be provided here.

## Models and Applications

The following table presents the problems that are to be solved by the models, as well as the predictors that may be used, potential applications, and the datasets that will be used to train the models:

| Forecasting Problem | Predictors | Application | Datasets |
| :--: | :--: | :--: | :--: |
| Hourly Day-Ahead Load Forecasting | Load, Weather, Generation | Unit Commitment Problem | 1, 8 |
| 15-min-Ahead Load Forecasting | Load, Generation | Economic Dispatch Problem | 1, 2, 8 |
| Hourly Day-Ahead Wind Power Forecasting | Wind, Wind Generation, Installed Capacity | Unit Commitment Problem | 1, 3, 4, 8 |
| 15-min-Ahead Wind Power Forecasting | Wind, Wind Generation, Installed Capacity, Turbine Power Curves | Economic Dispatch Problem, HVAC Control | 3-6, 8 |
| Hourly Day-Ahead Electricity Price Forecasting | Load, Weather, Generation, Price | Demand Response Program | 1 |
| Tabular Price Models | Weather, Load, Generation | HVAC Control Simulation | 1-4 |
| 15-min-Ahead (or lower) Weather Forecasting | Weather | HVAC Control Systems | 1 |
| 15-min-Ahead (or lower) Electricity Price Forecasting | Weather, Price | HVAC Control Systems with Real-time Pricing | 1-4 |
| Load Profiling | Load, maybe Weather | Autonomous study | 7 |
| Classification | Load, Price | Tariff definition for Demand Response Programs | 1, 7 |
| Anomaly Detection | Load, Generation, Price | Anomalous consumption patterns, tariff definition for Demand Response Programs | 1, 7 |

## Datasets

All the datasets used in this work are publicly available and can be easily download from the Kaggle repository:

1. [Hourly electricy prices, consumption, generation and weather - Spain](https://www.kaggle.com/datasets/nicholasjhana/energy-consumption-generation-prices-and-weather)
2. [Western Europe Power Consumption](https://www.kaggle.com/datasets/francoisraucent/western-europe-power-consumption?select=nl.csv)
3. [Wind Power in Germany](https://www.kaggle.com/datasets/l3llff/wind-power)
4. [Hourly Power Generation in Europe](https://www.kaggle.com/datasets/mehmetnuryildirim/hourly-power-generation-of-europe?select=Germany_Power_Generation.csv)
5. [Europe's Installed Capacity per Production Type](https://www.kaggle.com/datasets/mehmetnuryildirim/europes-installed-capacity-per-production-type?select=InstalledCapacity_Germany_2022.csv)
6. [Europe Installed Capacity and Power Generation](https://www.kaggle.com/datasets/mehmetnuryildirim/europe-installed-capacity-and-power-generation)
7. [Load profile data of 50 industrial plants](https://www.kaggle.com/datasets/pythonafroz/load-profile-data-of-50-industrial-plants)
8. [Power Systems Optimisation course materials](https://github.com/Power-Systems-Optimization-Course/power-systems-optimization)

## Deployment

The resulting models may be deployed in one of three ways, depending on the application:

- Python API via FastAPI within a Docker container;
- Python Web App using Streamlit or Dash/Plotly (published autonomously or via Docker container);
- Edge deployment using an STM32 and/or Raspberry Pi (for control applications).

## Licence

This project is licensed under the [Apache 2.0 licence](LICENSE).