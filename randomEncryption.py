import random
import math
import string
# import zlib
# import sys

globalKey = ""
addedNumbers = []
globalKeyRandomPrime = ""  # stores the n in the nth prime, turnBlockToRandomPrimes
globalKeyAddedNumberInRandomPrime = ""  # stores how much is added while rounding to the next prime

operator = ""
operand = 0

compressed = 0  # Fix the decompression and delete this

mean = 0  # Global variable
maxim = 0  # Global variable

# TODO: Shuffle the order of the chars in digs and save it in key, adds too much complexity to brute force
# digs = 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.
# used to convert large numbers into a compressed string_input representation
# Length: 62
digs = string.digits + string.ascii_letters


# Check if the number_input m is prime
def is_prime(m):
    n = int(m)
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i <= math.sqrt(n):
        if n % i == 0:
            return False
        i = i + 2
    return True


# Generate prime number endlessly
def prime_generator():
    n = 1
    while True:
        n += 1
        if is_prime(n):
            yield n


# Round the number to the next closest prime number, even the number is already a prime
def roundToNextPrime(number):
    number = number + 1
    while not is_prime(int(number)):
        number += 1
    return number


# Swap the first half bits and last half bits (n is a number_input)
def swapBits(n):
    return ((0x0000FFFF & n) << 16) + ((0xFFFF0000 & n) >> 16)


# Generate random integer between 1-5
# You can make the interval greater to make the encryption stronger
# but it will slow down the algorithm
def generateRandomNumber():
    return random.randint(1, 5)


# Takes a string and converts its every char to int and then reverses the bit positions of all chars,
# input is the plaintext like flag{abc123}
# Output format: number_input.number_input.number_input. like 1.2.3.
def reverseBitsOfStringCharByChar(string_input):
    result = ""
    plaintextAsUnicode = ""  # DEBUG
    for char in string_input:
        number = ord(char)
        plaintextAsUnicode += str(number) + "."  # DEBUG
        # print(number)
        reversedNumber = reverseBits(number, 32)  # type is int
        result += str(reversedNumber) + "."
    print(f"Plaintext As Unicode: {plaintextAsUnicode}")  # DEBUG
    return result


# reverse of reverseBitsOfStringCharByChar, takes a string_input like 51.27.67. and turns it into string characters
def restoreOrderOfBitsCharByChar(string_input):
    listOfNumbers = str(string_input).split(".")
    # print(f"        ListOfNumbers: {listOfNumbers }")
    plaintextAsUnicode = ""
    for number in listOfNumbers:
        if number != "":
            # print(f"      current number_input: {number}")
            number = int(number)
            # print(f"          int(number_input): {number}")
            reversedNumber = reverseBits(number, 32)
            # print(f"          reversedNumber: {reversedNumber}")
            plaintextAsUnicode += str(reversedNumber) + "."
            # print(f"          plaintextAsUnicode: {plaintextAsUnicode}")
    # print(f"Plaintext As Unicode: {plaintextAsUnicode}")  # DEBUG
    return plaintextAsUnicode


# Reverses the bits of an integer
def reverseBits(num, bit_size=32):
    # output will be like bin(10) = '0b10101'
    binary = bin(num)
    # skip first two characters of binary
    # representation string_input and reverse
    # remaining string_input and then append zeros
    # after it. binary[-1:1:-1]  --> start
    # from last character and reverse it until
    # second last character from left
    reverse = binary[-1:1:-1]
    reverse = reverse + (bit_size - len(reverse)) * '0'
    # converts reversed binary string_input into integer
    return int(reverse, 2)


# Converts the string_input 1.2.3. to  abc
def numberToUnicodeStr(string_input):
    result = ""
    temp_list = str(string_input).split(".")
    for elem in temp_list:
        if elem != "":
            result += chr(int(elem))
    return result


# Pick a random operation (add/subtract) and apply it with a random number_input on each block
# TODO: The generated number_input had 2 digits before, do 3. Last 2 digits will be multiplied and used as operand.
def applyRandomOperationOnBlocks(string_input):  # input: 1.2.3. etc.
    result = ""
    tempList = str(string_input).split(".")
    # print(f"     tempList: {tempList}")
    # Decide which operator (if first digit is 0 -> add, if 1 -> subtract. Second digit is the operand to be applied)
    # Examples: 05 -> add 5, 13 -> subtract 3
    generatedNumber = random.randint(10, 21)  # between 10 - 20  # OLD
    global operand
    global operator
    operatorTmp = str(generatedNumber)
    operator = operatorTmp[0]
    # print(f"     operator (0 -> Add, 1 -> Subtract): {operator}")
    operand = int(operatorTmp[1])
    # print(f"     operand (Value to be applied): {operand}")
    for elem in tempList:
        if elem != "":
            number = int(elem)
            # print(f"     Current block number_input: {number_input}")
            if operator == "0":  # add
                number += operand
            else:  # sub
                number -= operand
            # print(f"     Current block number_input after operation: {number_input}")
            result += str(number) + "."
            # print(f"     Current result: {result}")
    return result


# Reverse all the random operations done by applyRandomOperationOnBlocks() using the saved key
def reverseRandomOperationOnBlocks(string_input, operator_input, operand_input):
    print(f"string: {string_input}, operator: {operator_input}, operand: {operand_input}")
    result = ""
    tempList = str(string_input).split(".")
    for elem in tempList:
        if elem != "":
            number = int(elem)
            if operator_input == "0":  # add operation was selected, reverse it by subtracting
                number -= int(operand_input)
            else:  # sub was selected
                number += int(operand_input)
            result += str(number) + "."
    return result


# Round all of the blocks to the next prime number_input
def roundBlocksToPrime(encrypted):
    length = len(encrypted)
    global addedNumbers
    if type(input) == list:
        addedNumbers = [0 for _ in range(length - 1)]
        result = [0 for _ in range(length - 1)]
        index = 0
        for block in encrypted:
            if block != "":
                # print(f"index: {index}")
                # rounded += str(roundToNextPrime(int(block))) + "."
                generatedPrim = roundToNextPrime(int(block))
                result[index] = generatedPrim
                addedNumbers[index] = generatedPrim - int(block)
                # print(f"result in for: {result}")
            index = index + 1
    else:
        listOfBlocks = str(encrypted).split(".")
        addedNumbers = [0 for _ in range(len(listOfBlocks) - 1)]  # Key as global variable?
        # print(f"listOfBlocks: {listOfBlocks}")
        result = [0 for _ in range(len(listOfBlocks) - 1)]
        # print(f"result: {result}")
        rounded = ""
        index = 0
        for block in listOfBlocks:
            if block != "":
                # print(f"index: {index}")
                rounded += str(roundToNextPrime(int(block))) + "."
                result[index] = str(roundToNextPrime(int(block)))
                addedNumbers[index] = roundToNextPrime(int(block)) - int(block)
                # print(f"result in for: {result}")
            index = index + 1
            # print(f"rounded: {rounded}")
        # print(f"result: {result}")
        # return rounded
        # print(f"addedNumbers: {addedNumbers}")
    return result


# Multiply the prime number_input with its index
def combinePrimeBlocks(prime_blocks):
    index = 1
    combinedBlock = [0 for _ in range(len(prime_blocks))]
    for block in prime_blocks:
        combinedBlock[index - 1] = int(block) * index
        index = index + 1
    return combinedBlock


# should be renamed as DecryptCombinedBlocks
# Reverses the multiply done by combinePrimeBlocks() by finding a divisible factor
def decryptCombinedBlocks(combined_blocks):
    length = len(combined_blocks)
    result = [0 for _ in range(len(combined_blocks))]
    index = length
    # print(f"length: {range(length+1)}")  # + 1 bcs range excludes (stops at) last element
    for block in combined_blocks:
        # go from length to 1 bcs 1 should be checked last, every number_input is a factor of 1
        for i in reversed(range(length + 1)):
            if i == 0:
                continue
            # print(f"i: {i}")
            if (int(block) % i) == 0:
                blockDivided = int(block) // i
                # print(f"{i}. Number is {blockDivided}")
                result[i - 1] = blockDivided
                break
        index = index - 1
    return result


# Get the Encrypted text
def subtractAddedNumbersFromBlock(combined_blocks):
    length = len(combined_blocks)
    result = [0 for _ in range(length)]
    index = 0
    for block in combined_blocks:
        result[index] = int(block) - addedNumbers[index]
        index = index + 1
    return result


# Write the encrypted (its a list) content in a text file
def writeEncryptedFile(encrypted):
    content = ""
    for elem in encrypted:
        content += str(elem) + "."
    with open("encrypted.txt", "w") as f:
        f.write(content)


# Write the content into nameOfFile
def writeIntoFile(name_of_file, content):
    with open(name_of_file, "w", encoding="utf-8") as f:
        f.write(content)


# shuffle the numbers order in the encrypted text
def shuffleBlocks(block):
    return random.sample(block, len(block))


# Reverses the multiply done by combinePrimeBlocks() by finding a divisible factor
def unshuffleBlocks(block):
    # print(f"     @@@@@@@@ Unshuffled Blocks Input: {block}")  # Debug
    # print(f"     @@@@@@@@ length: {len(block)}")  # Debug
    length = len(block)
    result = [0 for _ in range(len(block))]
    index = length
    foundFactors = [0 for _ in range(length + 1)]  # DEBUG and optimize for loop
    # print(f"length: {range(length+1)}")  # + 1 bcs range excludes (stops at) last element
    for elem in block:
        # print(f"  Checking {elem}:")
        # Can be optimized by skipping the already checked i's
        # Go from length to 1 bcs 1 should be checked last, every number_input is a factor of 1
        for i in reversed(range(length + 1)):
            # print(f"    Current i: {i}")
            if i in foundFactors:
                # print(f"    @@ Factor {i} was already used, skipping")
                i -= 1
                continue
            if i == 0:
                continue
            if (int(elem) % i) == 0:
                foundFactors[i] = i
                blockDivided = int(elem) // i
                # print(f"    {i}. Number: {elem} is divisible by {i}, result: {blockDivided}")
                result[i - 1] = blockDivided  # index instead of i?
                break
        index = index - 1
    # print(f"    Result of Unshuffled (None should 0 or 1): {result}")
    return result


# Find the maximum of a list
def findMax(blocks):
    return max(blocks)


# Returns the biggest value of the list, regardless of the sign. So -5 is bigger than 4 with this.
# Used when the average of list is subtracted and possibly generated negative values,
# but we shouldn't allow negative values since the next prime cant work with negative values.
def maxAbs(blocks):
    res = [elem * (-1) for elem in blocks]
    return max(res)


# Find the average value of list
# TODO: Risk: returned value can be a float
def returnAverage(blocks):
    return sum(blocks) // len(blocks)


# Subtract the mean from all blocks
def subtractMeanFromAllBlocks(blocks):
    new_list = [x - returnAverage(blocks) for x in blocks]
    return new_list


# Subtract the number_input from all blocks
def subtractNumberFromAllBlocks(blocks, number):
    # print(f"        Input: {blocks} , number to subs: {number}")
    new_list = [int(x) - int(number) for x in blocks]
    # print(f"        Output: {new_list}")
    return new_list


# Add the number_input to all blocks
def addNumberToAllBlocks(blocks, number):
    new_list = [x + int(number) for x in blocks]
    return new_list


# Returns the nth next prime number_input close to the given number_input
def generateNextNthPrime(number, n):
    nthPrime = number
    for i in range(n):
        nthPrime = roundToNextPrime(nthPrime)
    return nthPrime


# Turn every list element to a next random prime,
# which random number_input is selected will be stored as a key
# in global variable globalKeyRandomPrime
def turnBlockToRandomPrimes(block):
    result = block
    global globalKeyRandomPrime  # stores the n part of the "next nth prime number_input"
    globalKeyRandomPrime = ""
    global globalKeyAddedNumberInRandomPrime
    globalKeyAddedNumberInRandomPrime = ""
    index = 0
    for element in block:
        rnd = generateRandomNumber()
        globalKeyRandomPrime += str(rnd) + "."
        result[index] = generateNextNthPrime(element, rnd)
        # print(f"\n  generated random: {rnd}\n  generateNextNthPrime: {result[index]}\n  element: {element}")  #  Debug
        globalKeyAddedNumberInRandomPrime += str(result[index] - element) + "."
        index = index + 1
    # print(f"Generated globalKeyRandomPrime: {globalKeyRandomPrime}")  #  Debug
    # print(f"Generated globalKeyAddedNumberInRandomPrime: {globalKeyAddedNumberInRandomPrime}")  #  Debug
    return result


# Turn Blocks to their original values before they were rounded to the primes,
# use the key file, reverse of turnBlockToRandomPrimes()
def turnRandomPrimesToOriginal(block):
    result = [0 for _ in range(len(block))]  # create empty result list

    keyFile = open("Key.txt", "r")
    keyContent = keyFile.read()
    # print(f"Key Content: {keyContent}")

    # Take the String part after P and delete the ":" and ")" and convert to a list separated by "."
    temp = keyContent.split("P")[1].replace(":", "").replace(")", "").split(".")
    addedPrimes = [x for x in temp if x != ""]  # Remove the last blank element ""
    print(f"  Added Primes: {addedPrimes}")

    index = 0
    for elem in block:
        # print(f"Current Element: {elem}")
        # print(f"Current addedPrimes({index}): {addedPrimes[index]}")
        result[index] = int(elem) - int(addedPrimes[index])
        index = index + 1
    # print(f"Subtracted Primes: {result}")

    return result


def readOperandFromKey(key_path):
    keyFile = open(key_path, "r")
    keyContent = keyFile.read()
    result = keyContent.split("S")[1].split(")")[0].replace(":", "")  # .replace(")", "").split(".")
    print(f"  Reading Operand (Operator(0: add, 1: sub), Operand ): {result}")
    return result[1]


def readOperatorFromKey(key_path):
    keyFile = open(key_path, "r")
    keyContent = keyFile.read()
    result = keyContent.split("S")[1].split(")")[0].replace(":", "")  # .replace(")", "").split(".")
    # print(f"Reading Operator: {result}")
    return result[0]


def readBlockLengthFromKey(key_path):
    keyFile = open(key_path, "r")
    keyContent = keyFile.read()
    # print(f"Key Content: {keyContent}")

    # Take the String part after M and delete the part before ), remove the ":"
    result = keyContent.split("B")[1].split(")")[0].replace(":", "")  # .replace(")", "").split(".")
    # addedPrimes = [number_input for number_input in temp if number_input != ""]  # Remove the last blank element ""
    # print(f"mean: {result}")
    return result


def readAverageFromKey(key_path):
    keyFile = open(key_path, "r")
    keyContent = keyFile.read()
    # print(f"Key Content: {keyContent}")

    # Take the String part after M and delete the part before ), remove the ":"
    result = keyContent.split("A")[1].split(")")[0].replace(":", "")  # .replace(")", "").split(".")
    # addedPrimes = [number_input for number_input in temp if number_input != ""]  # Remove the last blank element ""
    # print(f"mean: {result}")
    return result


def readMaxFromKey(key_path):
    keyFile = open(key_path, "r")
    keyContent = keyFile.read()
    # print(f"Key Content: {keyContent}")
    # Take the String part after M and delete the part before ), remove the ":"
    result = keyContent.split("M")[1].split(")")[0].replace(":", "")  # .replace(")", "").split(".")
    # addedPrimes = [number_input for number_input in temp if number_input != ""]  # Remove the last blank element ""
    # print(f"Max Value: {result}")
    return result


# Multiplies all the block elements with their indexes, here index begins from 1
# because multiplication with 0 would erase the first number_input
def multiplyBlockByTheirIndexes(block):
    result = block
    for i in range(len(block)):  # i starts from 0, goes to 14, block length is 15
        result[i] = block[i] * (i + 1)
    return result


# reverse of multiplyBlockByTheirIndexes
# input is: [prime_1*index_1, prime_2*index_2, ..]
def divideBlocks(block):
    result = block
    # i starts from 0, goes to 14, block length is 15
    for i in range(len(block)):
        result[i] = block[i] // (i + 1)
    return result


# Turns a string_input like "1.2.3.4." into a list: [1,2,3,4]
def turnStringWithDelimiterIntoList(string_input, delimiter):  # delimiter = "."
    tempList = string_input.split(delimiter)
    result = [0 for _ in range(len(tempList) - 1)]  # -1 Bcs the keys end with . which makes an empty list element
    index = 0
    for elem in tempList:
        if elem != "":
            result[index] = int(elem)
        index += 1
    return result


# Turns a list like [1,2,3,4] into a string_input "1.2.3.4."
def convertListIntoSeparatedString(list_input):
    result = ""
    for elem in list_input:
        result += str(elem) + "."
    return result


# Takes a number_input number_input, and base (base < digs(len))
# Modified version of this:
# https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-to-a-string-in-any-base
def intToCustomBase(number_input, base):
    # print(f"number: {number_input}")
    # print(f"base:   {base}")
    if number_input < 0:
        sign = -1
    elif number_input == 0:
        return digs[0]
    else:
        sign = 1
    number_input *= sign
    digits = []
    while number_input != 0:  #
        # print(f"  New number: {number_input}")
        # print(f"    number % base = {number_input} % {base} = {number_input % base}")
        # print(f"    digs[number % base] = digs[{number_input % base}] = {digs[number_input % base]}")
        digits.append(digs[number_input % base])
        # print(f"    digits: {digits}")
        number_input = number_input // base
        # print(f"    number = number // base = {number_input} // {base} = {number_input}")
    if sign < 0:
        digits.append('-')
    digits.reverse()
    # print(f"    digits reversed: {digits}")
    return ''.join(digits)


# Reverses the intToCustomBase(number_input, base) function
def CustomBaseToInt(string_input, base):
    # print(f"string_input: {string_input}")
    # print(f"base: {base}")
    tmp_string = string_input
    sign = 1
    result = 0
    if tmp_string[0] == "-":
        sign = -1
        tmp_string = tmp_string[1:]  # Remove the - sign if the value was negative
        # print(f"sign deleted: {tmp_string}")
    index = len(tmp_string)
    # print(f"index: {index}")
    for char in tmp_string:
        # print(f" analysing char: {char}")
        found_index = digs.index(str(char))  # If str(char) exists in digs, it returns the lowest index
        # print(f"  found index of {str(char)}: {found_index}")
        result += found_index * pow(base, index - 1)  # index - 1 careful
        # print(f"  adding to result: {found_index} * {base} ^ {index} = {found_index * pow(base, index)}")
        # print(f"  current result: {result}")
        index -= 1
    result = result * sign
    # print(f"  result: {result}")
    return result


# Convert a list of numbers to their custom sting representation
def convertListOfNumbersToCustomBaseString(list_input, base):
    result = ""
    for elem in list_input:
        result += intToCustomBase(elem, base) + "."
    return result


# Reverts the Function convertListOfNumbersToCustomBaseString()
# Input like: abc.123.xyz, Output like: [123, 432, 125]
def convertCustomBaseStringToListOfNumbers(string_input, base):
    temp_str = str(string_input).split(".")
    result = [0] * (len(temp_str) - 1)  # Create empty list
    index = 0
    for elem in temp_str:
        if elem != "":
            result[index] = int(CustomBaseToInt(elem, base))
        index += 1
    return result


# TODO: Delete?
def convertNumberListToASCIIString(block):
    result = ""
    for elem in block:
        result += str(elem).encode("utf-8").decode("utf-8") + "."  # Just saves it as a string_input separated by .
    return result


# TODO: Delete?
def convertASCIIStringToNumberList(string_input):
    temp = str(string_input).split(".")
    result = [x for x in temp if x != ""]
    return result


# Add random 0 or 1 padding at the end of seq till the size is num_bits
def add_padding(seq, num_bits):
    pad_size = num_bits - len(seq)
    # Optional parameter x: If the length is already a multiple of x = 8, no padding
    # if len(seq) % x == 0 and len(seq) > 0:  # an empty sequence will return an 8 bit sequence (all padding)
    result = seq
    if pad_size == 1:
        result = seq + ["_"]
    elif pad_size > 2:
        result = seq + ["_"] + [random.randint(1, 9) for _ in range(pad_size - 1)]
    else:
        print("No padding needed")
    return result


# Add random padding to make it a multiple of 8, and store the added pad length
# at the end so that removing the padding is possible
def addRandomPaddingToString(string_input, pad_length):
    tmp_list = list(string_input)
    resultList = add_padding(tmp_list, pad_length)
    result = "".join(str(e) for e in resultList)
    return result


# Remove the random padding by checking if the string contains "_"
def remove_padding(string_input):
    if "_" in string_input:
        index = string_input.index("_")
        return string_input[0:index]
    else:
        return string_input


# XOR each character of the input_string with a given key.
# key must be an alphanumerical character: [A-Z][a-z][0-9]
def xorStringWithKey(input_string, key):
    length = len(input_string)
    for i in range(length):
        # Select the first element, XOR it with the key,
        # and concatenate it with the unXORed part again.
        # Iterate until all the characters are XORed.
        input_string = (input_string[:i] +
                        chr(ord(input_string[i]) ^ ord(key)) +
                        input_string[i + 1:])
    return input_string


# XOR each character of the input_string with a given key.
# key must be an alphanumerical character: [A-Z][a-z][0-9]
def xorStringWithString(input_string1, input_string2):
    length = len(input_string1)
    result = ""
    if length != len(input_string2):
        print(f"Error: Unequal lengths for xor!")
        return
    for i in range(length):
        result += chr(ord(input_string1[i]) ^ ord(input_string2[i]))
    return result


# TODO: Store these in Key.txt
# TODO: make the 10 an integer parameter
globalXORKey = ["" for _ in range(10)]  # 11 because 10 (Max length of one block) + IV


# Input: abc.123.sdf34e. separate all the blocks and xor them using cbc
# Define a random IV for the first xor and save it in the key file
# TODO: Global key length?
def applyCBC(string_input):
    # The key that will be stored
    key = ["" for _ in range(string_input.count('.') + 2)]  # The key also stores IV and the result at the end (+2)
    # Generate random IV with length 10
    iv = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
    print(f"  Generated IV: {iv}")
    key[0] = iv  # First element of key is IV
    # Convert string_input into list of strings,
    # remove the last element since it will be "" because of the . at the end
    listOfStrings = string_input.split(".")[0:(len(string_input) - 1)]
    # Add padding to the first string block
    paddedFirstString = addRandomPaddingToString(listOfStrings[0], 10)
    # Xor the first block with iv
    xor_result = xorStringWithString(iv, paddedFirstString)
    key[1] = xor_result
    # Xor the rest of the blocks
    for i in range(len(listOfStrings) - 1):  # -1 because first block was xored already
        # pad the operands of xor
        # i+1 because first block is xored with iv
        paddedString = addRandomPaddingToString(listOfStrings[i + 1], 10)
        xor_result = xorStringWithString(xor_result, paddedString)
        key[i + 2] = xor_result
    global globalXORKey
    globalXORKey = key  # [:-1]  # Remove the last key element since its the same as result  # TODO: Optimize later
    print(f"  XOR Key: {key}")
    print(f"  XOR Key length: {len(key)}")
    return xor_result


# reverse of CBC
# Input should be a 10 char long string
# TODO: Fix: Result array is 1 longer than the output, but still works
def reverseCBC(string_input):
    print(f"\n *** Reversing ***  \n")
    global globalXORKey
    # iv = globalXORKey[0]
    length_of_key = len(globalXORKey)
    block_length = length_of_key - 2  # Exclude the result and IV
    print(f"Reverting: {string_input}")
    # length = len(string_input)  # 10?
    result = [""] * (block_length + 1)
    # Reverse XOR and then remove padding
    xor_result = string_input
    for i in range(length_of_key - 1):  # Note: length of globalXORKey is 11
        # m_n with padding calculated
        # Begin: globalXORKey[10], End: globalXORKey[1], i ends at 9
        # number = length - i - 1
        # DON'T XOR WITH LAST KEY ELEMENT BCS ITS EQUAL TO string_input
        xor_result = xorStringWithString(globalXORKey[length_of_key - 1 - i],
                                         globalXORKey[length_of_key - 2 - i])
        # remove padding of m_n
        result[i] = remove_padding(xor_result)  # -2 -> exclude IV and last Key?

    result = result[1:]  # Weird workaround
    # Since we calculated the plaintexts beginning from m_n to m_1, reverse
    result.reverse()
    print(f"Result after reversing: {result}")

    # For a string output:
    resultString = ''.join(str(e) + "." for e in result)
    return resultString


# Encrypt the string_input
# TODO: save the key as base62 format to make it smaller
# TODO: What if compression is applied multiple times: base62 of base62 etc.
# TODO: add the CBC key to key file.
# TODO: save the last number_input blocks as hex and remove the dots because hex numbers have prefix?
# TODO: Fix: max is always the same, make it random
# TODO: add padding + block cipher
# TODO: instead of giving a string_input, also be able to read string_input from a file
def encrypt(string_input, output_path_encrypted):  # Input = "flag{abc123xyz}"

    print("\n   **** Encrypting ****   \n")

    keyPath = "Key.txt"
    keyFileContent = ""  # Key file will be stored at Key.txt

    print(f"Plaintext: \n{string_input}")  # DEBUG

    reversedBits = reverseBitsOfStringCharByChar(string_input)
    print(f"Reversed Bits: {reversedBits}")  # DEBUG

    # Add/subtract a random number_input to the reversedBits
    # so that the mean and average doesnt stay same for all the time
    randomOperations = applyRandomOperationOnBlocks(reversedBits)
    print(f"Applied Random Operation: {randomOperations}")  # DEBUG

    keyFileContent += f"(S:{operator}{operand})"  # S means Sign (Addition or Subtraction in random operation)
    # O means Operand (The value that will be added or subtracted)
    # keyFileContent += f"(O:{operand})"    # Delete

    # Turn "1.2.3.4" to [1,2,3,4]
    blocks = turnStringWithDelimiterIntoList(randomOperations, ".")  # changed from BlockInput
    print(f"String To List: {blocks}")  # DEBUG

    global mean
    global maxim
    average = sum(blocks) // len(blocks)
    mean = average

    keyFileContent += f"(A:{mean})"  # A means average

    # Subtract average from every block element
    subtractedBlocks = subtractNumberFromAllBlocks(blocks, mean)
    print(f"Subtracted Average From Blocks: {subtractedBlocks}")  # DEBUG

    # Find the maximum negative Number of the subtracted list
    maximum = maxAbs(subtractedBlocks)
    print(f"Maximum Abs: {maximum}")  # DEBUG
    print(f"Average: {average}")  # DEBUG
    maxim = maximum

    keyFileContent += f"(M:{maxim})"  # M means maximum

    # adding max to all numbers makes them a positive number_input, smallest ist 1
    added1 = addNumberToAllBlocks(subtractedBlocks, maxim)
    print(f"Added Maximum to All: {added1}")  # DEBUG

    # add the block length to all list member,
    # otherwise, reversing the multiplication with indexes not clear
    blockLength = len(blocks)
    added2 = addNumberToAllBlocks(added1, blockLength)
    print(f"Added Block Length ({blockLength}) to All: {added2}")  # DEBUG

    keyFileContent += f"(B:{blockLength})"  # B means Block length

    # Turn all blocks to the next nth prime, n is random for each number_input and
    # saved in order in the global variable globalKeyRandomPrime as string_input
    # who's values are separated by dot (.)
    nextPrimes = turnBlockToRandomPrimes(added2)
    print(f"Next Primes: {nextPrimes}")  # DEBUG

    # P means Primes (stores the added numbers to acquire the next prime)
    keyFileContent += f"(P:{globalKeyAddedNumberInRandomPrime})"

    # Multiplies all the block elements with their indexes
    multipliedBlocks = multiplyBlockByTheirIndexes(nextPrimes)
    print(f"Multiplied Blocks: {multipliedBlocks}")  # DEBUG

    # Shuffle all blocks in place
    shuffledBlocks = shuffleBlocks(multipliedBlocks)
    print(f"Shuffled Blocks: {shuffledBlocks}")  # DEBUG

    # Convert list to a base 63 string_input representation to compress the size
    # TODO: save base (62) as global variable?
    convertedListToBase62 = convertListOfNumbersToCustomBaseString(shuffledBlocks, 62)
    print(f"Converted List to base63: {convertedListToBase62}")  # DEBUG

    # TODO: Applying CBC makes the bit manipulations recognizable, but XOR key is enormously large,
    # TODO: grows linear with the size of blocks, return the xored parts as result?
    # Pad every string block before cbc
    cbcEncrypted = applyCBC(convertedListToBase62)
    print(f"CBC Encrypted: {cbcEncrypted}")  # DEBUG
    keyFileContent += f"\n(C:{globalXORKey})"  # C CBC XOR Key

    # Save the key file to be able to encrypt the text with this key
    print(f"Key File Content: {keyFileContent}")  # DEBUG
    writeIntoFile(keyPath, keyFileContent)  # Key.txt

    # Write the encrypted text into the file output_path_encrypted
    writeIntoFile(output_path_encrypted, cbcEncrypted)

    # global compressed
    # Compress the file
    # compressed = compressString(asciiString)
    # writeIntoFile("encryptedCompressed.txt", str(compressed))

    return cbcEncrypted


# Decrypt the encrypted file with the generated key
def decrypt(file_name, key_path, output_path_decrypted):  # Call with decryptNew("encryptedCompressed.txt", "Key.txt")

    print("\n   **** Decrypting ****   \n")

    encryptedFile = open(file_name, "r")
    encryptedContent = encryptedFile.read()
    print(f"Content of {file_name} (encryptedContent):\n  {encryptedContent}")

    # Read key
    keyFile = open(key_path, "r")
    keyContent = keyFile.read()
    print(f"Content of {key_path} (Key):\n  {keyContent}")

    # Start Decrypting
    # First decompress
    # global compressed
    # decompressedString = decompressString(compressed)
    # print(f"Decompressed String: {decompressedString}")

    # Deleted after base 62 Implementation
    # Convert ASCII String to a number_input list
    # asciiToNumberList = convertASCIIStringToNumberList(encryptedContent)
    # print(f"asciiToNumberList: {asciiToNumberList}")

    # Reverse the CBC operation which makes the encrypted string a lot larger
    reversedCBC = reverseCBC(encryptedContent)
    print(f"CBC reversed: {reversedCBC}")

    # Convert base x to list of numbers
    convertedBaseXToList = convertCustomBaseStringToListOfNumbers(reversedCBC, 62)
    print(f"Converted Base X to List: {convertedBaseXToList}")  # DEBUG

    # Unshuffle the shuffled blocks
    unshuffledBlocks = unshuffleBlocks(convertedBaseXToList)
    print(f"Unshuffled Blocks: {unshuffledBlocks}")

    # Turn Prime numbers to their original values using the key
    originalNumbers = turnRandomPrimesToOriginal(unshuffledBlocks)
    print(f"Original Numbers: {originalNumbers}")

    # Subtract the block length from all blocks, read block length from the key
    blockLengthFromKey = readBlockLengthFromKey(key_path)
    subtractedLengthFromBlocks = subtractNumberFromAllBlocks(originalNumbers, blockLengthFromKey)
    print(f"Subtracted Length From Blocks: {subtractedLengthFromBlocks}")

    # Read the maximum value from key and subtract it from all blocks
    # Subtract the block length from all blocks
    maxValue = readMaxFromKey(key_path)  # TODO: check if + 1 or -1
    subtractedMaxFromBlocks = subtractNumberFromAllBlocks(subtractedLengthFromBlocks, (int(maxValue)))
    print(f"Subtracted Max From Blocks: {subtractedMaxFromBlocks}")

    # Read mean value from key and add it to all blocks
    averageValue = readAverageFromKey(key_path)
    addAverageToAll = addNumberToAllBlocks(subtractedMaxFromBlocks, averageValue)
    print(f"Add Average To All Blocks: {addAverageToAll}")

    # Return the list as String separated with dots (.)
    decryptedString = convertListIntoSeparatedString(addAverageToAll)
    print(f"Decrypted String: {decryptedString}")

    operatorKey = readOperatorFromKey(key_path)
    operandKey = readOperandFromKey(key_path)
    # print(f"OPERAND: {operandKey}")  # DEBUG
    randomOperations = reverseRandomOperationOnBlocks(decryptedString, operatorKey, operandKey)
    print(f"Reverse Random Operation: {randomOperations}")  # DEBUG

    restoredBits = restoreOrderOfBitsCharByChar(randomOperations)
    print(f"New Plaintext (Restored Bits): {restoredBits}")

    numberToChar = numberToUnicodeStr(restoredBits)
    print(f"Encrypted: \n{numberToChar}")

    writeIntoFile(output_path_decrypted, str(numberToChar))
    return restoredBits


# Driver Code
plaintext = "flag{abc123xyz}"
plaintextLong = "哈哈 ☞ Lorem ipsum dolor sit amet, consetetur sadipscing elitr!\n" \
                "\tsed diam nonumy eirmod tempor invidunt ut labore et dolore magna?\n" \
                "Lorem ipsum dolor sit amet. ⚔ ॐ 𝄠 ☤ ✺ ಠ_ಠ ☣ ☠ ♣ ♛ ☺ "

enc = encrypt(plaintextLong, "encrypted_output.txt")
decrypt("encrypted_output.txt", "Key.txt", "decrypted_output.txt")
