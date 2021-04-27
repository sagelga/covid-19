# COVID-19 Data Explorer
COVID-19 Data Explorer is a dashboard-data explorer for COVID-19 data around the world; running on Python using Plotly/Dash framework.

- Health Data pulled from [https://github.com/owid/covid-19-data/](https://github.com/owid/covid-19-data/)
- Vaccine Purchase &  Manufacturing Arrangements data pulled from [https://www.knowledgeportalia.org/covid19-vaccine-arrangements](https://www.knowledgeportalia.org/covid19-vaccine-arrangements)
    - Data is pulled, convert and stored in `.csv`
- Mobility Trends Reports from [https://covid19.apple.com/mobility](https://covid19.apple.com/mobility)        

## Project Roadmaps
We stored roadmaps here : [https://github.com/sagelga/covid-vaccine/projects](https://github.com/sagelga/covid-vaccine/projects)
## Develop
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
    python index.py
    ```
3. Your app will run in `localhost` and `debug` mode. Please refer to Plotly/Dash documentation for more detail.

### Directory
For maintainance
- `.vscode` for VSCode automation and configurations
- `LICENSE` for legal things

## Deployment
Repository development develiverables will be automatically deployed to Heroku after merge/push commit.

Official version is available on [covid.sagelga.com](http://covid.sagelga.com)

Also available in `dev` mode on [dev.covid.sagelga.com](http://dev.covid.sagelga.com/). Expect some nasty bugs and crashes in this website.

## Contributor
![Contributor bubble](https://contrib.rocks/image?repo=sagelga/covid-vaccine)

## Donations
If you like to support us via donation, please leave a donations here : [https://commerce.coinbase.com/checkout/aed305a0-d6ae-4d98-b993-b1e85e0a99f6](https://commerce.coinbase.com/checkout/aed305a0-d6ae-4d98-b993-b1e85e0a99f6)

All of the donations goes to fund Operation (and soon the future) cost.

---

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/contains-cat-gifs.svg)](https://forthebadge.com)