import sys, numpy as np
from scipy.interpolate import griddata
f, p01, t01, mdot_pp = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
d=np.genfromtxt(f,delimiter=',',skip_header=1)
p0,T0,rho,vx,vy,vz,x,y,z=d.T
r=np.hypot(x,y); th=np.arctan2(y,x)
vt=(x*vy-y*vx)/r
pitch=2*np.pi/36
rh,rt=0.19381,0.23823
rm=0.5*(rh+rt)
# replicate one pitch either side (scalars/cyl. components are rotation-invariant)
R=np.concatenate([r,r,r]); TH=np.concatenate([th-pitch,th,th+pitch])
F=np.vstack([p0,T0,rho,vz,vt]).T; F=np.vstack([F,F,F])
th0=th.min()
nr,nt=600,600
rg=rh+(rt-rh)*(0.5*(1-np.cos(np.linspace(0,np.pi,nr))))   # clustered at walls
tg=th0+pitch*(np.arange(nt)+0.5)/nt
RG,TG=np.meshgrid(rg,tg,indexing='ij')
pts=np.c_[R, rm*TH]; q=np.c_[RG.ravel(), rm*TG.ravel()]
G=griddata(pts,F,q,method='linear')
bad=np.isnan(G[:,0])
if bad.any(): G[bad]=griddata(pts,F,q[bad],method='nearest')
G=G.reshape(nr,nt,5)
gp0,gT0,grho,gvz,gvt=[G[...,i] for i in range(5)]
# area weights r dr dtheta (trapezoid in r)
dr=np.gradient(rg); A=(rg*dr)[:,None]*np.full((1,nt),pitch/nt)
m=grho*gvz*A
print(f"points {len(r)}, NaN-filled grid pts {bad.sum()}")
print(f"mass flow per passage: integrated {m.sum():.5f} kg/s vs STAR {mdot_pp:.5f}  ({100*(m.sum()/mdot_pp-1):+.2f}%)")
P0=(m*gp0).sum()/m.sum(); TT=(m*gT0).sum()/m.sum()
pr=P0/p01; tr=TT/t01; eta=(pr**0.28601-1)/(tr-1)
print(f"plane mass-avg: p0 {P0:.0f} Pa  T0 {TT:.3f} K  PR {pr:.4f} TR {tr:.4f} eta {eta:.4f}")
# spanwise: mass-average around circumference at each radius
mr=m.sum(1)
span=(rg-rh)/(rt-rh)*100
pr_s=(m*gp0).sum(1)/mr/p01; tr_s=(m*gT0).sum(1)/mr/t01
eta_s=(pr_s**0.28601-1)/(tr_s-1)
ang=np.degrees(np.arctan2(-(m*gvt).sum(1),(m*gvz).sum(1)))   # swirl in rotation (-theta) direction positive
out=np.c_[span,pr_s,tr_s,eta_s,ang]
np.savetxt(sys.argv[5],out,delimiter=',',header='span_pct,p0_ratio,t0_ratio,eta,abs_flow_angle_deg',comments='',fmt='%.5f')
