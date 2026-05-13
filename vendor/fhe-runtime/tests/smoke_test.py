"""
FHE smoke test — end-to-end encrypt/compute/decrypt pipeline.

What this proves:
  1. crypto_toolkit + henumpy load with the user's skf/dictf/user_authorization
  2. Plaintext numbers can be encrypted to a CipherArray
  3. Ciphertext arithmetic (add/mul/dot/mean) produces correct results
  4. Decryption recovers the expected plaintext
"""

import sys
import time

import numpy as np
import crypto_toolkit as ct
import henumpy as hp


def banner(s):
    print(f"\n{'=' * 60}\n{s}\n{'=' * 60}")


banner("1. Initialize FHE runtime")
t0 = time.time()
hp.initDict()
ct.initSK()
print(f"  initDict + initSK ok  ({time.time() - t0:.2f}s)")

banner("2. Encrypt plaintext arrays")
a_plain = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
b_plain = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
print(f"  a (plain) = {a_plain.tolist()}")
print(f"  b (plain) = {b_plain.tolist()}")

t0 = time.time()
a_enc = ct.encrypt(a_plain)
b_enc = ct.encrypt(b_plain)
print(f"  encrypt 2x5 elements ok  ({time.time() - t0:.2f}s)")
print(f"  type(a_enc)         = {type(a_enc).__name__}")

banner("3. Ciphertext arithmetic")
t0 = time.time()
c_enc = hp.add(a_enc, b_enc)
print(f"  c = a + b           done ({time.time() - t0:.2f}s)")

t0 = time.time()
d_enc = hp.mul(a_enc, b_enc)
print(f"  d = a * b           done ({time.time() - t0:.2f}s)")

t0 = time.time()
dot_enc = hp.dot(a_enc, b_enc)
print(f"  dot = a · b         done ({time.time() - t0:.2f}s)")

t0 = time.time()
mean_enc = hp.mean(a_enc)
print(f"  mean = avg(a)       done ({time.time() - t0:.2f}s)")

banner("4. Decrypt and verify")

def verify(label, enc, expected):
    t = time.time()
    decoded = ct.decrypt(enc)
    decoded_arr = np.array(decoded).flatten()
    expected_arr = np.array(expected).flatten() if hasattr(expected, '__len__') else np.array([expected])
    ok = np.allclose(decoded_arr[: len(expected_arr)], expected_arr, atol=1e-2)
    mark = "✅" if ok else "❌"
    print(f"  {mark} {label:8s} = {decoded_arr[:len(expected_arr)].tolist()}   "
          f"(expected {expected_arr.tolist()})   "
          f"[decrypt {time.time()-t:.2f}s]")
    return ok

results = []
results.append(verify("a+b",   c_enc,    a_plain + b_plain))
results.append(verify("a*b",   d_enc,    a_plain * b_plain))
results.append(verify("a·b",   dot_enc,  np.dot(a_plain, b_plain)))
results.append(verify("mean",  mean_enc, np.mean(a_plain)))

banner("Summary")
passed = sum(results)
print(f"  {passed}/{len(results)} checks passed")
sys.exit(0 if passed == len(results) else 1)
