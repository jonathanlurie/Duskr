
def trace(string):
    with open("traces.txt", "a") as myfile:
        myfile.write(string + '\n')
