# Movehack
Our system provides users best mode of transportation with te following parameters:
-Minimum time
-Minimum cost
-Maximum comfort level

We have created a graph where the nodes are the bus stops and metro stations combined. For each trips of a passenger, We are storing the trip as an edge in the graph. Also, for all metro stations and bus stops, We are finding the nearest bus stop and metro station respectively using only the geological coordinates (gives a good approximation). We are also using another graph of metro stations where an edge exists between adjacent metro stations so that we can find the cost between any pair of metro stations using a graph algorithm called Floyd Warshall. We also mapped the geological coordinates of all the bus stops and metro stations using Google API. So, given a starting and ending location, We will find the nearest bus/metro station from the starting location and the ending location and run djisktra to find the shortest path between these pairs in terms of cost and time. Also, for comfort, private cabs from uber is taken into consideration. We are running an API to get the details for the uberGO price and time taken to get there.

Please find the assets from https://drive.google.com/open?id=1D2E6cdw-G4BF1MQETFUCzj-rUGAWhdqf.
Download the assets folder in the root and run the command: '$ python app.py' in the terminal. Wait for the preprocessing for around 30 seconds and then run localhost:5000 in the browser.
For checking, please enter the card number: 4242 4242 4242 4242.
