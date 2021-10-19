import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt


price_a = np.full(12, 325.)
price_b = np.array([300, 300, 290, 275, 275, 280,
                    260, 250, 230, 200, 210, 190.])
price_c = np.array([100, 110, 98, 115, 200, 220,
                    210, 500, 500, 490, 487, 550.]) # price for every month in CZK

plt.plot(price_a,c='blue',label='A')
plt.plot(price_b,c='red',label='B')
plt.plot(price_c,c='green',label='C')
plt.xlabel("hour")
plt.ylabel("price CZK")
plt.legend()
plt.show()

Items_A = cp.Variable(12)
Items_B = cp.Variable(12)
Items_C = cp.Variable(12)
constraints = [
    Items_A + Items_B + Items_C <= 10000.,  # maximal MW for block
    Items_A >= 2000.,  # minimal MW for block
    Items_B >= 2000.,  # minimal MW for block
    Items_C >= 2000.,  # minimal MW for block
    Items_C[6:] <= 5000.,
    Items_B <= 4500.,
    Items_A[:6] <= 4000.,
]
objective = cp.Maximize(Items_A * price_a + Items_B * price_b +Items_C * price_c)
problem = cp.Problem(objective, constraints)
problem.solve(verbose=True)

plt.plot(Items_A.value,c='blue',label='A')
plt.plot(Items_B.value,c='red',label='B')
plt.plot(Items_C.value,c='green',label='C')
plt.xlabel("month")
plt.ylabel("#Items")
plt.legend()
plt.show()