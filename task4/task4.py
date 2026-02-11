import janus_swi as janus

janus.consult("leagueKB.pl")

print("Query 1: Is Darius a good pick into Garen?")
q1 = janus.query_once("good_pick(darius, garen)")
print(f"Answer: {q1['truth']}")

print("Query 2: Who counters Ezreal?")
q2 = janus.query_once("good_pick(Who, ezreal)")
print(f"Counter: {q2['Who']}")

print("Query 3: List all available good picks")
for x in janus.query("good_pick(Winner, Loser)"):
    print(f"{x['Winner']} is a good pick against {x['Loser']}")

