def read_source_code(file, mode):
    sourceCode = open(file, mode)

    fileContent = ""

    multiLineComment = False

    line = sourceCode.readline()

    while (line):
        if (multiLineComment):

            if (line.find("*/") != -1):
                multiLineComment = False
                auxLine = (line.split("*/"))
                line = auxLine[-1]
                fileContent = fileContent + line

        else:

            if (line.find("/*") != -1):
                multiLineComment = True
                auxLine = (line.split("/*"))
                line = auxLine[0] + "\n"
                fileContent = fileContent + line
            else:
                if (line.find("//") != -1):
                    auxLine = (line.split("//"))
                    line = auxLine[0] + "\n"
                    fileContent = fileContent + line
                else:
                    fileContent = fileContent + line
        line = sourceCode.readline()

    sourceCode.close()

    return fileContent