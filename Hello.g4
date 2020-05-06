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

conclusion  : lc=LBRA conclusion rc=RBRA
            | conclusion AND conclusion
            | literal
            ;

premise     : lp=LBRA premise rp=RBRA
            | premise AND premise
            | premise OR premise
            | literal
            ;

literal     : NEG ID
            | ID
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