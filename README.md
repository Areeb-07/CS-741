# CS 741 - Advanced Network Security and Cryptography

### Homomorphic Encryption for Secure K-Nearest Neighbour Search on Cloud Data

To simulate the encryption scheme, run the file knn_computation.py

The file data_encryption.py defines classes:
- KeyGenerator - to generate key for data owner
- OwnerEncryptor - to provide functions to encrypt and decrypt data, and to encrypt query vector
- QueryUserEncryptor - to provide functions to perform initial and final encryptions of the query vector
- KNNCalculator - to provide function to search k nearest neighbours of a given query vector
- A function StandardKNNCalculator is used to evaluate the performance of the encryption scheme by calculating true nearest neighbours

The file knn_computation.py simulates the data encryption, storage, and querying process.
The file points_data.xlsx is used as sample data for this project, which contains information about 26,000 points lying in space, measured by a LiDAR sensor.
The data is encrypted and stored in a file encrypted_points.xlsx
The code allows user to keep performing KNN searches unless user types 'quit'.
The result of each query is the nearest vecotrs found with the encryption scheme, along with their distances from query vector.
Additionally, the true nearest vectors are also listed, along with their distances from query vector.
The scheme can be used to estimate exact vectors when the distances are large
For smaller closest distance, the scheme does not provide exact vectors but provides vectors reasonably close to query vector.