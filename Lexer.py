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
    tokens = { OBJECTID, INT_CONST, BOOL_CONST,TYPEID,NUMBER,ERROR1,ASSIGN, COMENT,DARROW,LE, ELSE, STR_CONST, CASE, CLASS, ESAC, FI, IF, IN, INHERITS,ISVOID,LET,LOOP,NEW,NOT,OF, POOL,THEN,WHILE, ERROR}
    #ignore = '\t '
    literals = { '=', '+', '-', '*', '/', '(', ')', '<', '.',',','~',';',':','(',')', '@', '{','}'}
    asci = {'','','','','',''}

    ELSE =r'[eE][lL][sS][eE]\b'
    CASE =r'[cC][aA][sS][eE]\b'
    CLASS =r'[cC][lL][aA][sS][sS]\b'
    ESAC =r'[eE][sS][aA][cC]\b'
    FI =r'[fF][iI]\b'
    IF =r'[iI][fF]\b'
    IN =r'[iI][nN]\b'
    INHERITS = r'[iI][nN][hH][eE][rR][iI][tT][sS]\b'
    ISVOID = r'[iI][sS][vV][oO][iI][dD]\b'
    LET = r'[lL][eE][tT]\b'
    LOOP = r'[lL][oO][oO][pP]\b'
    NEW = r'[nN][eE][wW]\b'
    NOT = r'[nN][oO][tT]\b'
    OF = r'[oO][fF]\b'
    POOL = r'[pP][oO][oO][lL]\b'
    THEN = r'[tT][hH][eE][nN]\b'
    WHILE = r'[wW][hH][iI][lL][eE]\b'
    ASSIGN = r'<-'
    DARROW = r'=>'
    LE = r'<='

    @_(r'"([^"\n\\]|([^\\]?(\\\\)*\\(\n|.)))*"')
    def STR_CONST(self, t):
        self.lineno += t.value.count('\n')
        t.lineno = self.lineno
        t.value = t.value.replace('\\\n',r'\n')
        t.value = t.value.replace('\\\t',r'\t')
        t.value = t.value.replace('\\\b',r'\b')
        t.value = t.value.replace('\\\f',r'\f')
        t.value = t.value.replace('\t',r'\t')
        #for e in asci:
        #    t.value = t.value.replace(e,ord(e))
        r = re.compile(r'(?<!\\)\\([^nftb"\\])')
        t.value = r.sub(r'\1', t.value)
        return t

    @_(r'"[^"]*\n')
    def ERROR1(self,t):
        self.lineno += t.value.count('\n')
        t.lineno = self.lineno
        t.type = "ERROR"
        t.value = '"Undeterminated string constant"'
        return t

    @_(r'\(\*.*\*\)')
    def COMENT(self,t):
        pass

    @_(r'[!#$%^&_>\?`\[\]\\\|]')
    def ERROR(self,t):
        t.type = "ERROR"
        if t.value == "\\":
            t.value = "\\\\"
        t.value = '"'+t.value+'"'
        return t

    @_(r'\d+')
    def INT_CONST(self, t):
        return t

    @_(r'(t[rR][uU][eE]\b|f[aA][lL][sS][eE]\b)')
    def BOOL_CONST(self, t):
        if t.value[0] == "t":
            t.value = True
        else:
            t.value = False
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
            elif token.type == 'ERROR':
                result += f"{str(token.value)}"
            elif token.type == 'INT_CONST':
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
    fich = "stringcomment.cool"
    f = open(os.path.join(DIR,fich),'r')
    text = f.read()
    print('\n'.join(lexer.salida(text)))
