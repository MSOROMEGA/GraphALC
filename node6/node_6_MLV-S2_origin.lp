\ Model MLV-S2
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  0 x_sfj[] + x_dcj[D2,C1,J1] + x_dcj[D2,C1,J2] + 3 x_dcj[D2,C2,J1]
   + 2.8 x_dcj[D2,C2,J2] + 4 x_dcj[D2,C3,J1] + 4.4 x_dcj[D2,C3,J2]
   + 3 x_dcj[D2,C4,J1] + 3.5 x_dcj[D2,C4,J2]
Subject To
 Depot2[D2]: x_fdj[F1,D2,J1] + x_fdj[F1,D2,J2] + x_fdj[F2,D2,J1]
   + x_fdj[F2,D2,J2] <= 1100
 Depot1[J1,D2]: - x_fdj[F1,D2,J1] - x_fdj[F2,D2,J1] + x_dcj[D2,C1,J1]
   + x_dcj[D2,C2,J1] + x_dcj[D2,C3,J1] + x_dcj[D2,C4,J1] = 0
 Depot1[J2,D2]: - x_fdj[F1,D2,J2] - x_fdj[F2,D2,J2] + x_dcj[D2,C1,J2]
   + x_dcj[D2,C2,J2] + x_dcj[D2,C3,J2] + x_dcj[D2,C4,J2] = 0
Bounds
End
