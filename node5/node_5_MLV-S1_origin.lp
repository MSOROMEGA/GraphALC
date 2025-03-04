\ Model MLV-S1
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  0 x_sfj[] + 2 x_dcj[D1,C1,J1] + 3 x_dcj[D1,C1,J2] + 3 x_dcj[D1,C2,J1]
   + 2.5 x_dcj[D1,C2,J2] + x_dcj[D1,C3,J1] + 2.2 x_dcj[D1,C3,J2]
   + 2 x_dcj[D1,C4,J1] + 1.5 x_dcj[D1,C4,J2]
Subject To
 Depot2[D1]: x_fdj[F1,D1,J1] + x_fdj[F1,D1,J2] + x_fdj[F2,D1,J1]
   + x_fdj[F2,D1,J2] <= 1100
 Depot1[J1,D1]: - x_fdj[F1,D1,J1] - x_fdj[F2,D1,J1] + x_dcj[D1,C1,J1]
   + x_dcj[D1,C2,J1] + x_dcj[D1,C3,J1] + x_dcj[D1,C4,J1] = 0
 Depot1[J2,D1]: - x_fdj[F1,D1,J2] - x_fdj[F2,D1,J2] + x_dcj[D1,C1,J2]
   + x_dcj[D1,C2,J2] + x_dcj[D1,C3,J2] + x_dcj[D1,C4,J2] = 0
Bounds
End
