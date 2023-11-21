# FGPA Synthesis Engine

This program was completed for EC551 at Boston University

## About this program

This program takes a file of equations or a bitstream and synthesizes a FPGA based on the given specs.

## Table of Contents

1. [Running the Program](#running-the-program)
2. [Dependencies](#dependencies)
3. [Outputs](#outputs)
4. [Organization](#organization)
5. [Reading Code](#reading-code)
6. [Appendix](#appendix)

## Running the Program

The main executable is `runner.py`.

To execute using equations: `python runner.py -f <inputs>` The inputs must be in order:

- file: *.dat like in examples
  - supports SOP and POS equations
  - POS equations must start with parenthesis
- nLut: number of LUTs in the synthesized FPGA
- tLut: type of LUT (4 or 6)
- cLut: *.json file representing a partially connected LUT (optional)

Example equation files are located in the _examples_ directory.

Example:
```bash
python runner.py -f examples/example_4var.dat 8 4
```

To execute using a previously created bitstream, use: `python runner.py -b <file>` where the file is the bitstream.

Outputs are specified [below](#outputs).

## Dependencies

EC551 Project 1: Logic Synthesis Engine which was minimized to build this.

## Outputs

The follow information can be accessed on the UI upon a successful run:

- list of functions assigned to LUTs
  - f: all
  - f \<output\>: some specified
- c: internal connections
- i: external input assignments
- o: external output assignments
- b: bitstream
- r: resource allocation

### Bad exit codes

- 

## Organization

Each python file has a dedicated purpose.

configurator.py
- creates the confiuration for the synthesis of an FPGA

eq_adt.py
- contains the class implementation to hold relevant logic synthesis data

fpga_adt.py
- contains the class implementation to hold relevant FPGA and LUT data

logic_synthesis_engine.py
- the synthesis engine used to parse equations and output requested information

quine_mccluskey.py
- contains the Quine-McCluskey algorithm used by the synthesis engine to minimize functions

runner.py
- contains the UX interface to interact with the program

tester.py
- contains tests for all logic heavy files

## Reading Code

Files will have a header describing what the file is and what it does.

Comments are at the start of every major function implementation and parts of the code to help readers track what is happening.

## Appendix

### Known Issues
