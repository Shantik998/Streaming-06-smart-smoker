# Streaming-06-smart-smoker
The main objective of this project is to establish a comprehensive monitoring and notification system tailored for environments sensitive to temperature variations, such as those involved in smoking food. This system utilizes RabbitMQ message queues in conjunction with Python scripts to ensure effective temperature monitoring and alerting.

The project is structured into distinct components, namely the Smoker Producer, Smoker Consumer, Food A Consumer, and Food B Consumer. Each of these consumers plays a crucial role in the system by receiving incoming temperature data messages, deciphering their content, and performing necessary data processing. The primary function of these consumers is to trigger alerts based on predefined criteria:

Smoker Alert: This alert is initiated when there is a substantial decrease in the smoker's temperature, specifically 15 degrees Fahrenheit or more, within a relatively short time frame of 2.5 minutes or after receiving 5 consecutive temperature readings.
Food Stall Alert: The system also issues an alert when the temperature of the food being smoked experiences minimal change, typically 1 degree Fahrenheit or less, over an extended period of 10 minutes or after collecting 20 consecutive temperature readings.
In summary, the project's core aim is to provide a robust and responsive monitoring system that ensures the safety and quality of temperature-sensitive processes, such as food smoking, by promptly notifying users of critical temperature fluctuations. This is achieved through the seamless integration of RabbitMQ messaging and Python scripting components.
# Prerequisites

Git
Python 3.7+ (3.11+ preferred)
VS Code Editor
VS Code Extension: Python (by Microsoft)
The following modules are required:

Module	Version
csv	1.0
webbrowser	3.11.4
sys	3.11.4
time	3.11.4
pika	1.3.2
collections	3.11.4
