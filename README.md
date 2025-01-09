# Cohere Commerce Recommendation Model

The **Cohere Commerce Machine Learning Recommendation Model** is an innovative addition to Cohere Commerce's’ existing e-commerce platform. This addition designed to streamline the purchasing process while providing a personalized shopping experience for customers. Leveraging cutting-edge AI and machine learning technology, this application delivers targeted, tailored product recommendations. With a focus on scalability and performance, this platform aims to offer an intuitive user interface and a secure environment for customers.

Below is the current UI that houses the machine learning recommendation API: 
- The reccomendations are at the bottom of the page and correspond to brand ID's which are present in our dataset

<img width="1470" alt="Screenshot 2024-12-04 at 1 55 24 PM" src="https://github.com/user-attachments/assets/17915e7e-040d-40e5-ba74-709a402d3db9">


Searching for the API's first reccomendation returns highly relevant and accurate results, offering strong suggestions that align well with the user's preferences as shown below:

<img width="1470" alt="Screenshot 2024-12-08 at 6 06 45 PM" src="https://github.com/user-attachments/assets/25d8d7ba-2f9b-4122-a99e-a405127e7768">


Below is the pipeline for cleaning and processing review data, performing sentiment analysis, prioritizing user-defined rating categories, and using SVD-based matrix factorization to recommend top brands.

<img width="894" alt="Screenshot 2025-01-08 at 4 27 48 PM" src="https://github.com/user-attachments/assets/ff091f97-002e-4690-8288-70b9af013e79">


## Set Up and Run the API
### Setup Process
1) Clone the repository to your local machine
2) Install pipenv by using command: ```pip install pipenv```
3) Install the dependencies by using command: ```pipenv install```

### Running the Application
1) Activate the virtual environment by using command: pipenv shell   
2) In the terminal, type these commands: 
- ```python```
- ```import fastapi```
- ```exit()```
3) Run the application by using command: ```uvicorn api.main:app --reload```
4) Open your web browser and navigate to ```http://127.0.0.1:8000``` (or link show on terminal)
5) Optional: You can use the Swagger UI to interact with the API by navigating to ```http://127.0.0.1:8000/docs``` in your web browser.
6) To end the process, click on the terminal then ```Ctrl + C```
7) To deactivate the virtual environment, in terminal type: ```exit```

### Next step:
1) Visit the ```http://127.0.0.1:8000/docs``` after step 3 above
2) Choose the GET route that has /recommend
3) Click ```Try it out```
4) Click excecute and you will see this
![Screenshot 2024-11-10 233942](https://github.com/user-attachments/assets/3257d833-d1c5-4eeb-a536-e1358fd8d901)

5) Look at the Response body, that is our top 5 recommended brand id

### Installing Packages
If you need to install any other packages. Follow these steps
1) Deactivate virtual env
2) Use command: ```pipenv install <package-name>```
3) Activate virtual env
4) Import those package if needed by following step 2 in the "Running the Application" part.

Note: If you want to install dev-package, the use this command: ```pipenv install --dev <package-name>```




