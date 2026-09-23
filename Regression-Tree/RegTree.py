# Regression Tree
students = [
    ["S1", 2, 40, 45],
    ["S2", 3, 45, 50],
    ["S3", 4, 50, 55],
    ["S4", 6, 60, 65],
    ["S5", 7, 65, 70]
]


# Function to calculate Mean
def mean(values):
    return sum(values) / len(values)


# Function to calculate Mean Squared Error
def mse(values):
    avg = mean(values)
    error = 0

    for value in values:
        error += (value - avg) ** 2
    return error / len(values)


# Try different Study Hour splits
best_split = None
best_mse = float("inf")

for split in [2, 3, 4, 5, 6]:
    left = []
    right = []

    for student in students:
        SH = student[1]
        FM = student[3]
        if SH <= split:
            left.append(FM)
        else:
            right.append(FM)

    # Avoid empty groups
    if len(left) == 0 or len(right) == 0:
        continue

    # Calculate weighted MSE
    total = len(left) + len(right)
    weighted_mse = (
        (len(left) / total) * mse(left)
        +
        (len(right) / total) * mse(right)
    )

    print(
        "Split:", split,
        "MSE:", round(weighted_mse, 2)
    )

    # Find best split
    if weighted_mse < best_mse:
        best_mse = weighted_mse
        best_split = split


print("\nBest Split:", best_split)
print("Best MSE:", round(best_mse, 2))


# Create the two groups using best split
left = []
right = []
for student in students:
    SH = student[1]
    FM = student[3]
    if SH <= best_split:
        left.append(FM)
    else:
        right.append(FM)

# Prediction for each group

left_prediction = mean(left)
right_prediction = mean(right)
print("\nLeft group FM:", left)
print("Left prediction:", left_prediction)
print("\nRight group FM:", right)
print("Right prediction:", right_prediction)

# Predict FM for new student
new_SH = 5
if new_SH <= best_split:
    prediction = left_prediction
else:
    prediction = right_prediction
print("\nNew Student Study Hours:", new_SH)
print("Predicted FM:", prediction)
