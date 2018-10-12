# Disaster-Help-Predictor

Classification of social media posts into some predefined classes and new classes as defined later dynamically.

The idea is to cluster the same type of posts which denote a certain type of help required by the affected site. For example a tweet - "We don't need money or medical support. We only need food. #Haiyan". 

This can denote infrastructure damage, cry for food or medical help. We use NLP and clustering algorithms to cluster the similar posts. We also plan to have an interface for people to check out the posts recieved, related to the disaster and give their input for the class, which can be a predefined class or they can add a new class. The post after getting a certain threshold of confidence gets assigned the most voted class.

The metadata of a post information provides us with the location of the post. We can automate a sending helping process for that location based on the type of help required. For example sending notification to the nearby hospital. 
