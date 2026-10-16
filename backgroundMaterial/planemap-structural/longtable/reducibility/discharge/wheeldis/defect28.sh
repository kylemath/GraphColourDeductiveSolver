#!/bin/zsh
# Job 28 task 3: resume the strict K = 4 defect searches (README §7.3.1 share table), nice 20.
# usage: defect28.sh 56   (centres 5 then 6)   |   defect28.sh 7
cd "$(dirname $0)"; O=out/job28
if [ "$1" = 56 ]; then
  nice -n 20 bin/defectc bin/defect_tables.txt 5 4 1 1000000000 60 55777 > $O/defK4_c5.txt 2> $O/defK4_c5.err
  nice -n 20 bin/defectc bin/defect_tables.txt 6 4 1 1000000000 60 556677 > $O/defK4_c6.txt 2> $O/defK4_c6.err
  echo done > $O/defK4_c56.DONE
else
  nice -n 20 bin/defectc bin/defect_tables.txt 7 4 1 1000000000 60 5556667 > $O/defK4_c7.txt 2> $O/defK4_c7.err
  echo done > $O/defK4_c7.DONE
fi
