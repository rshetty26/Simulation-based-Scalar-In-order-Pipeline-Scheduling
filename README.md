In a programming language of your choice among {C, Java, Python, C++} [note, you will be submitting a makefile, and it must ensure that the correct version of python is invoked i.e. be explicit in whether to invoke the python3 or python2.7 interpreter], implement a program with the following specification that schedules a restricted set of simplified instructions on an FDEMW 5 stage scalar (1-wide) pipeline with all potential forwarding paths:

a) Invocation:
Your program will be built (if necessary) and invoked via the Make utility. We will run "make test" i.e. asking the make program to follow the "test" rule.
The test rule will have your program consume an input file named test.in and produce its output in a file named out.txt

b) Format of input file:
The input file will consist of 1-32 lines, with each line being in one of the 4 formats below: 
- R,<REG>,<REG>,<REG>
- I,<REG>,<REG>,<IMM>
- L,<REG>,<IMM>,<REG>
- S,<REG>,<IMM>,<REG>
where {R,I,L,S} are the capital letters R, I, L, and S, {,} is comma, <REG> is a positive integer value between 0 and 31, inclusive, and <IMM> is a NON-NEGATIVE integer value between 0 and 65535, with both <REG> and <IMM> encoded as decimals. The first <REG> is the destination for R, I, and L. Memory (not modeled) is the destination for S.
e.g. a valid input file may look like:
- L,2,80,4
- L,3,64,5
- R,2,2,3
- S,2,24,29
- L,2,80,4
- L,3,64,2
- S,2,20,3
- L,7,28,3
- S,7,24,29
R represents R-type instructions, e.g. ADDU $2, $3, $4 --> R,2,3,4

L represents loads, e.g. LW $2, 80($3) --> L,2,80,3

I represents immediate instructions, e.g. ADDI $2, $3, 300 --> I,2,3,300

S represents store instructions, e.g. SW $2, 40($8) --> S,2,40,8 

c) Specifications
- Pipeline stages = <F>,<D>,<E>,<M>,<W>
- The first instruction is always fetched in cycle 0
- Register 0 is always 0 (writes to $0 are no-ops; no dependencies via register 0).
- All memory operations are cache hits; ergo, the only stalls in this system are register-carried load-use dependencies
Given the above, and standard assumptions about FDEMW pipelines with forwarding, produce the following output in out.txt:
For each instruction in the input file, produce a corresponding line in out.txt of the form
<F-cycle>,<D-cycle>,<E-cycle>,<M-cycle>,<W-cycle>
where all comma-separated fields are non-negative integers encoded as two-digit decimals and represent the cycle in which the associated instruction completes the specified stage.
e.g. for the example input above in b), the expected output is:
00,01,02,03,04
01,02,03,04,05
02,04,05,06,07
04,05,06,07,08
05,06,07,08,09
06,08,09,10,11
08,10,11,12,13
10,11,12,13,14
11,12,13,14,15
