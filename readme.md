# Scopus Citation Scraper
## Why? 
When using engineering village, google scholar or other citation databases, the quality of the citation data is unreliable and not standardized. Having a standardized data format for each of the reference publication can help in analyzing your bibliography data. Citation data from Scopus is of excellent quality. 

## Solution
I used the DOI information from engineering village and searched citation data for each DOI in Scopus. 
This is a small robotic automation project I had to develop while writing the following publication.
Feel free to use this program as you wish and change the logic as per your use case. 

`Hegde, J., Rokseth, B. 
Applications of machine learning methods for engineering risk assessment – A review
(2020) Safety Science, 122.
https://www.sciencedirect.com/science/article/pii/S0925753519308835
`

## Installation
Step 1. Clone this repository 

Step 2. Navigate into the cloned repository
`
cd scopusCitationScraper
`

Step 3. Setup a virtual environment  
`
pip install virtualenv 
`
`virtualenv env
`

Activate the virtualenv in windows
`
.\env\Scripts\activate
`

Activate the virtualenv in linux
`
source /env/bin/activate.sh
`

Step 4. Once the virtual environment is activated use the requirements.txt file to install all dependencies
`
pip install -r requirements.txt
` 

Step 6. Install Firefox browser (https://www.mozilla.org/en-US/firefox/new/)

Step 7. Input DOIs you are interested in the doi.csv file 

Step 8. Run 'ScopusScraper.py'
`
python ScopusScraper.py
`

## Process
The process will open firefox and navigate to scopus and search for the given DOI.
Citations will be downloaded to your "Downloads" folder as defined in Firefox. 


## Contributors
* [jeev20]("https://github.com/jeev20")