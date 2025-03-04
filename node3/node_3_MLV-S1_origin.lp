\ Model MLV-S1
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  4 x_fdj[F1,D1,J1] + 4.7 x_fdj[F1,D1,J2] + 4.2 x_fdj[F1,D2,J1]
   + 4.9 x_fdj[F1,D2,J2] + 0 x_dcj[] + 3.15 zm1_ffj[F1,F2,J1]
   + 0.925 zm1_ffj[F1,F2,J2] - 2.25 zm1_ffj[F2,F1,J1]
   - 0.65 zm1_ffj[F2,F1,J2] + 1.68 zm2_ffj[F1,F2,J1]
   + 2.94 zm2_ffj[F1,F2,J2] - 1.2 zm2_ffj[F2,F1,J1]
   - 2.28 zm2_ffj[F2,F1,J2]
Subject To
 factory2[F1]: 1.5 x_fdj[F1,D1,J1] + 0.5 x_fdj[F1,D1,J2]
   + 1.5 x_fdj[F1,D2,J1] + 0.5 x_fdj[F1,D2,J2] + zm1_ffj[F1,F2,J1]
   + zm1_ffj[F1,F2,J2] - zm1_ffj[F2,F1,J1] - zm1_ffj[F2,F1,J2] <= 300
 factory3[F1]: 0.8 x_fdj[F1,D1,J1] + 1.2 x_fdj[F1,D1,J2]
   + 0.8 x_fdj[F1,D2,J1] + 1.2 x_fdj[F1,D2,J2] + zm2_ffj[F1,F2,J1]
   + zm2_ffj[F1,F2,J2] - zm2_ffj[F2,F1,J1] - zm2_ffj[F2,F1,J2] <= 1900
 factory4[F1]: 1.5 zm1_ffj[F1,F2,J1] + 0.5 zm1_ffj[F1,F2,J2] <= 0
 factory5[F1]: 0.8 zm2_ffj[F1,F2,J1] + 1.2 zm2_ffj[F1,F2,J2] <= 1600
 factory6[J1,F1]: x_fdj[F1,D1,J1] + x_fdj[F1,D2,J1] - 1.5 zm1_ffj[F2,F1,J1]
   >= 0
 factory6[J2,F1]: x_fdj[F1,D1,J2] + x_fdj[F1,D2,J2] - 0.5 zm1_ffj[F2,F1,J2]
   >= 0
 factory7[J1,F1]: x_fdj[F1,D1,J1] + x_fdj[F1,D2,J1] - 0.8 zm2_ffj[F2,F1,J1]
   >= 0
 factory7[J2,F1]: x_fdj[F1,D1,J2] + x_fdj[F1,D2,J2] - 1.2 zm2_ffj[F2,F1,J2]
   >= 0
 factory1[J1,F1]: - x_sfj[S1,F1,J1] - x_sfj[S2,F1,J1] + x_fdj[F1,D1,J1]
   + x_fdj[F1,D2,J1] = 0
 factory1[J2,F1]: - x_sfj[S1,F1,J2] - x_sfj[S2,F1,J2] + x_fdj[F1,D1,J2]
   + x_fdj[F1,D2,J2] = 0
Bounds
End
