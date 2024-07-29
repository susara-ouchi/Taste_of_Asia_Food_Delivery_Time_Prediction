# Taste of Asia - Food Delivery Prediction Website

### Contributors: Susara Ouchithya, Thiruni Withana, Heshani Kavindya

---

### "A perfectly cooked meal means nothing if it’s not served on time."

In today's fast-paced world, food delivery isn't just a convenience; it brings global flavors to your doorstep, turning every meal into an unforgettable experience from the comfort of your home.

Punctuality in food delivery transforms this service into a seamless culinary journey. Timely delivery significantly impacts customer satisfaction and service quality, driving competition in the industry. Achieving on-time delivery is challenging due to numerous internal and external factors.

Our analysis is based on a rich dataset from Kaggle, encompassing various factors crucial for thorough examination.

### Objectives:

1. **Identify Key Factors Influencing Delivery Time**
2. **Develop an Effective Delivery Time Prediction Model**

The response variable, Delivery Time (in minutes), is continuous, leading to the use of multiple linear regression as our benchmark model. The model was evaluated using MSE and R-squared metrics. Despite outliers, similar metrics were obtained with and without them, so they were retained in the analysis. We tested various models (KNN, SVR, XGBoost, Random Forest), with XGBoost and Random Forest performing best and yielding nearly identical results. To resolve the choice between them, an ensemble model combining both was created, leveraging their strengths and chosen as the best model for predicting delivery time.

### Key Takeaways:

- The analysis highlighted key factors crucial for enhancing delivery time.
- Offers valuable insights for delivery companies aiming to improve their services.
- Particularly useful in densely populated countries like India with unique logistical challenges.
- Implementing changes based on these findings could lead to more efficient and timely deliveries, boosting customer satisfaction and loyalty.

### Conclusion:

Our findings offer actionable insights for improving food delivery services, ensuring timely deliveries, and enhancing customer satisfaction and loyalty. By addressing the identified factors, delivery companies can make data-driven improvements, providing a better experience for their customers.

---

We hope this analysis serves as a valuable resource for the food delivery industry, contributing to more efficient and satisfying customer experiences.


