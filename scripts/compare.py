import os
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
NASA=os.path.join(ROOT,'data','nasa','nasa_st4_profiles.csv')
PROF=lambda f: os.path.join(ROOT,'data','cfd','profiles',f)
import sys, numpy as np, csv
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
cfd=np.genfromtxt(sys.argv[1],delimiter=',',names=True)
pt=sys.argv[2]; label=sys.argv[3]; png=sys.argv[4]
rows=[r for r in csv.DictReader(open(NASA)) if r['point']==pt]
ns=np.array([float(r['span_pct']) for r in rows])
N={k:np.array([float(r[c]) for r in rows]) for k,c in [('pr','p0_ratio'),('tr','t0_ratio'),('eta','eta'),('ang','abs_flow_angle_deg')]}
C={'pr':cfd['p0_ratio'],'tr':cfd['t0_ratio'],'eta':cfd['eta'],'ang':cfd['abs_flow_angle_deg']}
print(f"{'span':>6} {'PR cfd':>8} {'nasa':>7} {'d%':>6} | {'TR cfd':>7} {'nasa':>7} {'d%':>6} | {'eta cfd':>7} {'nasa':>6} {'dpts':>6} | {'ang cfd':>7} {'nasa':>6} {'ddeg':>5}")
for i,s in enumerate(ns):
    c={k:np.interp(s,cfd['span_pct'],C[k]) for k in C}
    print(f"{s:6.1f} {c['pr']:8.4f} {N['pr'][i]:7.4f} {100*(c['pr']/N['pr'][i]-1):6.2f} | {c['tr']:7.4f} {N['tr'][i]:7.4f} {100*(c['tr']/N['tr'][i]-1):6.2f} | {c['eta']:7.4f} {N['eta'][i]:6.4f} {100*(c['eta']-N['eta'][i]):6.2f} | {c['ang']:7.2f} {N['ang'][i]:6.2f} {c['ang']-N['ang'][i]:5.2f}")
fig,ax=plt.subplots(1,4,figsize=(15,5.5),sharey=True)
for a,k,t in zip(ax,['pr','tr','eta','ang'],['Total pressure ratio','Total temperature ratio','Efficiency (local)','Absolute flow angle (deg)']):
    a.plot(C[k],cfd['span_pct'],'-',color='#1f5fbf',lw=2,label=f'CFD {label} (STAR, medium mesh)')
    a.plot(N[k],ns,'o',mfc='none',mec='#c0392b',mew=1.6,ms=6,label=f'NASA {pt.replace("_"," ")}')
    a.set_title(t); a.grid(alpha=.3)
    if k=='eta': a.set_xlim(0.6,1.0)
ax[0].set_ylabel('% span (hub = 0)'); ax[0].set_ylim(0,100); ax[0].legend(loc='lower left',fontsize=8)
fig.suptitle(f'NASA Rotor 37, Station 4 (z = 106.7 mm): circumferential mass-averaged profiles — {label} vs NASA {pt.replace("_"," ")}')
fig.tight_layout(); fig.savefig(png,dpi=150)
