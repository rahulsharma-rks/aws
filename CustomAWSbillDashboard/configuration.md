# AWSbillDashboard
**Steps:**
1. Set Up AWS Account and Permissions
2. Enable AWS Cost Explorer
3. Set Up Data Storage (AWS S3)
4. Create Lambda Function for Data Collection
5. Preprocess and Store Data
6. Create a Web Application Frontend
7. Test and Optimize

**Configurations for S3 Bucket.**

* Enable Transfer acceleration.
* Enable Static website hosting.
* Add CORS in bucket Permissions.
  ```
  [
    {
        "AllowedHeaders": [
            "*"
        ],
        "AllowedMethods": [
            "GET",
            "PUT",
            "POST",
            "DELETE"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
  ]
  
  ```

**Output**
![image](https://github.com/rahulsharma-rks/AWSbillDashboard/assets/27508314/08d2d42a-0137-48da-973a-fb136b52a955)
