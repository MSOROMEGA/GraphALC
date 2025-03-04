\ Model MLV-S1
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  - 15000 x_dcj[D1,C1,J1] - 112500 x_dcj[D1,C1,J2] - 15000 x_dcj[D1,C2,J1]
   - 120000 x_dcj[D1,C2,J2] - 15000 x_dcj[D1,C3,J1] - 15000 x_dcj[D1,C3,J2]
   - 15000 x_dcj[D1,C4,J1] - 15000 x_dcj[D1,C4,J2] - 15000 x_dcj[D2,C1,J1]
   - 112500 x_dcj[D2,C1,J2] - 15000 x_dcj[D2,C2,J1]
   - 120000 x_dcj[D2,C2,J2] - 15000 x_dcj[D2,C3,J1] - 15000 x_dcj[D2,C3,J2]
   - 15000 x_dcj[D2,C4,J1] - 15000 x_dcj[D2,C4,J2] + 4.734375e+07 Constant
   + [ 300 x_dcj[D1,C1,J1] ^2 + 600 x_dcj[D1,C1,J1] * x_dcj[D2,C1,J1]
   + 300 x_dcj[D1,C1,J2] ^2 + 600 x_dcj[D1,C1,J2] * x_dcj[D2,C1,J2]
   + 300 x_dcj[D1,C2,J1] ^2 + 600 x_dcj[D1,C2,J1] * x_dcj[D2,C2,J1]
   + 300 x_dcj[D1,C2,J2] ^2 + 600 x_dcj[D1,C2,J2] * x_dcj[D2,C2,J2]
   + 300 x_dcj[D1,C3,J1] ^2 + 600 x_dcj[D1,C3,J1] * x_dcj[D2,C3,J1]
   + 300 x_dcj[D1,C3,J2] ^2 + 600 x_dcj[D1,C3,J2] * x_dcj[D2,C3,J2]
   + 300 x_dcj[D1,C4,J1] ^2 + 600 x_dcj[D1,C4,J1] * x_dcj[D2,C4,J1]
   + 300 x_dcj[D1,C4,J2] ^2 + 600 x_dcj[D1,C4,J2] * x_dcj[D2,C4,J2]
   + 300 x_dcj[D2,C1,J1] ^2 + 300 x_dcj[D2,C1,J2] ^2
   + 300 x_dcj[D2,C2,J1] ^2 + 300 x_dcj[D2,C2,J2] ^2
   + 300 x_dcj[D2,C3,J1] ^2 + 300 x_dcj[D2,C3,J2] ^2
   + 300 x_dcj[D2,C4,J1] ^2 + 300 x_dcj[D2,C4,J2] ^2 ] / 2 
Subject To
Bounds
 Constant = 1
End
