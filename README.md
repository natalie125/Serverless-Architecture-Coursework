This project investigates the performance of Python-based serverless functions on two platforms: AWS Lambda (commercial) and Knative (open-source). The serverless application chosen for testing is a lightweight image processing function that receives a base64-encoded image via an HTTP POST request, resizes it to 100x100 pixels using the Pillow library, and returns the processed image in base64 format.

To analyse performance, the same image function was deployed on both platforms, with adjustments made to suit each environment. The application also includes logic to detect cold vs warm starts, enabling more detailed performance evaluation. Multiple requests were sent under different concurrency levels (10, 20, 50) to simulate real-world usage and test scalability, latency, and cold start impact.

On AWS Lambda, the function was triggered using API Gateway, while Knative deployed the function as a container on a Kubernetes cluster with autoscaling capabilities. Performance data was collected by sending multiple concurrent HTTP requests and measuring response time, start type, and system behaviour under load.

The project demonstrates how different FaaS platforms handle the same workload and provides insights into their runtime efficiency, cold start behaviour, and scalability performance, helping evaluate their suitability for latency-sensitive applications.
