import file_handling
import transformation

branches = ["Chesterfield", "Leeds", "Uppingham"]

print("Which branch do you want to access? \n")

for branch in branches:
    print(branch)

num = int(input("\nMake your selection now: "))

transformation.transform()

print(file_handling.get_data(num))

