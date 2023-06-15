## MachineLearning_Project Capstone_BANGKIT2023
This repo is for recommendation system files for BudgetIN app. Our system has not implemented ML model however we do use some preprocessing for our main dataset.  

Recommendation system Architecture : 

![Model](https://github.com/BudgetInCapstone/MachineLearning/blob/main/ML%20ARCH.png)

Our main idea of this recommendation system is to fetch data of amount budget from user input, and user's location. Then our recsys will acquire the data from database and send it to the system to be processed. Our recommendation will generate food place that's cheaper in maximum price of foods that is not more than initial budget from user. Finally, the system will generate the location that is nearest to the user's location.

## Brief
- To database : files for uploading dataset to firebase

- main/recosys : files for recommendation (old)

- development/recsys : files for recommendation system (new)

- Other files : Old files and some notebook of our models that we couldnt implemented it to our application.

Our approach is originally using K-NN algorithm to find nearest data to the input data and generate the recommendation for it. Unfortunately, we have given in for the simpler recommendation system. However the developer still actively conduct researches and further development for this application can utilize ML aspects.

## Recommendation System
Tools and libraries used : 
FASTAPI
UVICORN
GUNICORN
Numpy
Pandas
scikit.learn (supposed to)
Tensorflow (supposed to)

As developer mention from earlier section, why we didn't utilized the ML model to our system. This is due to our lack of research for references and knowledge to apply it to our app. And we are striving to develop the recommendation system that is supposed to have ML model.

// This recsys deployed using App Engine from GCP services.

For recommendation system API using : 
<pre>
https://servicetwo-dot-capstone-project-387701.et.r.appspot.com//get_resto
</pre>

Testing the API :
<pre>
{
"max"  :50000,
"min"  :30000,
"lat"  :-7.9722092074906294,
"long":112.62179780958783,
"radius":100
}
</pre>

Screenshot of Testing :
![Postman Testing](https://github.com/BudgetInCapstone/MachineLearning/blob/main/Testing_API_1.png)

This output and response could change when :
- All variables above has different values, especially "radius" . The smaller the values of it the fewer the place is recommended from this system.
- All the values auto fill, and changed from the user inferences and input from our Android mobile app.

