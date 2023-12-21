def main(fileName):
    instructions = inputFile(fileName)

    instCount = len(instructions)
    instructionsDone, cycleCount, fetchCount, stall1, stall2, stall3 = 0, 0, 0, 0, 0, 0
    currInstCount, f, d, e, m, w = [], [], [], [], [], []
    
    while (instructionsDone < instCount):
        Write_Back(w, cycleCount, instCount)
        if stall3 == 1:
            cycleCount += 1
            stall3 = 0
        Memory(m, cycleCount, instCount)
        if stall2 == 1:
            cycleCount += 1
            stall2, stall3 = 0, 1
        Execute(e, cycleCount, instCount)
        if (fetchCount != 0 and fetchCount < instCount):
            currInstCount = instructions[fetchCount].split(",")
            PrevInst = instructions[fetchCount - 1].split(",")
            if stall1 == 1:
                cycleCount += 1
                stall1, stall2 = 0, 1
            stall1 = Decode(currInstCount, PrevInst, d, cycleCount, instCount, False)
        else:
            stall1 = Decode(instructions[0].split(","), [], d, cycleCount, instCount, True)
        Fetch(f, cycleCount, instCount)
        if not (stall2 == 1 or stall3 == 1):
            cycleCount += 1
        if (stall2 == 1 and stall3 == 1):
            cycleCount -= 1
        if cycleCount > 4:
            instructionsDone += 1
        fetchCount += 1
    emitOutput(f, d, e, m, w, instCount)
    return 0

def Write_Back(wb, cycleCount, instCount):
    if (cycleCount >= 4):
        if (len(wb) < instCount):
            wb += [cycleCount]

def Memory(mem, cycleCount, instCount) :
    if (cycleCount >= 3): 
        if (len(mem) < instCount):
            mem += [cycleCount]
                
def Execute (exe, cycleCount, instCount) :
    if (cycleCount >= 2):
        if (len(exe) < instCount):
            exe += [cycleCount]

def Decode (instruction, previnst, decode, cycleCount, instCount, check):
    if (cycleCount >= 1 and len(decode) < instCount):
        if check:
            decode += [cycleCount] 
            return 0
        else:
            if (previnst[0] == "L"):
                if (instruction[0] == "I" and previnst [1] == instruction[2] and not(previnst [1]  == "0")):
                    decode += [cycleCount]
                    return 1
                elif (instruction[0] == "R" and (previnst[1] == instruction[2] or previnst[1] == instruction[3]) and not(previnst[1] == "0")) :
                    decode += [cycleCount]
                    return 1
                elif (instruction[0] == "L" and (previnst[1] == instruction[3]) and not(previnst[1] == 0)):
                    decode += [cycleCount]
                    return 1
                elif (instruction[0] == "S" and previnst[1] == instruction[3] and not(previnst[1] == "0")):
                    decode += [cycleCount]
                    return 1
                else:
                    decode += [cycleCount] 
                    return 0
            else:
                decode += [cycleCount] 
                return 0

def Fetch(fet, cycleCount, instCount):
    if (cycleCount >= 0 and len(fet) < instCount):
        fet += [cycleCount]

def formatList(list1):
    for x in range(len(list1)):
        if list1[x] < 10: 
            list1[x] = "0" + str(list1[x])
        else:
            list1[x] = str(list1[x])
    return list1

def inputFile(fileName):
    input = open(fileName, "r")
    inputList = []
    for x in input:
        inputList.append(x[:-1])
    return inputList

def emitOutput(fetch, decodeode, execute, memory, write, instCount):
    output = open("out.txt", "w")
    fetch, decodeode, execute, memory, write = formatList(fetch), formatList(decodeode), formatList(execute), formatList(memory), formatList(write)
    out = ""
    for x in range(instCount):
        out += fetch[x] + "," + decodeode[x] + "," + execute[x] + "," + memory[x] + "," + write[x] + "\n"
    output.write(out)

main("seq0.txt")


