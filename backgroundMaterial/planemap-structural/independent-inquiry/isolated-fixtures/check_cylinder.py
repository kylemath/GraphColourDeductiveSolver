import runpy
s=runpy.run_path('/tmp/isolated-fixtures-work/build.py'); ff=s['from_faces'];fo=s['face_orbits']
for m in [2,3,4,8,20]:
 v=lambda i,j:1+5*i+j%5
 top=0;bottom=5*m+1;fs=[]
 for j in range(5): fs.extend([(top,v(0,j+1),v(0,j)),(bottom,v(m-1,j),v(m-1,j+1))])
 for i in range(m-1):
  for j in range(5):fs.extend([(v(i,j),v(i,j+1),v(i+1,j)),(v(i,j),v(i+1,j),v(i+1,j-1))])
 r=ff(5*m+2,fs);assert len(fo(r))==10*m
 hist={d:sum(len(ns)==d for ns in r) for d in [5,6]}
 assert hist=={5:12,6:5*m-10}
 print('cylinder',m,'vertices',len(r),'degrees',hist)
