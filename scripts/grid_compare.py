import os
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
NASA=os.path.join(ROOT,'data','nasa','nasa_st4_profiles.csv')
PROF=lambda f: os.path.join(ROOT,'data','cfd','profiles',f)
import numpy as np, csv
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
m=np.genfromtxt(PROF('cfd_M204_profile.csv'),delimiter=',',names=True)
c=np.genfromtxt(PROF('cfd_coarse_M204_profile.csv'),delimiter=',',names=True)
rows=[r for r in csv.DictReader(open(NASA)) if r['point']=='peak_eff']
ns=np.array([float(r['span_pct']) for r in rows])
N={'p0_ratio':[float(r['p0_ratio']) for r in rows],'t0_ratio':[float(r['t0_ratio']) for r in rows],'eta':[float(r['eta']) for r in rows],'abs_flow_angle_deg':[float(r['abs_flow_angle_deg']) for r in rows]}
print(f"{'span':>5} | {'PR crs':>7} {'med':>7} {'d%':>6} {'nasa':>7} | {'TR d%':>6} | {'eta crs':>7} {'med':>7} {'dpt':>6} {'nasa':>6}")
for s in [5,10,20,30,40,50,60,70,80,85,90,94,97]:
    f=lambda a,k: np.interp(s,a['span_pct'],a[k])
    nas=lambda k: np.interp(s,ns,N[k])
    print(f"{s:5.0f} | {f(c,'p0_ratio'):7.4f} {f(m,'p0_ratio'):7.4f} {100*(f(c,'p0_ratio')/f(m,'p0_ratio')-1):6.2f} {nas('p0_ratio'):7.4f} | {100*(f(c,'t0_ratio')/f(m,'t0_ratio')-1):6.2f} | {f(c,'eta'):7.4f} {f(m,'eta'):7.4f} {100*(f(c,'eta')-f(m,'eta')):6.2f} {nas('eta'):6.4f}")
fig,ax=plt.subplots(1,4,figsize=(15,5.5),sharey=True)
for a,k,t in zip(ax,['p0_ratio','t0_ratio','eta','abs_flow_angle_deg'],['Total pressure ratio','Total temperature ratio','Efficiency (local)','Absolute flow angle (deg)']):
    a.plot(c[k],c['span_pct'],'--',color='#8a8a8a',lw=1.8,label='CFD coarse (1.54 M)')
    a.plot(m[k],m['span_pct'],'-',color='#1f5fbf',lw=2,label='CFD medium (3.71 M)')
    a.plot(N[k],ns,'o',mfc='none',mec='#c0392b',mew=1.6,ms=6,label='NASA peak eff')
    a.set_title(t); a.grid(alpha=.3)
    if k=='eta': a.set_xlim(0.6,1.0)
ax[0].set_ylabel('% span (hub = 0)'); ax[0].set_ylim(0,100); ax[0].legend(loc='lower left',fontsize=8)
fig.suptitle('Rotor 37 Station 4, M204 (peak eff): mesh sensitivity — coarse vs medium vs NASA')
fig.tight_layout(); fig.savefig('st4_M204_grid_coarse_vs_medium.png',dpi=150)
