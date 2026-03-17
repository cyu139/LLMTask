% ==========================================
% FACTS (19 Facts)
% ==========================================

% parent(Parent, Child).
parent(john, mary).
parent(john, michael).
parent(susan, mary).
parent(susan, michael).
parent(michael, david).
parent(michael, emma).
parent(linda, david).
parent(linda, emma).
parent(mary, sophia).
parent(robert, sophia).

% male(Person).
male(john).
male(michael).
male(david).
male(robert).

% female(Person).
female(susan).
female(mary).
female(linda).
female(emma).
female(sophia).

% ==========================================
% RULES (10 Rules)
% ==========================================

father(X, Y) :- 
    parent(X, Y), 
    male(X).

mother(X, Y) :- 
    parent(X, Y), 
    female(X).

child(X, Y) :- 
    parent(Y, X).

sibling(X, Y) :- 
    parent(Z, X), 
    parent(Z, Y), 
    X \= Y.

brother(X, Y) :- 
    sibling(X, Y), 
    male(X).

sister(X, Y) :- 
    sibling(X, Y), 
    female(X).

grandparent(X, Y) :- 
    parent(X, Z), 
    parent(Z, Y).

grandfather(X, Y) :- 
    grandparent(X, Y), 
    male(X).

grandmother(X, Y) :- 
    grandparent(X, Y), 
    female(X).
    
uncle(X, Y) :- 
    brother(X, Z), 
    parent(Z, Y).