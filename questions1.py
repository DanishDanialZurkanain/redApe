def compress(string):

    result = ""

    counter = 1

    result += string[0]

    for i in range(len(string)-1):
        if(string[i] == string[i + 1]):
            counter += 1
        else:
            if(counter > 1):
                result += str(counter)
            result += string[i+1]
            counter = 1
    if(counter > 1):
        result += str(counter)
    return result

if __name__ == "__main__":
	input = str(input('Enter an string: '))
	print(compress(input))