"""Station 4 radial profiles: k-omega SST vs Spalart-Allmaras vs NASA at peak efficiency (M204)."""
import os, csv, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
P=lambda f: os.path.join(ROOT,'data','cfd','profiles',f)
S=np.genfromtxt(P('cfd_M204_profile.csv'),delimiter=',',names=True)
A=np.genfromtxt(P('cfd_M204_SA_profile.csv'),delimiter=',',names=True)
rows=[r for r in csv.DictReader(open(os.path.join(ROOT,'data','nasa','nasa_st4_profiles.csv'))) if r['point']=='peak_eff']
ns=np.array([float(r['span_pct']) for r in rows])
N={k:np.array([float(r[k]) for r in rows]) for k in ['p0_ratio','t0_ratio','eta','abs_flow_angle_deg']}
fig,ax=plt.subplots(1,4,figsize=(15,5.5),sharey=True)
for a,k,t in zip(ax,['p0_ratio','t0_ratio','eta','abs_flow_angle_deg'],['Total pressure ratio','Total temperature ratio','Efficiency (local)','Absolute flow angle (deg)']):
    a.plot(S[k],S['span_pct'],'-',color='#1f5fbf',lw=2,label='CFD k-omega SST')
    a.plot(A[k],A['span_pct'],'--',color='#e67e22',lw=2,label='CFD Spalart-Allmaras')
    a.plot(N[k],ns,'o',mfc='none',mec='#c0392b',mew=1.6,ms=6,label='NASA peak eff')
    a.set_title(t); a.grid(alpha=.3)
    if k=='eta': a.set_xlim(0.6,1.0)
ax[0].set_ylabel('% span (hub = 0)'); ax[0].set_ylim(0,100); ax[0].legend(loc='lower left',fontsize=8)
fig.suptitle('Rotor 37 Station 4, peak efficiency (medium mesh): SST vs SA vs NASA')
fig.tight_layout(); fig.savefig('st4_M204_SST_vs_SA.png',dpi=150)
