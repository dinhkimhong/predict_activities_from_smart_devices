# Predict human activites from smart devices
Predicting human activities from sensor data in smartphones and smartwatches <br>
In most smart devices, there is a health app that determines the metrics that matter to users, for example: how far and how many steps users have walked in a certain time… and more information about the users’ health data.<br>
How does the app know that the users are walking or not walking to start counting steps? How does machine learning work to detect activity? <br>
Members of the WIDSM (Wireless Sensor Data Mining) Lab in the Department of Computer and Information Science of Fordham University conducted a project of collecting data from 2 sensors: Accelerometer and Gyroscope on Smartphones and Smartwatches from 51 subjects performed 18 activities of daily living. These activities include basic ambulation-related activities, hand-based activities, and various eating activities. Sensor data was collected at a rate of 20 Hz (i.e, every 50 ms).<br>
The data set is available from the UCI Machine Learning Repository as the “WISDM Smartphone and Smartwatch Activity and Biometrics Dataset.”<br>
There are 2 different approaches:<br>
1.Using a traditional classifier on label data from a fixed-length window of 10 seconds.<br>
2.Using 1D Convolutional Neural Network<br>
Both approaches in this project are feature approaches. <br>
For a complete time series approach, I plan to use LSTM or HMM model which is a better approach, which receives the entire series as inputs, rather than window values. And that is my future work.
