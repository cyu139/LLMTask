/* ----------------------------------------------------------
   Title:   League Knowledge Base
   Author:  Crystal Yu
   Date:    2026-02-11
   
   Description:
   Prolog program with KB for use in Task4 and Task5
   League of Legends with 10+ facts and 1+ rule
   ----------------------------------------------------------
*/

% Facts
champion(darius).
champion(garen).
champion(nidalee).
champion(graves).
champion(katarina).
champion(ahri).
champion(ezreal).
champion(lucian).
champion(nami).
champion(janna).

lane(darius, top).
lane(garen, top).
lane(nidalee, jungle).
lane(graves, jungle).
lane(katarina, mid).
lane(ahri, mid).
lane(ezreal, bot).
lane(lucian, bot).
lane(nami, sup).
lane(janna, sup).

counters(darius, garen).
counters(graves, nidalee).
counters(katarina, ahri).
counters(lucian, ezreal).
counters(nami, janna).

% Rules

good_pick(MyChamp, EnemyChamp) :-
    lane(MyChamp, Lane),
    lane(EnemyChamp, Lane),
    counters(MyChamp, EnemyChamp).