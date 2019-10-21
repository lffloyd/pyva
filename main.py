from src.scanner import generateScanner

miniJavaFile = open("miniJava.java","r")

fileContent = ""

multiLineComment = False

line = miniJavaFile.readline()

while(line):
    if(multiLineComment):

        if(line.find("*/") != -1):
            multiLineComment = False
            auxLine = (line.split("*/"))
            line = auxLine[-1]
            fileContent = fileContent + line    
        
    else:

        if(line.find("/*") != -1):
            multiLineComment = True
            auxLine = (line.split("/*"))
            line = auxLine[0] + "\n"
            fileContent = fileContent + line    
        else:
            if(line.find("//") != -1):
                auxLine = (line.split("//"))
                line = auxLine[0] + "\n"
                fileContent = fileContent + line    
            else:
                fileContent = fileContent + line    
    line = miniJavaFile.readline()
    
print(fileContent)

generateScanner(fileContent)

miniJavaFile.close()