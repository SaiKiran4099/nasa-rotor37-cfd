# Celik-method GCI on the first three grid levels (very coarse/coarse/medium).
# Final study uses the medium/fine-lite pair with a conservative Roache GCI (Fs=3, p=2): see README.
import numpy as np
from scipy.optimize import brentq
N=np.array([3.71e6,1.54e6,0.834e6])
h=(1/N)**(1/3); r21=h[1]/h[0]; r32=h[2]/h[1]
print(f"r21={r21:.3f} r32={r32:.3f}")
def gci(name,f1,f2,f3):
    e21=f2-f1; e32=f3-f2; s=np.sign(e32/e21)
    def g(p): return p-abs(np.log(abs(e32/e21))+np.log((r21**p-s)/(r32**p-s)))/np.log(r21)
    p=0.5
    for _ in range(200): p=abs(np.log(abs(e32/e21))+np.log((r21**p-s)/(r32**p-s)))/np.log(r21)
    fext=(r21**p*f1-f2)/(r21**p-1)
    ea=abs((f1-f2)/f1); g21=1.25*ea/(r21**p-1)
    print(f"{name}: f1={f1:.4f} f2={f2:.4f} f3={f3:.4f} e21={e21:+.4f} e32={e32:+.4f} monotone={'yes' if s>0 else 'NO'} p={p:.2f} f_ext={fext:.4f} GCI_med={100*g21:.2f}%")
    for pp in (1.0,2.0):
        fe=(r21**pp*f1-f2)/(r21**pp-1); print(f"   assumed p={pp}: f_ext={fe:.4f}, GCI(Fs=3)={100*3*ea/(r21**pp-1):.2f}%")
gci('PR ',2.0616,2.0466,2.0373)
gci('TR ',1.2681,1.2660,1.2645)
gci('eta',0.8573,0.8546,0.8534)
