from compila.cclang import CCLangParser
from compila.error import CompilaError
from compila.tac_interpreter import TACInterpreter

parser = CCLangParser()

origin_code = '''
def matrixmult(int matA, int matB) {
    for(i = 0; i < 6; i = i + 1) 
        for(j = 0; j < 6; j = j + 1) 
            int matResult[5][5];
            matResult[i][j] = 0;
            for(k = 0; k < 6; k = k + 1) 
                matResult[i][j] = matResult[i][j] + matA[i][k] * matB[k][j];
                print matResult; return;
}
'''

bla = parser.analyze(origin_code)
inter_code = bla.code + "print bla"

print(inter_code)
print()

# interpreter = TACInterpreter()
# interpreter.run(inter_code)
