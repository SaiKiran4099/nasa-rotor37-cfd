import os
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
NASA=os.path.join(ROOT,'data','nasa','nasa_st4_profiles.csv')
PROF=lambda f: os.path.join(ROOT,'data','cfd','profiles',f)
import numpy as np, csv
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
L=[('cfd_vcoarse_M204_profile.csv','very coarse (0.83 M)',':','#b0b0b0'),('cfd_coarse_M204_profile.csv','coarse (1.54 M)','--','#7a7a7a'),('cfd_M204_profile.csv','medium (3.71 M)','-','#1f5fbf')]
D=[np.genfromtxt(PROF(f),delimiter=',',names=True) for f,_,_,_ in L]
rows=[r for r in csv.DictReader(open(NASA)) if r['point']=='peak_eff']
ns=np.array([float(r['span_pct']) for r in rows])
N={k:[float(r[k]) for r in rows] for k in ['p0_ratio','t0_ratio','eta','abs_flow_angle_deg']}
print(f"{'span':>4} | PR vc     c      m   | eta vc   c      m")
for s in [10,30,50,70,85,94]:
    v=[np.interp(s,d['span_pct'],d['p0_ratio']) for d in D]; e=[np.interp(s,d['span_pct'],d['eta']) for d in D]
    print(f"{s:4d} | {v[0]:.4f} {v[1]:.4f} {v[2]:.4f} | {e[0]:.4f} {e[1]:.4f} {e[2]:.4f}")
fig,ax=plt.subplots(1,4,figsize=(15,5.5),sharey=True)
for a,k,t in zip(ax,['p0_ratio','t0_ratio','eta','abs_flow_angle_deg'],['Total pressure ratio','Total temperature ratio','Efficiency (local)','Absolute flow angle (deg)']):
    for d,(f,lab,ls,c) in zip(D,L): a.plot(d[k],d['span_pct'],ls,color=c,lw=2,label='CFD '+lab)
    a.plot(N[k],ns,'o',mfc='none',mec='#c0392b',mew=1.6,ms=6,label='NASA peak eff')
    a.set_title(t); a.grid(alpha=.3)
    if k=='eta': a.set_xlim(0.6,1.0)
ax[0].set_ylabel('% span (hub = 0)'); ax[0].set_ylim(0,100); ax[0].legend(loc='lower left',fontsize=8)
fig.suptitle('Rotor 37 Station 4, M204 (peak eff): three-level grid study vs NASA')
fig.tight_layout(); fig.savefig('st4_M204_grid_3level.png',dpi=150)
