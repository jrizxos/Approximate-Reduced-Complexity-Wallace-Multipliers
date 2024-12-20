all: evaluator8 evaluator16 evaluator32

evaluator8: afa.cpp evaluator8.cpp  mul8.cpp  debug.cpp afa.h evaluator8.h  mul8.h  debug.h
	g++ afa.cpp evaluator8.cpp  mul8.cpp  debug.cpp afa.h evaluator8.h  mul8.h  debug.h -o "evaluator8"  -O3

evaluator16: afa.cpp evaluator16.cpp mul16.cpp debug.cpp afa.h evaluator16.h mul16.h debug.h
	g++ afa.cpp evaluator16.cpp mul16.cpp debug.cpp afa.h evaluator16.h mul16.h debug.h -o "evaluator16" -O3

evaluator32: afa.cpp evaluator32.cpp mul32.cpp debug.cpp afa.h evaluator32.h mul32.h debug.h
	g++ afa.cpp evaluator32.cpp mul32.cpp debug.cpp afa.h evaluator32.h mul32.h debug.h -o "evaluator32" -O3