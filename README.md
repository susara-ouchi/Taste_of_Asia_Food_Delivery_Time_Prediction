# Taste of Asia - Food-delivery-prediction-website

“A perfectly cooked meal means nothing if it’s not served on time”. 

In the fast-paced world we live in, food delivery has become more than just a convenience, it’s a solution that brings the flavors of the world to your doorstep, turning every meal into an experience without leaving the comfort of your home. 

In the food delivery industry, punctuality transforms this mere service into a seamless culinary experience. Hence, the delivery time, or more precisely on-time delivery, happens to have a significant impact on customer satisfaction and service quality of the delivery company which drives the competition in the industry. Yet, achieving this standard of on-time delivery is not a piece of cake, it is influenced by a lot of internal as well as external factors. 
The summarized analysis given here was based on a rich dataset obtained from Kaggle which included several external and internal factors deemed important to conduct a thorough analysis. 

Hence, the analysis was mainly directed towards addressing two objectives, 
1)	Identifying the factors that have the most significant influence on the food delivery time.
2)	Developing an effective delivery time prediction model that will aid the delivery companies in evaluating their performance showing them necessary directions for improvements

The response variable, Delivery Time (in minutes) was a continuous one, which led to the use of multiple linear regression as the benchmark model, and the model was evaluated with MSE and R-squared metrics. Despite outliers, similar metrics were obtained with and without them for the benchmark model, so they were retained in the analysis. Thereafter, various models (KNN, SVR, XGBoost, Random Forest) were tested, with XGBoost and Random Forest performing best and yielding almost identical results. To resolve the dilemma of choosing between them, an ensemble model combining both was created, leveraging their strengths and chosen as the best model for predicting delivery time. 

To sum up, the analysis highlighted key factors crucial for enhancing delivery time. It also offers valuable insights for delivery companies aiming to improve their services, particularly in densely populated countries like India with unique logistical challenges. Implementing changes based on these findings could hopefully lead to more efficient and timely deliveries, ultimately boosting customer satisfaction and loyalty.