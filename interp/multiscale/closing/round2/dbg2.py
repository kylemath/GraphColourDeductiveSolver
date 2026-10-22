from tm import *
L=8; R=rows(L); idx={r:i for i,r in enumerate(R)}; N=len(R)
shift_of = np.array([[idx[r[k:]+r[:k]] for r in R] for k in range(L)])
perm_of = np.array([[idx[tuple(p[c] for c in r)] for r in R] for p in PERMS])
full = np.concatenate([perm_of[:, shift_of[k]] for k in range(L)])
print(full.shape, all(set(full[:,i]) >= {i} for i in range(5)))
i=idx[(0,1,0,1,2,3,2,3)]
print(sorted(R[j] for j in set(full[:,i]))[:5], len(set(full[:,i])))
