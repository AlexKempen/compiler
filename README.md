# compiler
This is my compiler.

### Setup
This project includes a VS Code Dev Container, which bundles all of the dependencies and extensions need to run the project.

To use the Dev Container:
1. Install VS Code.
2. Add the Dev Containers Extension to VS Code.
3. Install and open Docker Desktop.
4. Use the command palette to open this repo in a Dev Container.

### Tests
Tests are written using Python's unittest package. They can be run in VSCode using the Testing tab.

### LLVM
This compiler outputs .ll llvm files. 

Example .ll files can also be created by compiling .c files using clang:
```
clang -emit-llvm hello.c -S -o hello.ll
```
.ll files can be compiled into byte code using clang:
```
clang hello.ll -o hello.out
```

