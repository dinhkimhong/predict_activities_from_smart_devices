# predict_activities_from_smart_devices
Predicting human activities from sensor data in smartphones and smartwatches
In most smart devices, there is a health app that determines the metrics that matter to users, for example: how far and how many steps users have walked in a certain time… and more information about the users’ health data.
How does the app know that the users are walking or not walking to start counting steps? How does machine learning work to detect activity? 
Members of the WIDSM (Wireless Sensor Data Mining) Lab in the Department of Computer and Information Science of Fordham University conducted a project of collecting data from 2 sensors: Accelerometer and Gyroscope on Smartphones and Smartwatches from 51 subjects performed 18 activities of daily living. These activities include basic ambulation-related activities, hand-based activities, and various eating activities. Sensor data was collected at a rate of 20 Hz (i.e, every 50 ms).
The data set is available from the UCI Machine Learning Repository as the “WISDM Smartphone and Smartwatch Activity and Biometrics Dataset.”
There are 2 different approaches:
1.Using a traditional classifier on label data from a fixed-length window of 10 seconds.
2.Using 1D Convolutional Neural Network
Both approaches in this project are feature approaches. 
For a complete time series approach, using LSTM or HMM model is a better approach, which receives the entire series as inputs, rather than window values. And that is my future work.
