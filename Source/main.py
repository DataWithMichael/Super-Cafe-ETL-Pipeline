import file_handling

branches = ["Chesterfield", "Leeds", "Uppingham"]

print("Which branch do you want to access? \n")

for branch in branches:
    print(branch)

num = int(input("\nMake your selection now: "))

print(file_handling.get_data(num))

