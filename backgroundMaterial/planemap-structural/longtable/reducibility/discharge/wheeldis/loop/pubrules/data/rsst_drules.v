(* Extracted from coq-community/fourcolor theories/proof/discharge.v (master), (c) 2006-2015 Microsoft Corporation and Inria, CeCILL-B. md5 of source: 5b8491c3b98d13f5e49df5829a688494 *)
Definition drule1 := Part $ * $ * $ 6+ $ * $ * $.
Definition drule2  := Part $ * $ 5 $ 7+ $ * $ * $.
Definition drule2' := Part $ * $ 5 $ 7+ $ * $ * $ * $.
Definition drule3  := Part $ 5 $ 6- $ 6+ $ * $ * $.
Definition drule3' := Part $ 5 $ 6- $ 6+ $ * $ * $ * $.
Definition drule4  := Part $ 6- $[5] 5 $ 6+ $ * $ * $ * $.
Definition drule4' := Part $ 6- $[5] 6 $ 6+ $ * $ * $ * $.
Definition drule5 := Part $ 6 $[6- 5] 6 $ 6+ $ * $ * $ * $.
Definition drule6 := Part $ 6 $[6-] 5 $[5] 7+ $ * $ * $ * $.
Definition drule7 := Part $ 6 $[6 6-] 6 $[5] 7+ $ * $ * $ * $.
Definition drule8 := Part $ 5 $ 6- $ 7+ $ * $ * $ * $ * $.
Definition drule9 := Part $ 6- $ 6- $ 7+ $ * $ * $ * $ 5 $.
Definition drule10  := Part $ 5 $ 5 $ 7+ $ 5 $ 6+ $ * $ * $.
Definition drule10' := Part $ 5 $ 5 $ 7+ $ 5 $ 5 $ * $ * $.
Definition drule11 := Part $ 6 $[5] 5 $ 7+ $ 5 $ 6+ $ * $ * $.
Definition drule12 := Part $ 5 $[5] 5 $ 7+ $ 5 $[5] 5 $ * $ * $.
Definition drule13 := Part $ 6 $[5] 5 $[5] 8+ $ 5 $ 5 $ * $ * $.
Definition drule14 := Part $ 5 $[5] 6 $ 7+ $ 5 $ * $ * $ * $.
Definition drule15 := Part $ 5 $ 6 $ 7+ $ 5 $ 7+ $ 5 $ 6 $.
Definition drule16 := Part $ 6 $ 6 $ 7+ $ 5 $ 5 $ 5 $ 6 $.
Definition drule17 := Part $ 5 $[6] 6 $ 7+ $ 5 $ 5 $ 7+ $ 5 $.
Definition drule18 := Part $ 6 $[5] 5 $[5] 7 $ 6+ $ * $ * $ 5 $.
Definition drule19 := Part $ 6 $ 6+ $ 8+ $[5] 5 $[5] 6 $ 5 $ 6 $.
Definition drule20 := Part $ 5 $ 6 $ 7+ $ 6 $ 6 $ 5 $ 5 $.
Definition drule21 := Part $ 6- $ 6 $[5] 7 $ 6+ $ * $ 5 $ 5 $.
Definition drule22 := Part $ 5 $ 6 $[5] 7 $ 6+ $ * $ 5 $ 6 $.
Definition drule23 := Part $ 5 $[5] 7 $ 7+ $ 5 $ * $ * $ * $.
Definition drule24 := Part $ 5 $ 5 $[5] 7 $ 7+ $ 6 $ 6 $ 5 $.
Definition drule25 := Part $ 5 $ 5 $ 7+ $[* * 5] 7 $[6] 5 $ 5 $ * $.
Definition drule26 := Part $ 6 $ 6 $[5] 7 $ 7+ $ 5 $ 5 $ 6 $.
Definition drule27 := Part $ 7+ $ 6 $[6 5 6+] 7 $ 7 $[5] 6- $ * $ * $.
Definition drule28 := Part $ 5 $ 5 $ 7+ $ 5 $ 5 $ * $ * $ 5 $.
Definition drule29 := Part $ 5 $[5] 5 $ 7+ $ 5 $ * $ * $ 5 $ 5 $.
Definition drule30 := Part $ 5 $ 5 $ 7+ $ 5 $[5] 6 $ 5 $ * $ * $.
Definition drule31  := Part $ 5 $[5] 5 $ 7+ $ 5 $[6+] 5 $ 6+ $ * $ 6+ $.
Definition drule31' := Part $ 5 $[5] 5 $ 7+ $ 5 $[5] 5 $ 6+ $ * $ 6+ $.
Definition drule32 := Part $ 5 $ 6 $[5] 7 $ 7+ $ 6 $ 5 $ 5 $ 5 $.
Definition base_drules : drules := @seqn part 38
 drule1  drule1  drule2  drule2' drule3  drule3'  drule4  drule4' drule5
 drule6  drule7  drule8  drule9  drule10 drule10'
 drule11 drule12 drule13 drule14 drule15 drule16 drule17 drule18 drule19
 drule20 drule21 drule22 drule23 drule24 drule25 drule26 drule27 drule28 drule29
 drule30 drule31 drule31' drule32.
