# COVID-19 Data Explorer
COVID-19 Data Explorer is a dashboard-data explorer for COVID-19 data around the world; running on Python using Plotly/Dash framework.

Data pulled from [https://github.com/owid/covid-19-data/](https://github.com/owid/covid-19-data/)

## Local Development
To locally develop this project, here's what you need 
1. Python >= 3.6
2. Python Virtual Environment (venv) (Strongly Recommended)
3. IDE or Text Editor you are familar with
4. Modern Internet Browser (i.e. Google Chrome (or Chromium-based Browswer), Mozilla Firefox, Apple Safari)

### Installation
1. Install the required packages
    ``` bash
    pip3 install -r requirements.txt
    ```
2. then run the app using
    ``` bash
    python app.py
    ```
3. Your app will run in `localhost` and `debug` mode. Please refer to Plotly/Dash documentation for more detail.

## Directory
For maintainance
- `.vscode` for VSCode automation and configurations
- `LICENSE` for legal things

## Deployment
This repo will be automatically deployed to [covid.sagelga.com](http://covid.sagelga.com) using Heroku.

Also available in `develop` mode in [https://sagelga-covid-vaccine-dev.herokuapp.com/](https://sagelga-covid-vaccine-dev.herokuapp.com/)

## Contributor
![Contributor bubble](https://contrib.rocks/image?repo=sagelga/covid-vaccine)
