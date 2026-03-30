import os
import re

# ============================================================
#      TYPE-A MINI (V11.5) - THE ABSOLUTE UNIVERSAL ASSEMBLER
# ============================================================
# Consolidated 7-Week Intelligence: Labs 1-7 (Week 1 to Week 7).
# Absolute Semantic Scorer + Universal Formula Library.
# Zero Internet. 100% Offline coverage of the curriculum.

KNOWLEDGE_HUB = {
    # Week 1: Basics (Arithmetic, Interest, BMI)
    "interest": ("res = (val1 * val2 * val3) / 100 if 'compound' not in text else val1 * ((1 + val2/100) ** val3)", ["principal", "rate", "time"]),
    "bmi": ("res = val1 / ((val2/100) ** 2)", ["weight", "height"]),
    "area_circle": ("res = 3.14159 * (val1 ** 2)", ["radius"]),
    "temp": ("res = (val1 - 32) * 5/9 if 'f' in text else (val1 * 9/5) + 32", ["temp"]),

    # Week 2: Strings (Slicing, Case, Palindromes)
    "string_ops": (["v1_res = str(val1).upper()", "v2_res = str(val2)[::-1]"], ["name", "member_id"]),
    "palindrome": ("res = str(val1).lower() == str(val1)[::-1].lower()", ["text"]),

    # Week 3: Bitwise & Radix (XOR, Shifts, Hex/Bin)
    "bitwise": (["bw_xor = int(val1) ^ 255", "bw_shift = bw_xor << 1 if bw_xor > 100 else bw_xor", "bw_hex = hex(bw_shift)"], ["pin"]),
    "rgb_hex": ("res = '#{:02x}{:02x}{:02x}'.format(int(val1), int(val2), int(val3))", ["red", "green", "blue"]),
    "radix": ("res = bin(int(val1)) if 'bin' in text else (hex(int(val1)) if 'hex' in text else oct(int(val1)))", ["value"]),

    # Week 4: Conditionals (Leap, ATM, Fraud, Grades, Commission)
    "leap": ("res = (int(val1) % 4 == 0 and int(val1) % 100 != 0) or (int(val1) % 400 == 0)", ["year"]),
    "grades": (["if val1 >= 90: g='A'", "elif val1 >= 80: g='B'", "elif val1 >= 70: g='C'", "else: g='F'", "res = g"], ["score"]),
    "fraud": (["if val1 > 100000 and str(val2).lower() != 'pakistan': res='High Risk'", "elif val1 > 100000: res='Review Required'", "else: res='Valid'"], ["amount", "location"]),
    "commission": (["if val1 > 10000: res = val1 * 0.10", "else: res = val1 * 0.05"], ["sales"]),

    # Week 5: Loops (Primes, Fibonacci, Factorial)
    "primes": ("res = [x for x in range(int(val1), int(val2)+1) if all(x % i for i in range(2, int(x**0.5) + 1))]", ["start", "end"]),
    "fibonacci": ("a, b = 0, 1; res = []; [(res.append(a), (a := b), (b := a+b)) for _ in range(int(val1))]", ["count"]),
    "factorial": ("res = math.factorial(int(val1))", ["value"]),
    "loop_else": (["for i in range(1, 11):", "    print(i)", "    if i > 15: break # Example break", "else:", "    print('Count Complete')", "res = 'Loop Finished'"], ["input_val"]),

    # Week 6: Functions & Lambdas
    "lambda_filter": ("res = list(filter(lambda x: x > 50, val1))", ["list_input"]),

    # Week 7: Collections (Analytics, Stats, Tuples, List Ops)
    "list_ops": (["unique = sorted(list(set(val1)))", "res = unique"], ["data_list"]),
    "stats": (["total = sum(val1)", "avg = total/len(val1)", "high = max(val1)", "res = (total, avg, high)"], ["data_list"])
}

def analyze_intent(text):
    text = text.lower().strip()
    p = {"f_name": "pb_solution", "count": 1, "inputs": [], "blocks": [], "loop": "fixed"}

    # 1. Semantic Scorer (All 7 Weeks) - Strict Word Boundaries
    scores = {k: 0 for k in KNOWLEDGE_HUB.keys()}
    def score(k, patterns, weight=10):
        if any(re.search(r"\b" + p + r"\b", text) for p in patterns): scores[k] += weight

    score("interest", ["interest", "principal", "rate", "loan"], 30)
    score("bmi", ["bmi", "weight", "height"], 30)
    score("area_circle", ["radius", "circle", "area"], 30)
    score("temp", ["temp", "fahrenheit", "celsius"], 30)
    score("string_ops", ["upper", "reverse", "formatting", "name", "member_id"], 5)
    score("palindrome", ["palindrome"], 30)
    score("bitwise", ["xor", "bitwise", "shift"], 30)
    score("rgb_hex", ["rgb", "red", "green", "blue"], 30)
    score("radix", ["bin", "binary", "hex", "octal"], 30)
    score("leap", ["leap"], 30)
    score("grades", ["grade", "attendance", "score"], 30)
    score("fraud", ["fraud", "risk", "flag", "location", "pakistan"], 40)
    score("commission", ["commission", "sales", "bonus", "salary"], 40)
    score("primes", ["prime"], 30)
    score("fibonacci", ["fibonacci"], 30)
    score("factorial", ["factorial"], 30)
    score("loop_else", ["loop", "else", "break", "interrupted"], 40)
    score("lambda_filter", ["filter", "lambda"], 30)
    score("list_ops", ["unique", "set", "sort", "duplicates"], 40)
    score("stats", ["stats", "analytics", "average", "total", "max"], 5)

    best_block = max(scores, key=scores.get)
    if scores[best_block] > 0: p["blocks"] = [best_block]

    # 2. Input Mapping
    if p["blocks"]:
        p["inputs"] = KNOWLEDGE_HUB[p["blocks"][0]][1]
    else:
        p["inputs"] = ["val1", "val2"]

    # 3. Metas (Loop/Count/Function Name)
    fn = re.search(r"\b(named|called|function)\b\s+([\w_]+)", text)
    if fn: p["f_name"] = fn.group(2)
    
    if any(k in text for k in ["exit", "another", "choice", "until"]): p["loop"] = "while"
    else:
        ct = re.search(r"(\d+)\s+[\w\s]{0,20}\b(nodes|students|people|items|customers|colors|entries|loans|members|prices|scores)\b", text)
        p["count"] = int(ct.group(1)) if ct else 1

    return p

def construct_solution(p, text_full):
    code = ["import os", "import math", "import random", ""]
    safe_text = text_full.replace("'", "").replace("\n", " ")
    
    # --- FUNCTION ---
    args = ", ".join([f"val{i+1}" for i in range(len(p["inputs"]))])
    code.append(f"def {p['f_name']}({args}):")
    code.append(f"    text = '{safe_text}' # Core Problem Context")
    code.append("    # Logical Synthesis Engine")
    
    if p["blocks"]:
        snippet = KNOWLEDGE_HUB[p["blocks"][0]][0]
        if isinstance(snippet, list):
            for line in snippet: code.append(f"    {line}")
        else: code.append(f"    {snippet}")
    else:
        code.append("    res = val1 # Default fallback")

    # Smart Return Detection
    ret = "res"
    if "string_ops" in p["blocks"]: ret = "v1_res, v2_res"
    if "bitwise" in p["blocks"]: ret = "bw_hex"
    if "grades" in p["blocks"]: ret = "res"
    code.append(f"    return {ret}")
    code.append("")

    # --- MAIN LOOP ---
    code.append("all_results = []")
    if p["loop"] == "while": code.append("active = True\nwhile active:")
    else:
        code.append(f"for i in range({p['count']}):")
        code.append("    print(f'\\n--- Processing Entry {i+1} ---')")

    for i, label in enumerate(p["inputs"]):
        code.append(f"    raw_{i+1} = input('Enter {label.title() if label != 'val1' else 'Input'}: ')")
    
    code.append("    try:")
    for i in range(len(p["inputs"])):
        code.append(f"        val{i+1} = float(raw_{i+1}) if raw_{i+1}.replace('.','').isdigit() else raw_{i+1}")
    code.append("    except: pass")
    
    code.append(f"    final = {p['f_name']}({', '.join([f'val{i+1}' for i in range(len(p['inputs']))])})")
    code.append("    print(f'Done: {final}')")
    code.append("    all_results.append(final[-1] if isinstance(final, (tuple, list)) else final)")
    
    if p["loop"] == "while":
        code.append("    if input('Exit? (y/n): ').lower() == 'y': active = False")

    # --- FINAL REPORT ---
    code.append("\n# --- ABSOLUTE FINAL REPORT (Immutable Stats) ---")
    code.append("num_only = [x for x in all_results if isinstance(x, (int, float))]")
    code.append("if num_only:")
    code.append("    print(f'Stats Summary -> Total: {sum(num_only)}, Avg: {sum(num_only)/len(num_only):.2f}')")
    code.append("final_record = tuple(all_results)")
    code.append("print('Stored Tuple Record:', final_record)")
    
    return "\n".join(code)

def main():
    if not os.path.exists("problem.txt"): return
    with open("problem.txt", "r") as f: text = f.read()
    p = analyze_intent(text)
    with open("midterm_solution.py", "w") as f:
        f.write("# --- MIDTERM SOLUTION BY GOD-MODE V11.0 ---\n\n")
        f.write(construct_solution(p, text))
    print(f"[Success] God-Mode V11.0 synthesized: {p['blocks']}")

if __name__ == "__main__":
    main()
