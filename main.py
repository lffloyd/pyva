from src.scanner import generateScanner

miniJavaFile = open("miniJava.java","r")

fileContent = miniJavaFile.read()

generateScanner(fileContent)
