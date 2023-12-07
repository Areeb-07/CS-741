import numpy as np
import pandas as pd

from data_encryption import *

class Simulator:
    
    def __init__(self):

        self.data = pd.read_excel('points_data.xlsx').to_numpy()
        
        self.key = KeyGenerator(self.data.shape[1])

        self.data_owner = OwnerEncryptor(self.key)

        self.query_user = QueryUserEncryptor(self.data.shape[1], self.key.eta)

        self.cloud_data = self.data_owner.encrypt(self.data)

        pd.DataFrame(self.cloud_data).to_excel('encrypted_points.xlsx')

        self.knn_calculator = KNNCalculator(self.cloud_data) 

        while True:
            query_input = input("Enter the query vector, space separated: ")
            if query_input.lower() == 'quit':
                break
            k = int(input("Enter the value of k: "))

            query = np.array([float(i) for i in query_input.strip().split()])
            q_dot = self.query_user.encrypt_initial(query)
            q_hat = self.data_owner.query_encrypt(q_dot)
            q_vec = self.query_user.encrypt_final(q_hat)

            result = self.data_owner.decrypt(self.knn_calculator.calculate(k, q_vec, self.data_owner.M_t))

            print("\nResult:\n")
            for i in result:
                print(i, "- Distance =", np.sqrt(np.sum((i-query)**2)))

            true_result = StandardKNNCalculator(self.data, k, query)
            print("\nTrue Result:\n")
            for i in true_result:
                print(i, "- Distance =", np.sqrt(np.sum((i-query)**2)))
            print()


if __name__ == "__main__":
    sim = Simulator()