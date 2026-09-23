import math
students = [
    ["S1", 2, 40, 45],
    ["S2", 3, 45, 50],
    ["S3", 4, 50, 55],
    ["S4", 6, 60, 65],
    ["S5", 7, 65, 70]
]

# New student
new_SH = 5
new_AM = 55

K = 3

results = []

for student in students:

    name = student[0]
    SH = student[1]
    AM = student[2]
    FM = student[3]

    distance = math.sqrt(
        (SH - new_SH) ** 2 +
        (AM - new_AM) ** 2
    )

    results.append([
        name,
        SH,
        AM,
        FM,
        distance
    ])


results.sort(key=lambda x: x[4])

print("Student\tSH\tAM\tFM\tDistance\tRank")
print("-" * 55)

for rank, student in enumerate(results, start=1):

    print(
        student[0], "\t",
        student[1], "\t",
        student[2], "\t",
        student[3], "\t",
        round(student[4], 2), "\t\t",
        rank
    )


nearest = results[:K]

total_FM = 0

for student in nearest:
    total_FM += student[3]

predicted_FM = total_FM / K


print("\nK =", K)

print("\nK Nearest Students:")

for student in nearest:
    print(
        student[0],
        "-> Distance:",
        round(student[4], 2),
        "FM:",
        student[3]
    )


print("\nPredicted FM =", predicted_FM)
