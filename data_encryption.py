import numpy as np


class KeyGenerator:

    def __init__(self, d):
        
        self.c = 5
        self.e = 5
        self.d = d
        self.eta = self.d + 1 + self.c + self.e 
        self.M_base = np.random.uniform(low = -10, high = 10, size = (self.eta, self.eta))
        self.s = np.random.uniform(low = -10, high = 10, size = self.d + 1)
        self.w = np.random.uniform(low = -10, high = 10, size = self.c)


class OwnerEncryptor:

    def __init__(self, key):

        self.key = key
        self.beta_2 = 2

    def encrypt(self, data):

        result = []

        for p in data:
            p_tilde = np.concatenate((
                np.array([self.key.s[i] - 2 * p[i] for i in range(len(p))] + [self.key.s[-1] + np.sum(p ** 2)]),
                self.key.w, np.random.uniform(low = -10, high = 10, size = self.key.e)
            ))
            p_prime = p_tilde @ np.linalg.inv(self.key.M_base)
            result.append(p_prime)

        self.max_norm = max([np.sqrt(np.sum(data[i] ** 2)) for i in range(len(data))])
        
        return np.array(result)

    def decrypt(self, data):

        result = []

        for p_prime in data:
            p_tilde = p_prime @ self.key.M_base
            p = (self.key.s[ : self.key.d] - p_tilde[ : self.key.d]) / 2
            result.append(p)
        
        return np.array(result)
    
    def query_encrypt(self, query):

        q_max = np.max(query)
        self.M_t = np.random.uniform(low = np.nextafter(q_max, q_max + 1), high = q_max + 20, size = (self.key.eta, self.key.eta))
        M_t_diagonal_entries = np.random.uniform(low = np.nextafter(self.max_norm, self.max_norm + 1), high = self.max_norm + 20, size = self.key.eta)
        for i in range(self.key.eta):
            self.M_t[i][i] = M_t_diagonal_entries[i]
        M_sec = self.M_t @ self.key.M_base
        q_prime = np.concatenate((query, np.ones(1), np.random.randint(low = -10, high = 10, size = self.key.c), np.zeros(self.key.e)))
        q_nn = np.eye(self.key.eta) * q_prime
        E = np.random.uniform(low = np.nextafter(q_max, q_max + 1), high = q_max + 20, size = (self.key.eta, self.key.eta))
        q_hat = self.beta_2 * (M_sec @ q_nn + E)

        return q_hat
    

class QueryUserEncryptor:

    def __init__(self, d, eta):
        
        self.d = d
        self.eta = eta
        self.beta_1 = 1.5
        self.N = np.eye(self.d) * np.random.uniform(low = -10, high = 10, size = self.d)
    
    def encrypt_initial(self, query):

        q_dot = self.beta_1 * query @ self.N

        return q_dot
    
    def encrypt_final(self, query):

        N_prime = np.eye(self.eta)
        for i in range(self.d):
            N_prime[i][i] = self.N[i][i]
        q_tilde = query @ np.linalg.inv(N_prime)
        
        return np.sum(q_tilde, axis=1)


class KNNCalculator:
    
    def __init__(self, data):

        self.cloud_data = data

    def calculate(self, k, query, M_t):

        data_prime = []

        for p in self.cloud_data:
            p_prime = p @ np.linalg.inv(M_t)
            data_prime.append(p_prime)
        cloud_data_prime = np.array(data_prime)

        closest_data = []
        for i in range(len(cloud_data_prime)):
            closest_data.append([i, np.sum(cloud_data_prime[i] * query)])
        closest_data.sort(key = lambda x: x[1])
        result = []
        for i in range(k):
            result.append(self.cloud_data[closest_data[i][0]])
        return np.array(result)
    
    
def StandardKNNCalculator(cloud_data, k, query):

        closest_data = []
        for i in range(len(cloud_data)):
            closest_data.append([i, np.sum((cloud_data[i] - query) ** 2)])
        closest_data.sort(key = lambda x: x[1])
        result = []
        for i in range(k):
            result.append(cloud_data[closest_data[i][0]])
        return np.array(result)