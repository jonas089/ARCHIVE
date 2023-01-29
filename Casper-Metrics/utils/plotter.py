import matplotlib.pyplot as plt
# example: Deploys on y-axis, Height on x-axis
def generate(x_arr, y_arr, x_label, y_label, path, filename):
    plt.plot(x_arr, y_arr)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(path + filename)

# Plot Deploys or Transfers in steps.
'''

example: steps = 2500
Blocks 0 - 2500: 30 deploys
=> (2500, 30)
Blocks 2501 - 3000: 10 deploys
=> (3000, 10)
...

'''
#transfer_hashes, deploy_hashes

#########################################
# Example Graph generation from dataset.#
#########################################

# generates a graph in ./Graphs/average-transactions-per-block-1000000-1310000
