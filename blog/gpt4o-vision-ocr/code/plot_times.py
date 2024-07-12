import os
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

np.random.seed(0)
plt.figure(figsize=(10, 6))

for dir_name, label, color in (("img", "Counting via Img", "tab:orange"), ("txt", "Counting via Txt", "tab:blue")):

    durations = []

    for amount in range(11):
        amount *= 100
        durations.append([])

        for result_path in os.listdir(os.path.join("result", dir_name, str(amount))):

            with open(os.path.join("result", dir_name, str(amount), result_path), "r") as file:
                result = json.load(file)

            durations[-1].append(result["duration_ms"])
            print(result["choices"][0]["message"]["content"])

    steps = np.arange(len(durations))
    x = steps.repeat(len(durations[0])).reshape(-1, 1)
    y = np.hstack(durations)

    model = LinearRegression().fit(x, y)
    y_pred = model.predict(steps.reshape(-1, 1))

    for step, duration in zip(steps, durations):
        plt.scatter([step * 100] * len(duration), duration, color=color, alpha=0.6)

    plt.plot(steps * 100, y_pred, color=color, linewidth=2, label=f"{label}: slope = {model.coef_[0]/100:.5f}")

    print(dir_name, durations)
    print(dir_name, [int(xi) for x in durations for xi in x])

plt.legend()

plt.show()
