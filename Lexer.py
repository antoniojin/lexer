# coding: utf-8

from sly import Lexer
import os
import re

PRACTICA = os.path.join("C:/Users/anton/Desktop/LenguajesProgramacion/practica1/")
DIR = os.path.join(PRACTICA, "grading")
FICHEROS = os.listdir(DIR)
TESTS =  [fich for fich in FICHEROS
          if os.path.isfile(os.path.join(DIR, fich)) and fich.endswith(".cool")]
TESTS.sort()

class CoolLexer(Lexer):
    tokens = { OBJECTID, INT_CONST, BOOL_CONST, TYPEID,NUMBER, ELSE, STR_CONST}
    #ignore = '\t '
    literals = { '=', '+', '-', '*', '/', '(', ')', '<', '.',',','~',';',':','(',')', '@', '{','}'}

    ELSE =r'[eE][lL][sS][eE]'

    @_(r'".*"')
    def STR_CONST(self, t):
        r = re.compile(r'\\([^nftb\\"])')
        t.value = r.sub(r'\1', t.value)
        return t
    
    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r't[rR][uU][eE]')
    def BOOL_CONST(self, t):
        t.value = True
        return t
    
    @_(r'[A-Z][a-zA-Z0-9]*')
    def TYPEID(self, t):
        t.value =str(t.value)
        return t

    @_(r'[a-z_][a-zA-Z0-9_]*')
    def OBJECTID(self,t):
        return t
    
    @_(r'\t| ')
    def spaces(self, t):
        pass
    
    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

    def salida(self, texto):
        list_strings = []
        for token in lexer.tokenize(texto):
            result = f'#{token.lineno} {token.type} '
            if token.type == 'OBJECTID':
                result += f"{token.value}"
            elif token.type == 'BOOL_CONST':
                result += "true" if token.value else "false"
            elif token.type == 'TYPEID':
                result += f"{str(token.value)}"
            elif token.type == 'STR_CONST':
                result += f"{str(token.value)}"
            else:
                result = f'#{token.lineno} {token.type}'
            
            list_strings.append(result)
        return list_strings
    def tests(self):
        for fich in TESTS:
            f = open(os.path.join(DIR,fich),'r')
            g = open(os.path.join(DIR,fich+ '.out'),'r')
            resultado = g.read()
            entrada =  f.read()
            texto = '\n'.join(self.salida(entrada))
            texto = f'#name "{fich}"\n' + texto
            f.close(), g.close()
            if texto.strip() != resultado.strip():
                #print("Primero:\n")
                #print(texto[:i])
                #print("Segundo:\n")
                #print(resultado[:i])
                print(f"Revisa el fichero {fich}")
            

lexer = CoolLexer()
                
if __name__ == '__main__':
    lexer = CoolLexer()
    #lexer.tests()
    fich = "backslash.cool"
    f = open(os.path.join(DIR,fich),'r')
    text = f.read()
    print('\n'.join(lexer.salida(text)))
