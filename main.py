import sys
import math
import os
import random


def arguments():
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))


def header(command_line):
    print('Cache Simulator CS 3852 Spring 2019 - Group #15')
    print('\nCmd Line: ', command_line)


# Returns a string of the size in bytes
def determinByteSize(BlockSize):
    sampleSize = BlockSize
    itteration = 0
    byteStringSize = "B"

    while sampleSize > 10:
        sampleSize = sampleSize - 10
        itteration = itteration + 1
        if itteration == 1:
            byteStringSize = "KB"
        elif itteration == 2:
            byteStringSize = "MB"
        elif itteration == 3:
            byteStringSize = "GB"
        elif itteration == 4:
            byteStringSize = "TB"

    sizeInBytes = str(int(pow(2, sampleSize))) + " " + byteStringSize
    return sizeInBytes


# def determineBitSize(CacheSize):

def numberOfSets(cacheSize, blockSize, associativity):
    n = (cacheSize / (blockSize * associativity))

    return n;


def openAFile(TraceFile):
    try:
        Input_File = open(TraceFile, "r")
    except:
        print("\n error: We cannot find " + TraceFile + ". Are you sure the file exists?\n")

    return Input_File


### MAIN FUNCTION ###

if __name__ == "__main__":

    TraceFile = ""
    CacheSize = 0
    BlockSize = 0
    Associativity = 0
    rPolicy = 0
    clock_Tick = 0

    i = 1
    while( i < len(sys.argv)):
        if(sys.argv[i] == '-f'):
            #scan for .trc file
            #while(sys.argv[i+1][:4] != ".trc"):
            #    print("no trc: "  + sys.argv[i+1][4:])
            #    i += 1

            TraceFile = sys.argv[i+1]
        elif(sys.argv[i] == '-s'):
            CacheSize = int(sys.argv[i+1]) * 1024
        elif(sys.argv[i] == '-b'):
            BlockSize = int(sys.argv[i+1])
        elif(sys.argv[i] == '-a'):
            Associativity = int(sys.argv[i+1])
        elif(sys.argv[i] == '-r'):
            rPolicy = sys.argv[i+1]
        i = i + 1

    if(TraceFile == ""):
        print("please enter parameters")
        quit()

    Offset = math.log(BlockSize) / math.log(2)


    print("Trace File:    ", TraceFile)
    print("\nGeneric:")
    print("Cache Size:    ", str(int(CacheSize / 1024)), "KB")
    print("Block Size:    ", str(BlockSize), "Bytes")
    print("Associativity: ", str(Associativity))
    print("R-Policy:      ", rPolicy)

    # Caclualate values
    total_Num_Blocks = determinByteSize(BlockSize)
    numSetBits = int(math.log(numberOfSets(CacheSize, BlockSize, Associativity)) / math.log(2))
    tagBits = int(32 - numSetBits - Offset)
    overheadMemory = (((tagBits + 1) * Associativity) * (math.pow(2, numSetBits) / 8))
    overheadMemoryInBytes = determinByteSize(math.log(int(overheadMemory)) / math.log(2))
    totalMemory = CacheSize + overheadMemory

    # end of value calculations

    print("\n----- Calculated Values -----")
    print("Total #Blocks: " + str(total_Num_Blocks) + " ( 2^" + str(BlockSize) + " )")
    print("Index bits:    " + str(numSetBits) + " bits, Total Indices: " + determinByteSize(numSetBits))
    print("Tag Size:      " + str(tagBits) + " bits")
    print("Overhead Memory Size:       " + str(overheadMemory) + " ( or " + overheadMemoryInBytes + " )")
    print("Implementation Memory Size: " + str(int(totalMemory)) + " ( or " + str(int(totalMemory / 1024)) + " KB )")

    # open the trace file

    NewTraceFile = "./TraceFiles/" + TraceFile
    TraceFile = NewTraceFile

    Input_File = (openAFile(TraceFile))

    Data_From_File = Input_File.read().split('\n')
    Cleaned_Data_Odd = []
    Cleaned_Data_Even = []

    i = 0

    for Data in Data_From_File:
        if Data != '':
            if (i % 2) == 1:
                Cleaned_Data_Odd.append(Data)
            if (i % 2) == 0:
                Cleaned_Data_Even.append(Data)
            i = i + 1

    Addresses_Of_Instructions = []
    Number_Of_Bytes_In_Instruction = []
    DstM = []
    Number_Of_Bytes_In_Instruction_DstM = []
    SrcM = []
    Number_Of_Bytes_In_Instruction_SrcM = []
    Number_Of_Bytes_In_Instruction_Total = []

    for Data in Cleaned_Data_Even:
        Entries = Data.split(' ')
        Addresses_Of_Instructions.append(Entries[2])
        Number_Of_Bytes_In_Instruction.append((Entries[1])[1:3])

    i = 0
    for Data in Cleaned_Data_Odd:
        Entries = Data.split(' ')
        Number_Of_Bytes_In_Instruction_Total.append(Number_Of_Bytes_In_Instruction[i])
        DstM.append(Entries[1])
        Number_Of_Bytes_In_Instruction_Total.append('04')
        SrcM.append(Entries[7])
        Number_Of_Bytes_In_Instruction_Total.append('04')
        i = i + 1

    #print("\nAddresses of instructions: ", Addresses_Of_Instructions)
    #print("Number of bytes in instruction: ", Number_Of_Bytes_In_Instruction_Total)
    #print("DstM: ", DstM)
    #print("SrcM: ", SrcM)

    #TODO: linearly store every single hex numbers
    i = 0
    All_Hex_Numbers = []
    while i < len(Addresses_Of_Instructions):
        All_Hex_Numbers.append(Addresses_Of_Instructions[i])
        All_Hex_Numbers.append(DstM[i])
        All_Hex_Numbers.append(SrcM[i])
        i = i + 1

    All_Hex_Numbers_Clean = []
    Number_Of_Bytes_In_Instruction_Clean = []
    i = 0

    while i < len(All_Hex_Numbers):
        if All_Hex_Numbers[i] != '00000000':
            All_Hex_Numbers_Clean.append(All_Hex_Numbers[i])
            Number_Of_Bytes_In_Instruction_Clean.append(Number_Of_Bytes_In_Instruction_Total[i])
        i = i + 1

    #print("Number of bytes in instruction: ", Number_Of_Bytes_In_Instruction_Clean)

    #print("Clean Hex: ", All_Hex_Numbers_Clean)



    Decimal_List = []
    Binary_List = []
    Formatted_Binary_List = []

    # uncomment for part 2
    #for hexNum in All_Hex_Numbers_Clean:
    #    Decimal_List.append(int(hexNum,16))
    #    Binary_List.append(bin(int(hexNum,16)).split('b')[1])

    #uncomment for part 2

    #print("Decimal List: ", Decimal_List)
    #print("Binary List: ", Binary_List)

    #Uncomment for part 2


#TODO: build the cache from data, and then???? check source addresses against the cache and fill up cache with tags,

#TODO: grab CPI and Cash_Hit_Rate from the hit and miss counter. and the count of the total number of trials


# Results values - part 2 work
Cache_Hit_Rate = "***"
CPI = "***"

# END OF RESULT VALUE CALCULATIONS



#i = 0
#while i < 20:
#    print("0x" + All_Hex_Numbers_Clean[i] +
#          ": (" + Number_Of_Bytes_In_Instruction_Clean[i] + ")")
#    i = i + 1


if(os.path.exists("trace_output_5.txt")):
    os.remove("trace_output_1.txt")
    os.remove("trace_output_2.txt")
    os.remove("trace_output_3.txt")
    os.remove("trace_output_4.txt")
    os.remove("trace_output_5.txt")

if not os.path.exists("trace_output_1.txt"):
    output_filename = "trace_output_1.txt"
elif not os.path.exists("trace_output_2.txt"):
    output_filename = "trace_output_2.txt"
elif not os.path.exists("trace_output_3.txt"):
    output_filename = "trace_output_3.txt"
elif not os.path.exists("trace_output_4.txt"):
    output_filename = "trace_output_4.txt"
elif not os.path.exists("trace_output_5.txt"):
    output_filename = "trace_output_5.txt"

with open(output_filename, "w") as outfile:

    outfile.write('Cache Simulator CS 3852 Spring 2019 - Group #15')
    outfile.write('\n\nCmd Line: ' + str(sys.argv))

    outfile.write("\n\nTrace File:    " + TraceFile)
    outfile.write("\nGeneric:")
    outfile.write("\nCache Size:    " + str(int(CacheSize / 1024)) + "KB")
    outfile.write("\nBlock Size:    " + str(BlockSize) + "Bytes")
    outfile.write("\nAssociativity: " + str(Associativity))
    outfile.write("\nR-Policy:      " + rPolicy)

    outfile.write("\n\n----- Calculated Values -----")
    outfile.write("\nTotal #Blocks: " + str(total_Num_Blocks) + " ( 2^" + str(BlockSize) + " )")
    outfile.write("\nIndex bits:    " + str(numSetBits) + " bits, Total Indices: " + determinByteSize(numSetBits))
    outfile.write("\nTag Size:      " + str(tagBits) + " bits")
    outfile.write("\nOverhead Memory Size:       " + str(overheadMemory) + " ( or " + overheadMemoryInBytes + " )")
    outfile.write("\nImplementation Memory Size: " + str(int(totalMemory)) + " ( or " + str(int(totalMemory / 1024)) + " KB )")



    #i = 0
    #while i < 20:
    #    outfile.write("0x" + All_Hex_Numbers_Clean[i] +
    #          ": (" + Number_Of_Bytes_In_Instruction_Clean[i] + ")\n")
    #    i = i + 1

    #TODO: Counter for hit

    #TODO: Calculate hit and miss rates (percentage across all points)

    i = 0
    newCache = []

    #Cache set size control and indexes
    while i < pow(2,numSetBits):
        newCache.append([i])
        i = i + 1

    #Set association block creation fills in the cache with all 0's
    i = 0
    while i < pow(2,numSetBits):
        j = 0
        while j < Associativity:
            newCache[i].append([0,0,0,0,0])
            j = j + 1
        i = i + 1
    i = 0

    total_Num_Of_Addresses = 0
    for hexNum in All_Hex_Numbers:
        total_Num_Of_Addresses = total_Num_Of_Addresses + 1

    total_Num_Of_Instructions = total_Num_Of_Addresses / 3

    #print(total_Num_Of_Addresses)
    #print(int(total_Num_Of_Instructions))


    # uncomment for part 2
    for hexNum in All_Hex_Numbers:
        Decimal_List.append(int(hexNum,16))
        Binary_List.append(bin(int(hexNum,16)).split('b')[1])

    #uncomment for part 2

    #print("Decimal List: ", Decimal_List)
    #print("Binary List: ", Binary_List)

    # hit counter
    hit = 0
    tried = 0

    # Uncomment for part 2
    j = 0
    #print(Binary_List)
    r = 0
    count = 0

    #for binary in Binary_List:
    #        print(binary)

    #New_Binary_List = []
    #for binary in Binary_List:
    #    if binary != '0':
    #        print("before: " + binary)
    #        originalBinary = binary
    #        i = 0
    #        while i < (32-len(originalBinary)):
    #            binary = "0" + binary
    #            i = i + 1
    #        print("after : " + binary)
    #        New_Binary_List.append

    #for numbytes in Number_Of_Bytes_In_Instruction_Total:
    #    print(numbytes)


    for binary in Binary_List:
        if binary != '0':
            i = 0
            originalBinary = binary
            while i < (32-len(originalBinary)):
                binary = "0" + binary
                i = i + 1

            #print(binary)
            #print("tag: " + binary[:tagBits] + " index: " + binary[tagBits:tagBits+numSetBits] + " offset: " + binary[tagBits+numSetBits:])
            #print("tag: " + hex(int(binary[:tagBits],2)) + " index: " + hex(int(binary[tagBits:tagBits+numSetBits],2)) + " offset: " + hex(int(binary[tagBits+numSetBits:],2)))
            #print("\n")

    #print(str(len(Number_Of_Bytes_In_Instruction_Total)))
    count = 0
    for binary in Binary_List:
        #print("[" + str(count) + "]: " + binary)
        count = count + 1

    r = 0
    cpi = 0
    total_cpi = 0
    average_cpi = 0
    originalBinary = 0
    for binary in Binary_List:
        if binary != '0':
            originalBinary = binary
            i = 0
            while i < (32-len(originalBinary)):
                binary = "0" + binary
                i = i + 1




        if r % 3 == 0:
            total_cpi += cpi
            cpi = 0
        if binary != '0':
            cpi += 2
            #TODO: send binary to cache to check if hit/miss

            #TODO: if miss then do miss things:

            #print("list index: " + str(r))
            #print(binary[tagBits+numSetBits:])
            instruction_size_plus_block_offset = int(binary[tagBits+numSetBits:],2) + int(Number_Of_Bytes_In_Instruction_Total[r])
            number_of_runs = (instruction_size_plus_block_offset // BlockSize) + 1

            a = 0
            while a < number_of_runs:
                # while
                k = 0
                while k < Associativity:
                    tried = tried + 1
                    hexVal = hex(int(binary[:tagBits], 2))
                    index = int(binary[tagBits:tagBits + numSetBits], 2) + a
                    # index = pow(2,numSetBits) - 1

                    # print ("block: " + k + " index: " + index)
                    if (a > 0) and (index >= pow(2, numSetBits) - 1):
                        index = 0

                    if(index == 32768):
                        print(index)
                    if(index == 32767):
                        print(newCache[index])

                    # If valid = 0, it counts as a miss. compulsory miss
                    if newCache[index][k + 1][0] == 0:
                        clock_Tick = clock_Tick + 1
                        newCache[index][k+1][3] = clock_Tick;

                        newCache[index][k + 1][1] = hexVal
                        newCache[index][k + 1][0] = 1
                        k = 0
                        cpi += 3 * (BlockSize / 4)
                        #print(newCache[index])
                        break
                    else:
                        # TODO: CHECK THE TAG

                        # if the tags match
                        if (newCache[index][k + 1][1] == hexVal):
                            # print("I found a match!: " + hex(int(binary[:tagBits],2)))
                            # TODO: if hit then do hit things: 1 + 2
                            hit = hit + 1
                            cpi = cpi + 1
                            k = 0
                            #keep track of how many times this guys is hit for LRU
                            if(rPolicy == "LRU"):
                                clock_Tick += 1
                                newCache[index][k+1][3] = clock_Tick
                            break
                        else:
                            # MISS
                            if k == Associativity - 1:
                                clock_Tick = clock_Tick + 1
                                if (rPolicy == "LRU"):
                                    newCache[index][k + 1][3] = clock_Tick
                                ## THE BLOCKS ARE FULL
                                # Conduct Replacement:
                                if rPolicy == "RR":
                                    smallest_block = 0
                                    smallest_count = 9999999999999
                                    oIndex = 1
                                    while oIndex < Associativity + 1:
                                        if newCache[index][oIndex][3] < smallest_count:
                                            #print("in cache: " + str(newCache[index][oIndex][3]) + " smallest_count: " + str(smallest_count))
                                            smallest_count = newCache[index][oIndex][3]
                                            smallest_block = oIndex
                                        oIndex = oIndex + 1
                                    #print("INDEX: " + str(newCache[index]))
                                    #print("SMALLEST BLOCK: " + str(newCache[index][smallest_block]))


                                    #print("What is here?: " + str(newCache[index][smallest_block][1]))
                                    newCache[index][smallest_block][1] = hexVal

                                    #replace the count
                                    newCache[index][smallest_block][3] = clock_Tick

                                    #check to see which block has the lowest count value
                                    #print(newCache[index])
                                    #print(rPolicy)
                                elif rPolicy == "R":
                                    #implement random policy
                                    clock_Tick = clock_Tick + 1
                                    block_number = random.randint(1,Associativity)

                                    newCache[index][block_number][1] = hexVal

                                    #replace the count
                                    newCache[index][block_number][3] = clock_Tick

                                    #print(newCache[index])
                                    #print(rPolicy)
                                elif rPolicy == "LRU":
                                    #print(clock_Tick)
                                    #print(newCache[index])
                                    smallest_block = 0
                                    smallest_count = 9999999999999
                                    oIndex = 1
                                    while oIndex < Associativity + 1:
                                        if newCache[index][oIndex][3] < smallest_count:
                                            # print("in cache: " + str(newCache[index][oIndex][3]) + " smallest_count: " + str(smallest_count))
                                            smallest_count = newCache[index][oIndex][3]
                                            smallest_block = oIndex
                                        oIndex = oIndex + 1
                                    # print("INDEX: " + str(newCache[index]))
                                    # print("SMALLEST BLOCK: " + str(newCache[index][smallest_block]))

                                    # print("What is here?: " + str(newCache[index][smallest_block][1]))
                                    newCache[index][smallest_block][1] = hexVal

                                    # replace the count
                                    clock_Tick = clock_Tick + 1
                                    newCache[index][smallest_block][3] = clock_Tick
                                    #print(newCache[index])
                            else:
                                cpi += 3 * (BlockSize / 4)
                    k = k + 1
                a = a + 1

        r = r + 1
    average_cpi = total_cpi / total_Num_Of_Instructions;
    #print(average_cpi)




    #while i < pow(2,numSetBits):
    #    if(newCache[i][1] != 0):
    #        print(newCache[i])
    #    i = i + 1

    #print(newCache[0])
    #print(newCache[len(newCache)-1])

    Cache_Hit_Rate = (hit/tried) * 100
    #print("hit count: " + str(hit) + " tries: " + str(tried) + " hit rate = " + str(Cache_Hit_Rate) + "%")

    print("\n----- Results -----")
    print("Cache Hit Rate:  %.2f" % Cache_Hit_Rate + "%")
    print("CPI: %.2f" % average_cpi + " cycles/instruction\n")

    outfile.write("\n\n----- Results -----")
    outfile.write("\nCache Hit Rate: %.2f" % Cache_Hit_Rate + "%")
    outfile.write("\nCPI: %.2f" % average_cpi + " cycles/instruction\n\n")

    #TODO: CPI - find notes on CPI and implement formula
    #TODO: Calculate frequencies based off the text files that we are using.
    #TODO: Categorize across ALU, Read, Write, Branches, and other
    #TODO: ALU - arithmetic logic, (AND OR)
    #TODO: Read - mov ax,[ebp+0x8]
    #TODO: write -
    #TODO: Branches -
    #TODO: Other -

    #TODO: run the information 5 times using different input paramters each time.