# cars_api

### Run server
uvicorn src.main:app --reload

### Run tests
pytest

### Deployed app
https://cars-api-task-9be479b79f13.herokuapp.com/

### For convenient api interface
https://cars-api-task-9be479b79f13.herokuapp.com/docs

### Used setup
FastAPI was chosen for the purpose of building the API due to it's high-performance and reduced speed of development.

As a database MongoDB was chosen as it offers ACID guarantees, is highly scalable but also very flexible and easy to use.
For the purpose of given task where only one collection of data is stored it seemed to be a sufficient solution, however,
for more extensive data schema with complex relations possibly relational database would have to be considered. 

In proposed approach for every car model, sum of ratings and number of given ratings are stored to calculate average rating based on that.
Example document stored in the database looks as follows:

{"_id":{"make":"Honda","model":"CBR1000RR"},"rates_sum":17,"rates_num":5}

Since these values are incremented using $inc operation which in MongoDB is atomic there is no risk of interruption by other concurrent update operation.
Moreover, int values can be stored using 64 bits so there should be no risk of out of range error. 
It was also assumed that number of updates would be reasonably small, but in case of heavy load of updates of the same car record possibly other approach would have to be
considered, optimized for writes. Potentially new collection/table would be required to store only ratings but it this scenario calculartion of average would be more expensive.
Furthermore, index was created on attribute representing number of ratings to improve sorting performance for /popular endpoint. 
