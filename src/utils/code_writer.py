from os import name


def write_assembly_code(file, mode, data):
    folderSeparator = "/" if (name == "posix") else "\\"
    destinationPathArr = file.split(folderSeparator)

    filename = destinationPathArr[len(destinationPathArr)-1].lower().replace(".java", ".asm")

    path = folderSeparator.join(destinationPathArr[:-1]) + filename

    destinationFile = open(path, mode)

    destinationFile.write(data)

    destinationFile.close()

    print("ASM file generated at: " + path + "\n")