facts = {
    ("lane", "darius", "top"),
    ("lane", "garen", "top"),
    ("lane", "nidalee", "jungle"),
    ("lane", "graves", "jungle"),
    ("lane", "katarina", "mid"),
    ("lane", "ahri", "mid"),
    ("lane", "ezreal", "bot"),
    ("lane", "lucian", "bot"),
    ("lane", "nami", "sup"),
    ("lane", "janna", "sup"),
    ("counters", "darius", "garen"),
    ("counters", "graves", "nidalee"),
    ("counters", "katarina", "ahri"),
    ("counters", "lucian", "ezreal"),
    ("counters", "nami", "janna")
}

lanes = ["top", "jungle", "mid", "bot", "sup"]

def backwards_chain(goal):
    if goal in facts:   # our base case, where goal is a fact
        return True
    
    predicate = goal[0]     # start evaluating using recursion

    if predicate == "good_pick":
        my_champ = goal[1]
        enemy_champ = goal[2]

        for lane in lanes:  # test each lane (our OR tree)
            subgoals = [
                ("lane", my_champ, lane),
                ("lane", enemy_champ, lane),
                ("counters", my_champ, enemy_champ)
            ]


            subgoals_met = True     # check if all subgoals are met (our AND tree)
            for subgoal in subgoals:
                if not backwards_chain(subgoal):
                    subgoals_met = False
                    break       # break if subgoal is false
            
            if subgoals_met:
                return True     # backwards chaining proved all subgoals are true
        
    return False    # returns false if not a known fact or accepted predicate

print("Is Darius a good pick into Garen?")  # should return true (darius is a top laner, garen is a top laner, and darius counters garen)
print("Answer: ", backwards_chain(("good_pick", "darius", "garen")))
print("------------------------------")

print("Is Nidalee a good pick into Garen?") # should return false (nidalee and garen are different lanes, no counter relationship)
print("Answer: ", backwards_chain(("good_pick", "nidalee", "garen")))
print("------------------------------")

print("Is Lucian a good pick into Ezreal?") # should return true (lucian is a bot laner, ezreal is a bot laner, and lucian counters ezreal)
print("Answer: ", backwards_chain(("good_pick", "lucian", "ezreal")))
print("------------------------------")

print("Is Ahri a good pick into Katarina?") # should return false (ahri is a mid laner, katarina is a mid laner, and ahri is COUNTERED by katarina)
print("Answer: ", backwards_chain(("good_pick", "ahri", "katarina")))
print("------------------------------")




