import json,os,sys,urllib.request
E=os.environ.get("MAKEFUN_ENV_URL") or sys.exit("no env")
V={"P":100,"N":320,"B":330,"R":500,"Q":900,"K":0}
KN=[(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]
KD=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
RD=[(1,0),(-1,0),(0,1),(0,-1)];BD=[(1,1),(1,-1),(-1,1),(-1,-1)]
def post(p,b):
 r=urllib.request.Request(E+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 return json.load(urllib.request.urlopen(r))
def parse(f):
 b={}
 for i,row in enumerate(f.split()[0].split("/")):
  j=0
  for c in row:
   if c.isdigit():j+=int(c)
   else:b[chr(97+j)+str(8-i)]=c;j+=1
 return b
def tofen(b):
 o=[]
 for i in range(8,0,-1):
  r="";e=0
  for c in "abcdefgh":
   p=b.get(c+str(i))
   if p is None:e+=1
   else:
    if e:r+=str(e);e=0
    r+=p
  o.append(r+str(e) if e else r)
 return "/".join(o)
def gen(b,w,ep):
 o=[]
 for s,p in b.items():
  if p.isupper()!=w:continue
  u=p.upper();f=ord(s[0])-97;r=int(s[1])
  if u=="P":
   d=1 if w else -1;t=s[0]+str(r+d)
   if t not in b:
    o.append(s+t)
    t2=s[0]+str(r+2*d)
    if r==(2 if w else 7) and t2 not in b:o.append(s+t2)
   for df in(-1,1):
    c=chr(97+f+df)
    if c<"a"or c>"h":continue
    t=c+str(r+d)
    if t in b and b[t].isupper()!=w or t==ep:o.append(s+t)
  elif u=="N":
   for df,dr in KN:
    c=chr(97+f+df);rr=r+dr
    if "a"<=c<="h" and 1<=rr<=8:
     t=c+str(rr)
     if b.get(t,"x").isupper()!=w or t not in b:o.append(s+t)
  elif u=="K":
   for df,dr in KD:
    c=chr(97+f+df);rr=r+dr
    if "a"<=c<="h" and 1<=rr<=8:
     t=c+str(rr)
     if b.get(t,"x").isupper()!=w or t not in b:o.append(s+t)
  else:
   for df,dr in (RD if u=="R" else BD if u=="B" else RD+BD):
    c=chr(97+f+df);rr=r+dr
    while "a"<=c<="h" and 1<=rr<=8:
     t=c+str(rr)
     if t in b:
      if b[t].isupper()!=w:o.append(s+t)
      break
     o.append(s+t);c=chr(ord(c)+df);rr+=dr
 return o
def mv(b,m):
 n=dict(b);p=n.pop(m[:2],None)
 if p and p.upper()=="P" and m[0]!=m[2] and m[2:]not in n:n.pop(m[2]+m[1],None)
 n[m[2:]]=p
 return n
def ev(b,w):
 s=0
 for q,p in b.items():
  v=V[p.upper()];f=ord(q[0])-97;r=int(q[1])-1
  if p.upper()!="K":v-=int((f-3.5)**2+(r-3.5)**2)
  s+=v if p.isupper()else-v
 return s if w else -s
def srch(b,w,d,a,be,ep):
 if d==0:return ev(b,w)
 ms=gen(b,w,ep)
 if not ms:return -9999
 bs=-99999
 for m in ms:
  s=-srch(mv(b,m),not w,d-1,-be,-a,"-")
  if s>bs:bs=s
  if s>a:a=s
  if a>=be:break
 return bs
def pick(f,legal):
 b=parse(f);w=f.split()[1]=="w";ep=f.split()[3]
 bs=-99999;best=legal[0]
 for d in (2,3,4):
  a=-99999;bm=best
  for m in sorted(legal,key=lambda m:-(0 if m[2:]in b else -10)):
   s=-srch(mv(b,m),not w,d-1,-99999,-a,"-")
   if s>a:a=s;bm=m
  best=bm
 return best
while 1:
 g=post("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  g=post("/move",{"game":g["game"],"move":pick(g["fen"],g["legal_moves"])})
 print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)
