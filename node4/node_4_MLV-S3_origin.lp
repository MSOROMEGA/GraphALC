\ Model MLV-S3
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  5 x_fdj[F2,D1,J1] + 4.3 x_fdj[F2,D1,J2] + 4 x_fdj[F2,D2,J1]
   + 3.6 x_fdj[F2,D2,J2] + 0 x_dcj[] - 2.4 zm1_ffj[F1,F2,J1]
   - zm1_ffj[F1,F2,J2] + 3.075 zm1_ffj[F2,F1,J1] + 1.1 zm1_ffj[F2,F1,J2]
   - 1.44 zm2_ffj[F1,F2,J1] - 1.2 zm2_ffj[F1,F2,J2] + 1.8 zm2_ffj[F2,F1,J1]
   + 1.44 zm2_ffj[F2,F1,J2]
Subject To
 factory2[F2]: 1.5 x_fdj[F2,D1,J1] + 0.5 x_fdj[F2,D1,J2]
   + 1.5 x_fdj[F2,D2,J1] + 0.5 x_fdj[F2,D2,J2] - zm1_ffj[F1,F2,J1]
   - zm1_ffj[F1,F2,J2] + zm1_ffj[F2,F1,J1] + zm1_ffj[F2,F1,J2] <= 1900
 factory3[F2]: 0.8 x_fdj[F2,D1,J1] + 1.2 x_fdj[F2,D1,J2]
   + 0.8 x_fdj[F2,D2,J1] + 1.2 x_fdj[F2,D2,J2] - zm2_ffj[F1,F2,J1]
   - zm2_ffj[F1,F2,J2] + zm2_ffj[F2,F1,J1] + zm2_ffj[F2,F1,J2] <= 1100
 factory4[F2]: 1.5 zm1_ffj[F2,F1,J1] + 0.5 zm1_ffj[F2,F1,J2] <= 800
 factory5[F2]: 0.8 zm2_ffj[F2,F1,J1] + 1.2 zm2_ffj[F2,F1,J2] <= 0
 factory6[J1,F2]: x_fdj[F2,D1,J1] + x_fdj[F2,D2,J1] - 1.5 zm1_ffj[F1,F2,J1]
   >= 0
 factory6[J2,F2]: x_fdj[F2,D1,J2] + x_fdj[F2,D2,J2] - 0.5 zm1_ffj[F1,F2,J2]
   >= 0
 factory7[J1,F2]: x_fdj[F2,D1,J1] + x_fdj[F2,D2,J1] - 0.8 zm2_ffj[F1,F2,J1]
   >= 0
 factory7[J2,F2]: x_fdj[F2,D1,J2] + x_fdj[F2,D2,J2] - 1.2 zm2_ffj[F1,F2,J2]
   >= 0
 factory1[J1,F2]: - x_sfj[S1,F2,J1] - x_sfj[S2,F2,J1] + x_fdj[F2,D1,J1]
   + x_fdj[F2,D2,J1] = 0
 factory1[J2,F2]: - x_sfj[S1,F2,J2] - x_sfj[S2,F2,J2] + x_fdj[F2,D1,J2]
   + x_fdj[F2,D2,J2] = 0
Bounds
End
