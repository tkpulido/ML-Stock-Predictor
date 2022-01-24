# Close of the Day Stock price predictor
  Input : Day Open, ATR, FIrst 15 Min candle is green (True) or Red(False)
  Output : Day Close
  
  Usage:
      test_and_plot("ticker")
           The program fetches 1000 Calendar days data from Alpaca. Train the model. 
           Plot the last 50 Days of predicted close price vs  actual close price.
  
  Environment Variables Needed:
      APCA_API_SECRET_KEY
      APCA_API_KEY_ID

  Model Used: Linear Regression.
  Example usage is in project.ipynb
# ML Stocks Predictor Positive Movement

This is to use AWS SageMakers machine learning to see if there is predictive correlation with positive open (15min candle) of a stock to its future value.

---

## Technologies

This requires these tools for the application to run properly.
- MacOS, Windows, or Linux operating system 2015 or newer
- Terminal or a Command Line Interface
- python 3.7
- Python pandas module
- Python pathlib module
- Python matplotlib module
- Python numpy module
- In AWS:
-     os module
-     io module
-     json module
-     numpy module
-     pandas module
-     pathlib module
-     matplotlib.pyplot module
-     sklearn.model_selection module
-     sklearn.metrics module
-     sagemaker module
-     boto3 module
-     
- JupyterLabs module and use through terminal, AWS notebook instances
- Webbrowser capable of Jupyterlabs, AWS, AWS S3, AWS SageMaker workthrough

---

## Installation Guide

To install this application please follow this process:

1. Install python3.7 and all accompaning modules.
2. Download application file and resource file.
    - Note: Pay attention to where file is located as you will need this information for running the applicaiton in a command line interface later.
3. Sign up for an AWS account which will need a S3 bucket set up to receive the data.
4. Process the the data in the file marked 'ml_movement_predictor' in AWS SageMaker - Studio

---

## Usage

To use this application please follow this process:

1. Download the Module 4 folder and contents to your computer.
2. Open a Jupyter Labs terminal from the Module 4 terminal folder 
3. Run the  risk_return_analysis.ipynb file in Jupyter Labs.
4. As needed, be sure that the relative path is set for the read_csv function to operate, the whale_navs.csv file is located in the resources folder inside the Starter_Code folder.
5. Run cells in order to process and review data.

---

## Contributors

Contributors include:
- Anthony Zamora, available at freshfarm99@gmail.com for questions and comments.
- Tristen Pulido
- Anil Vinnakota

    - Assistance from Teachers Assistants and Teacher of FinTech Class UC Berkeley Extension course.
        

---

## License

Licensed by Anthony Zamora Inc.

---
