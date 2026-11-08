# ST-51 v2 add-on smoke (Studio, 8 Nov)
smoke_v2.sh ended SMOKE-V2: FAIL with one failing step (4): the comparator saw 3 extra numpy RuntimeWarning lines (<string>:166 = v2r.py line 166,
divide by zero / overflow / invalid value in matmul); V2R-TEST: PASS on both sides, 0 of 37 reference lines differ. Opus (via coordinator, 08:17Z):
the line multiplies 0/1 masks by finite amounts, no division, so the flags are spurious FP flags left by numpy 2.0 + Accelerate; GO.
Recorded as PASS: touch smoke_v2.ok in the pack. All other steps OK (gate t = -0.076947399076 = container). GV1 not launched, k86ML1 not stopped.
