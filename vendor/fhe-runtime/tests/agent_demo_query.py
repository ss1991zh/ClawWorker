"""
Agent demo — query: 加密后求两组员工薪资的多维统计.

Simulates what zfhe-skill / henumpy-skill instruct the LLM to emit when
the user asks an HR-style statistics question over private salary data.
"""

import numpy as np
import crypto_toolkit as ct
import henumpy as hp

print("init...")
hp.initDict()
ct.initSK()

# ----------------------------------------------------------------------
# 1. plaintext (would normally arrive already-encrypted from another party)
# ----------------------------------------------------------------------
team_a = np.array([8000.0, 12000.0, 15000.0, 9000.0, 11000.0])
team_b = np.array([10000.0, 13000.0, 14000.0, 8500.0, 11500.0])
print(f"team_a (plain) = {team_a.tolist()}")
print(f"team_b (plain) = {team_b.tolist()}")

# ----------------------------------------------------------------------
# 2. encrypt
# ----------------------------------------------------------------------
a_enc = ct.encrypt(team_a)
b_enc = ct.encrypt(team_b)
print("encrypted team_a, team_b.")

# ----------------------------------------------------------------------
# 3. ciphertext statistics (never touch the plaintext after this point)
# ----------------------------------------------------------------------
mean_a_enc  = hp.mean(a_enc)
mean_b_enc  = hp.mean(b_enc)
diff_enc    = hp.sub(mean_a_enc, mean_b_enc)
sum_a_enc   = hp.sum(a_enc)
max_a_enc   = hp.max(a_enc)
min_a_enc   = hp.min(a_enc)
std_a_enc   = hp.std(a_enc)
dot_enc     = hp.dot(a_enc, b_enc)
var_a_enc   = hp.var(a_enc)
print("computed: mean, sum, max, min, std, var, dot — all on ciphertext.")

# ----------------------------------------------------------------------
# 4. decrypt only the answers
# ----------------------------------------------------------------------
mean_a  = float(np.array(ct.decrypt(mean_a_enc)).flatten()[0])
mean_b  = float(np.array(ct.decrypt(mean_b_enc)).flatten()[0])
diff    = float(np.array(ct.decrypt(diff_enc)).flatten()[0])
total_a = float(np.array(ct.decrypt(sum_a_enc)).flatten()[0])
max_a   = float(np.array(ct.decrypt(max_a_enc)).flatten()[0])
min_a   = float(np.array(ct.decrypt(min_a_enc)).flatten()[0])
std_a   = float(np.array(ct.decrypt(std_a_enc)).flatten()[0])
dot_val = float(np.array(ct.decrypt(dot_enc)).flatten()[0])
var_a   = float(np.array(ct.decrypt(var_a_enc)).flatten()[0])

# ----------------------------------------------------------------------
# 5. report — cross-check against plaintext numpy in parentheses
# ----------------------------------------------------------------------
print()
print("=" * 64)
print(f"  team_a sum               =  {total_a:>13,.2f}   (np: {np.sum(team_a):,.2f})")
print(f"  team_a mean              =  {mean_a:>13,.2f}   (np: {np.mean(team_a):,.2f})")
print(f"  team_a max               =  {max_a:>13,.2f}   (np: {float(np.max(team_a)):,.2f})")
print(f"  team_a min               =  {min_a:>13,.2f}   (np: {float(np.min(team_a)):,.2f})")
print(f"  team_a std               =  {std_a:>13,.4f}   (np: {float(np.std(team_a)):,.4f})")
print(f"  team_b mean              =  {mean_b:>13,.2f}   (np: {np.mean(team_b):,.2f})")
print(f"  mean(a) - mean(b)        =  {diff:>13,.2f}   (np: {np.mean(team_a) - np.mean(team_b):,.2f})")
print(f"  team_a var               =  {var_a:>13,.2f}   (np: {float(np.var(team_a)):,.2f})")
print(f"  dot(a, b)                =  {dot_val:>13,.2f} (np: {float(np.dot(team_a, team_b)):,.2f})")
print("=" * 64)
print()
print("✅ All stats computed on ciphertext — plaintext salaries never left")
print("   the encryption boundary except for the final decrypt of answers.")
