\ Model MLV-S2
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  0 x_sfj[S1,F1,J1] + 0 x_sfj[S1,F1,J2] + 0 x_sfj[S1,F2,J1]
   + 0 x_sfj[S1,F2,J2] + 0 x_sfj[S2,F1,J1] + 0 x_sfj[S2,F1,J2]
   + 0 x_sfj[S2,F2,J1] + 0 x_sfj[S2,F2,J2] + 0 x_fdj[F1,D1,J1]
   + 0 x_fdj[F1,D1,J2] + 0 x_fdj[F1,D2,J1] + 0 x_fdj[F1,D2,J2]
   + 0 x_fdj[F2,D1,J1] + 0 x_fdj[F2,D1,J2] + 0 x_fdj[F2,D2,J1]
   + 0 x_fdj[F2,D2,J2] - 15000 x_dcj[D1,C1,J1] - 112500 x_dcj[D1,C1,J2]
   - 15000 x_dcj[D1,C2,J1] - 120000 x_dcj[D1,C2,J2] - 15000 x_dcj[D1,C3,J1]
   - 15000 x_dcj[D1,C3,J2] - 15000 x_dcj[D1,C4,J1] - 15000 x_dcj[D1,C4,J2]
   - 15000 x_dcj[D2,C1,J1] - 112500 x_dcj[D2,C1,J2] - 15000 x_dcj[D2,C2,J1]
   - 120000 x_dcj[D2,C2,J2] - 15000 x_dcj[D2,C3,J1] - 15000 x_dcj[D2,C3,J2]
   - 15000 x_dcj[D2,C4,J1] - 15000 x_dcj[D2,C4,J2] + 0 zp1_ssj[S1,S2,J1]
   + 0 zp1_ssj[S1,S2,J2] + 0 zp1_ssj[S2,S1,J1] + 0 zp1_ssj[S2,S1,J2]
   + 0 zp2_ssj[S1,S2,J1] + 0 zp2_ssj[S1,S2,J2] + 0 zp2_ssj[S2,S1,J1]
   + 0 zp2_ssj[S2,S1,J2] + 0 zm1_ffj[F1,F2,J1] + 0 zm1_ffj[F1,F2,J2]
   + 0 zm1_ffj[F2,F1,J1] + 0 zm1_ffj[F2,F1,J2] + 0 zm2_ffj[F1,F2,J1]
   + 0 zm2_ffj[F1,F2,J2] + 0 zm2_ffj[F2,F1,J1] + 0 zm2_ffj[F2,F1,J2]
   + 4.734375e+07 Constant + [ 300 x_dcj[D1,C1,J1] ^2
   + 600 x_dcj[D1,C1,J1] * x_dcj[D2,C1,J1] + 300 x_dcj[D1,C1,J2] ^2
   + 600 x_dcj[D1,C1,J2] * x_dcj[D2,C1,J2] + 300 x_dcj[D1,C2,J1] ^2
   + 600 x_dcj[D1,C2,J1] * x_dcj[D2,C2,J1] + 300 x_dcj[D1,C2,J2] ^2
   + 600 x_dcj[D1,C2,J2] * x_dcj[D2,C2,J2] + 300 x_dcj[D1,C3,J1] ^2
   + 600 x_dcj[D1,C3,J1] * x_dcj[D2,C3,J1] + 300 x_dcj[D1,C3,J2] ^2
   + 600 x_dcj[D1,C3,J2] * x_dcj[D2,C3,J2] + 300 x_dcj[D1,C4,J1] ^2
   + 600 x_dcj[D1,C4,J1] * x_dcj[D2,C4,J1] + 300 x_dcj[D1,C4,J2] ^2
   + 600 x_dcj[D1,C4,J2] * x_dcj[D2,C4,J2] + 300 x_dcj[D2,C1,J1] ^2
   + 300 x_dcj[D2,C1,J2] ^2 + 300 x_dcj[D2,C2,J1] ^2
   + 300 x_dcj[D2,C2,J2] ^2 + 300 x_dcj[D2,C3,J1] ^2
   + 300 x_dcj[D2,C3,J2] ^2 + 300 x_dcj[D2,C4,J1] ^2
   + 300 x_dcj[D2,C4,J2] ^2 ] / 2 
Subject To
Bounds
 Constant = 1
End
