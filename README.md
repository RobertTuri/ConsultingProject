This project automates the process of gathering recent articles and researching market trends. It takes in a prompt from the user (perhaps an emerging technology or an industry) and outputs a data-driven dashboard that scrapes, analyses, and visualises industry sentiment and market performance from multiple sources — combining natural language processing and financial data to provide actionable insights for consultants and analysts.

Searches across priority domains grouped into:
- Professional: McKinsey, BCG, Deloitte, PwC, etc.
- Mainstream: BBC, CNN, Reuters, Financial Times, etc.
- Social: Reddit, Medium, Substack, etc.

It then fetches 5-year stock performance for companies or industries relevant to the chosen topic.

In order to get started after you have cloned the repo at https://github.com/RobertTuri/ConsultingProject (name subject to change) do the following:
1) Create and activate a virtual environment
python -m venv venv          
venv\Scripts\activate        # On Windows
source venv/bin/activate     # On macOS/Linux

NOTE: If the bash script given above gives a security error like mine did at first run PS as admin and enter the command below and then confirm with 'Y':
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

2) Install dependencies/packages
pip install -r requirements.txt

3) Run set-up script
python setup.py

4) Usage (WARNING: May be slow to run at first so do NOT press any keys as it will be passed as the input for search)
python ./src/main.py

Author: 
Robert Turi 
https://www.linkedin.com/m/in/robert-turi

