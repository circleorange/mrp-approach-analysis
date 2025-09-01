# Overview

Cloned source: https://bitbucket.org/wjaskowski/roadef-challange-2012-public/src/master/

This repository contains the solution submitted by team J12 for the EURO/ROADEF
2012 Challange Machine Reassignment Problem proposed by Google:<br>
http://challenge.roadef.org/2012/en/index.php.

For more informations about the solution see:<br>
http://www.cs.put.poznan.pl/wjaskowski/projects/roadef-challenge-2012.

# Dependencies

- Java 8
- Ant
- IBM ILOG CPLEX Studio v22.1.1 (specifically for the MIP solver)

# Build

- To compile and build the build/jar/roadef.jar file, run:
```
ant jar
```

Other `ant` commands include; `ant clean`, `ant compile`.

# Run

- As the project relies on CPLEX Solver v22.1.1, ensure it is accessible to the system:
```
export CPLEX_STUDIO=/opt/ibm/ILOG/CPLEX_Studio2211
export LD_LIBRARY_PATH=$CPLEX_STUDIO/cplex/bin/x86-64_linux:$LD_LIBRARY_PATH
```

- Run the project using the VS Code launch files.
