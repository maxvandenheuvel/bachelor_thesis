/*  ID          is 1 letter, either upper or lower case.
    rules       "ID <- premise."
    premise     "ID or ID COMPOUND ID COMPOUND..." with optional brackets
    COMPOUND    "and" or "or"

*/

grammar Hello;
/*
Parser Rules
*/

prog        : expr+ EOF;

expr        : conclusion IMPLIES premise end;

//conclusion  : lc=LBRA conclusion rc=RBRA            #braConc
//            | conclusion AND conclusion             #andConc
//            | (NEG ID | ID)                         #genConc
//            ;

//conclusion  : LBRA* (NEG ID | ID) ((AND LBRA* (NEG ID | ID) RBRA*))* ;
conclusion  : LBRA* literal ((AND LBRA* literal RBRA*))* ;


//premise     : lp=LBRA premise rp=RBRA               #braPrem
//            | premise AND premise                   #andPrem
//            | premise OR premise                    #orPrem
//            | literal+                              #genPrem
//            ;
//premise       : LBRA* (NEG ID | ID) ((AND LBRA* (NEG ID | ID) RBRA*) | (OR LBRA* (NEG ID | ID) RBRA*))* ;
premise     : LBRA* literal ((AND LBRA* literal RBRA*) | (OR LBRA* literal RBRA*))* ;

// Can be used to calculates opposites conclusion with "and"/"or".
//conclusion  : LBRA* literal andlit* ;
//premise     : LBRA* literal (andlit | orlit)* ;
//andlit         : AND LBRA* literal RBRA* ;
//orlit       : OR LBRA* literal RBRA* ;

literal     : NEG ID                                #negID
            | ID                                    #genID
            ;

end         : DOT ;

/*
Lexer Rules
*/

AND         : 'and' ;
OR          : 'or' ;
IMPLIES     : '<-' ;
NEG         : '-';
LBRA        : '(' ;
RBRA        : ')' ;
DOT         : '.' ;

ID          : [a-z] | [A-Z];

WS          : [ \t\r\n]+ -> skip ;

ANY         : . ;