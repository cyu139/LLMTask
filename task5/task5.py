from openai import OpenAI
import subprocess
from collections import Counter

client = OpenAI()

#Translation step using AI

question = "Who counters Ezreal?"
print(f"Question: {question}\n")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0.8,
    n=5,
    messages=[
        {"role": "system", "content": "You are a Prolog translator. Translate the user's question into a single Prolog query using the good_pick(MyChamp, EnemyChamp) rule. ONLY output the raw Prolog query string. Do not include markdown, formatting, periods, or any conversational text."},
        {"role": "user", "content": question}
    ]
)

translations = [choice.message.content.strip().rstrip('.') for choice in response.choices]
print("--- 5 Generated Queries by ChatGPT ---")
for i, t in enumerate(translations, 1):
    print(f"Query {i}: {t}")
print()

#Logic Prover step

prolog_file = "leagueKB.pl"
prolog_results = []

print("--- Results after running each query through prolog ---")

for i, query in enumerate(translations, 1):
    prolog_goal = f"forall({query}, writeln({query}))"
    try:
        result = subprocess.run(
            ["swipl", "-q", "-s", prolog_file, "-g", prolog_goal, "-t", "halt"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True 
        )
        output = result.stdout.strip()
        
        if output:
            prolog_results.append(output)
            print(f"Test {i} yielded: {output}")
        else:
            prolog_results.append("Unsure / No match")
            print(f"Test {i} yielded: Unsure / No Match")
            
    except subprocess.CalledProcessError:
        #crash handler
        prolog_results.append("Error")
        print(f"Query {i} yielded: Error (bad syntax)")
print()

# k-majority vote to determine best results
vote_counts = Counter(prolog_results)
final_answer = vote_counts.most_common(1)[0][0]

print("--- K-Majority Vote Final Result ---")
for ans, count in vote_counts.items():
    print(f"Votes: {count} | Answer: {ans}")

print(f"\nFinal Answer: {final_answer}")