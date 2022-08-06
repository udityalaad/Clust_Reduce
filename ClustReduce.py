import numpy as np
from matplotlib import pyplot

# -------------------------------------------------------------------------------------------------
#               Kohenen's Self Organizing Network (KSOM)
# -------------------------------------------------------------------------------------------------
class KSOM ():
    def __init__ (self, size_input_features = 0, rows = 0, columns = 0, alpha_init = 0, alpha_update = None, w = None, neighbourhood = False, max_epochs = 0, sigma = 0):
        # Number of features in each input
        self.size_input_features = size_input_features

        # Number of neurons in the feature map
        self.rows = rows
        self.columns = columns
        self.size_featureMap = rows * columns

        # Learning rate
        self.alpha_init = alpha_init
        self.alpha_update = alpha_update

        # Weights
        self.w = w

        # Whether neighbourhood exists or not (True/False)
        self.neighbourhood = neighbourhood

        # Max Allowed Epochs (while training)
        self.max_epochs = max_epochs

        # Initial Value of Sigma
        self.sigma_init = sigma

        # To find the Euclidean distance of all neurons from the winning neuron
        # Map_matrix
        self.d_mat = None
        if neighbourhood:
            self.d_mat = np.random.rand(self.rows*self.columns, 2)
            for i in range(len(self.d_mat)):
                self.d_mat[i] = np.array([i // 100 if j == 0 else i % 100 for j in range(2)])


    # -------------- Train the network with given data -----------------
    def train(self, inputs, checkpoints = []):
        # Step 1: Initialization
        if type(self.w) == type(None):
            self.w = np.random.rand(self.size_input_features, self.size_featureMap)

        checkpoint_weights = np.array([self.w])

        # Step 2: Competition
        for epoch in range(self.max_epochs):
            for input in inputs:
                # Step 2a: Find Winning Neuron
                winner = self.find_Winning_Neuron(input)

                # Step 2b: Update Winner and it's Neighborhood's Weights
                self.update_Neighbourhood_Weights(input, winner, epoch)

            # Save weights, when checkpoints are reached (For Assignment only)
            if (epoch + 1) in checkpoints:
                checkpoint_weights = np.append(checkpoint_weights, [self.w], axis = 0)
                
        return checkpoint_weights
                
        
    # -------------- Function to find the winning neuron for the given data point -----------------
    def find_Winning_Neuron (self, input):
        dist = np.sum(np.square(input.T - self.w.T), axis = 1)
        return np.argmin(dist)


    # -------------- Function to Update Winner and it's Neighborhood's Weights -----------------
    def update_Neighbourhood_Weights (self, input, winner, epoch):
        # For problems without neighbourhood condition
        if not self.neighbourhood:  
            self.w[:, winner] += self.alpha_init * (input - self.w[:, winner])    
        # For problems with neighbourhood
        else:
            alpha = self.update_alpha(epoch)
            sigma_square = np.square(self.sigma_init * np.exp(-(epoch)/self.max_epochs))
            
            winner_mat = np.array([winner // self.rows, winner % self.rows])
            d_square = np.power(self.find_Euclidian_Distance(winner_mat.T, self.d_mat.T), 2).T
            # d = self.find_Euclidian_Distance(self.w, self.w[:, winner])
            h = np.exp(- d_square / (2 * sigma_square))

            self.w +=  (alpha * h * (input.T - self.w.T).T)
            
    
    # -------------- Function to find the learning rate for the given epoch -----------------
    def update_alpha (self, k):
        if self.alpha_update != None:
            return pow(self.alpha_update, k) * self.alpha_init
        else:
            return (self.alpha_init * np.exp(-k/self.max_epochs))
    # ---------------------------------------------------------------------------


    # -------------- Function to find the Eclidean Distance -----------------
    def find_Euclidian_Distance (self, src, dest):
        return np.sqrt(np.sum(np.square(src.T - dest.T), axis = 1)).T
# -------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------