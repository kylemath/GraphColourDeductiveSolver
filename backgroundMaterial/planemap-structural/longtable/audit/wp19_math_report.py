"""Build Math's final report only from fully bound, verified phase records."""
import hashlib
import json
from pathlib import Path
from wp18_independent import ROOT, require


def main():
    manifest=json.loads((ROOT/'wp19'/'WP19-verified-output-manifest.json').read_text())
    phases={};stats={};counts={'P1':2070,'P2':843,'P3':7290}
    for phase,n in counts.items():
        p=ROOT/'wp19'/f'wp19-{phase}.json';r=ROOT/'audit'/f'wp19-{phase}-math-replay.json'
        d=json.loads(p.read_text());a=json.loads(r.read_text());c=json.loads((ROOT/'wp19'/f'wp19-{phase}-certificate-check.json').read_text())
        sha=hashlib.sha256(p.read_bytes()).hexdigest()
        require(a['complete'] and sha==a['phase_sha256']==manifest[phase]['raw_sha256'],'verified phase binding')
        require(c['total_failures']==0 and len(d['graphs'])==len(a['graphs'])==n,'coverage/certificates')
        require(len(c['results'])==1 and c['results'][0]['info']['file']==p.name,'certificate phase identity')
        require(c['results'][0]['stats']['graphs_checked']==n and c['results'][0]['stats']['pairs']==sum(g['pairs'] for g in a['graphs']),'certificate full coverage')
        s=d['summary'];require(not d['truncated'] and not s['interrupted'] and not s['unresolved_graphs'],'complete phase')
        require(not s['empty_pairs'] and not s['graphs_without_legal_pairs'],'nonempty pairs')
        require(s['hist_l']['capped']==s['hist_k']['capped']==s['hist_k']['nofill']==0,'resolved distances')
        require(all(not g['unresolved_pairs'] for g in d['graphs']),'every pair resolved')
        for stmt,v in s['statements'].items():
            killed=[g['graph_index'] for g in d['graphs'] if any(x['stmt']==stmt for x in g['kills'])]
            require(len(killed)==v['killed_count'],'kill accounting')
            na=sum(max(g['degrees'])<=6 for g in d['graphs']) if stmt=='C3' else 0
            require(v['not_applicable']==na and v['passed']==n-len(killed)-na and v['unresolved']==0,'pass/applicability accounting')
        phases[phase]=d
        stats[phase]={'graphs':n,'pairs':sum(g['pairs'] for g in a['graphs']),
                      'distinct_starts':sum(g['distinct_admitted_starts'] for g in a['graphs']),
                      'all_hole_states':sum(g['all_hole_states'] for g in a['graphs']),
                      'memberships':sum(s['hist_l'].values()),'m_hist':s['m_hist'],'U':s['U_exists'],
                      'max_l':max(int(k) for k,v in s['hist_l'].items() if v and k.isdigit()),
                      'max_k':max(int(k) for k,v in s['hist_k'].items() if v and k.isdigit()),
                      'producer_seconds':s['wall_seconds'],'replay_seconds':a['seconds'],
                      'peak_worker_KiB':s['max_peak_rss_kb'],'certificate_stats':c['results'][0]['stats'],
                      'statements':s['statements'],'raw_sha256':sha,'input_sha256':d['input_sha256']}
    require({k:v['killed'] for k,v in phases['P3']['summary']['statements'].items() if v['killed_count']}=={'M2':[[24,7228]],'C1':[[24,6406]],'C3':[[24,6406]]},'exact final kill identities')
    (ROOT/'audit'/'wp19-math-final-summary.json').write_text(json.dumps(stats,indent=2)+'\n')
    repo=ROOT.parents[2]
    lines=['# Math acceptance of WP19','',
           '5 October 2026. All released phases under frozen package `e7172ca` completed and independently reproduced. Order 24 kills M2, C1 and C3: the saved certificates and complete independent replay agree. Orders 23 and the U∃-only order-21/22 phase have no kills. There were no interrupted graphs, unresolved pairs, truncated records, capped distances or admitted starts in Kempe classes without a fill in any phase. These are finite results; the unrestricted vacancy hypothesis and U∃ remain open.','',
           '## Exact scope','',
           '| Phase | Graphs | Legal vertex/fan pairs | m=1 | m=2 | m=3 | U∃ true | Largest ℓ / κ |',
           '| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |']
    for phase,s in stats.items():
        lines.append(f"| {phase} | {s['graphs']:,} | {s['pairs']:,} | {s['m_hist'].get('1',0):,} | {s['m_hist'].get('2',0):,} | {s['m_hist'].get('3',0):,} | {s['U']['true']:,} | {s['max_l']} / {s['max_k']} |")
    lines+=['','P1 tests all seven statements on all 2,070 order-23 graphs. P3 tests them on all 7,290 order-24 graphs. P2 tests **U∃ only** on all 192 order-21 and 651 order-22 graphs; its other measurements are secondary data. Every graph has m≤2 except 24:6406, whose exact m is 3. This does not mean every vertex/fan pair or every start fills in two moves. Histograms count fan memberships, which can count one deletion colouring in several fans; independently reconstructed distinct-start counts are supplied in the final summary JSON.','',
            '## Seven fixed statements','',
            '| Statement | P1 | P3 |', '| --- | --- | --- |']
    for stmt in ('M1','M2','M3','C1','C2','C3','U_exists'):
        cells=[]
        for phase in ('P1','P3'):
            v=stats[phase]['statements'][stmt]
            cells.append((f"**Killed on {', '.join(str(n)+':'+str(i) for n,i in v['killed'])}**; " if v['killed_count'] else '')+f"{v['passed']:,} passed"+(f"; {v['not_applicable']:,} labelled not applicable" if v['not_applicable'] else ''))
        lines.append(f"| {'U∃' if stmt=='U_exists' else stmt} | {' | '.join(cells)} |")
    lines+=['','Every row has zero unresolved cases. The producer labels C3 not applicable when all degrees are already 5 or 6. C1 and C3 are false on 24:6406; M2 is false on 24:7228. M3 additionally has a general hand proof in `MathShortFillTheorem.md`, independently reviewed by both parallel teams. That proof is separate from the unchanged experimental test. M2, C1 and C3 are disproved by finite counterexamples. M1/C2/U∃ passed on the tested graphs and remain universal conjectures.','',
            '## Counterexamples','',
            '**24:6406 kills C1 and C3.** Every one of its 70 legal vertex/fan pairs has a start with no mixed fill in zero, one or two moves. At least one pair has maximum exactly three, so m=3. The degree multiset is fourteen 5s, eight 6s and two 7s: this simultaneously refutes m≤2 at order≥18 and the implication m≥3⇒all degrees 5/6. All these are exhaustive finite certificates; U∃ nevertheless holds.','',
            '**24:7228 kills M2.** At vertex 17, fan 0, the certified start has exact ℓ=3 and κ=5. The mixed path is slide to 8, K(1,2,seed 1), K(0,1,seed 0), in canonical labels after each move. The certificate excludes every pure Kempe fill through depth four; the complete independent replay establishes the exact distance five. Thus κ−ℓ=2, contradicting the proposed allowance of one extra Kempe swap. This graph still has m=1: its good choice of vertex/fan does not prevent a harder individual start elsewhere.','',
            'Full ASCII rotations, starts, all-pair lower witnesses and the mixed path are preserved in the complete P3 archive. Graph indices and vertices are zero-based. Both parallel teams separately rechecked all 70 lower certificates and the complete best-pair upper bound, and reconstructed the exact 3/5 witness. Team B also independently rebuilt a successful U∃ pair on each graph. The isolated readable exhibit is MathWP19Counterexamples.md; the accompanying extraction JSON also retains both full graph records. These kills do not refute VH∃ or U∃.','',
            '## Independent verification','',
            'The released certificate checker re-parsed every graph, verified pair coverage, replayed every saved path and reconstructed every listed all-locked T* class. It explicitly does not certify positive U verdicts, start counts or distance histograms. Math therefore used a separate implementation importing only its own old audit move code: it enumerated every deletion colouring at every hole, rebuilt mixed and Kempe distances, filtered every legal fan family, reconstructed every T* class and re-derived all graph and phase summaries. P3 was replayed as records completed, with final checks binding those records to the finished file, frozen sources, declaration and entire raw input. No replay findings were fed back into the producer.','',
            '| Phase | Producer seconds | Replay seconds | Peak producer worker KiB | Saved paths checked | All-locked classes checked |',
            '| --- | ---: | ---: | ---: | ---: | ---: |']
    for phase,s in stats.items():
        c=s['certificate_stats'];lines.append(f"| {phase} | {s['producer_seconds']} | {s['replay_seconds']} | {s['peak_worker_KiB']:,} | {c['witnesses_verified']:,} | {c['u_fail_classes_verified']:,} |")
    lines+=['','P3 replay time includes waiting for producer records; it overlaps the producer and is not an additional sequential cost. P1 used 12 producer workers and P2 used four. P3 used 12 producer and 12 replay workers concurrently. The declaration’s 30-minute per-graph, 12-hour per-phase, 8-GiB per-worker and 1-GB output limits were not reached.','',
            '## Integrity and release','',
            'Written Math releases were `8dffb45` (P1/P2) and `81b2bf7` (P3 after the verified P1 cost checkpoint), under the user’s existing autonomous release. Declaration digest: `56d1c97b8b913822822fe0ce5c8b4f2d05827c9845a1810c61037619e4b85a9e`. Producer/checker regressions and the independent replay corruption regressions passed. Frozen sources and imported dependencies were hash-checked; none was tuned between phases.','',
            'Each full phase output is preserved as deterministic lossless gzip in `longtable/wp19/wp19-P*.json.gz`; raw JSON also remains in the workspace. `WP19-verified-output-manifest.json` binds raw and archive sizes/digests to certificate and complete-replay files, and records decompression round-trip verification. Exact input hashes and every graph-level record are preserved. To inspect an archive, decompress it to a fresh path and verify its raw digest against that manifest.','',
            'Order-23/24 graph sets had already appeared in the night swarm’s exploratory q/lin rank sweeps. These move/class statistics are fresh; the graph sets are not pristine holdouts. No graph beyond these released phases was run. WP12 remains withdrawn.','',
            '## Next session','',
            'Long Table owns corrections to its source proof pages: promote M3 with its precise move conventions, remove the false converse after Lemma F, and distinguish uniform all-start bounds from existential VH∃. Navigator can record accepted finite results, the reviewed belt theorem with its Florek dependency, the conditional VH∃ induction route and the short-fill theorem. Universal vacancy remains exploring. Any further computation requires a new declaration; none is launched by this report.']
    (repo/'SolvingFrameworkPlan'/'MathWP19Results.md').write_text('\n'.join(lines)+'\n')
    print('PASS report',json.dumps({k:{j:v for j,v in s.items() if j in ('graphs','pairs','m_hist','max_l','max_k')} for k,s in stats.items()}),flush=True)

if __name__=='__main__':main()
