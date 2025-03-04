\ Model MLV-S1
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  3.5 x_sfj[S1,F1,J1] + 4.2 x_sfj[S1,F1,J2] + 4.5 x_sfj[S1,F2,J1]
   + 4.5 x_sfj[S1,F2,J2] + 0 x_fdj[] + 0 x_dcj[] + 1.25 zp1_ssj[S1,S2,J1]
   + 2.4 zp1_ssj[S1,S2,J2] - zp1_ssj[S2,S1,J1] - 2 zp1_ssj[S2,S1,J2]
   + 2.625 zp2_ssj[S1,S2,J1] + 0.7 zp2_ssj[S1,S2,J2]
   - 2.25 zp2_ssj[S2,S1,J1] - 0.5 zp2_ssj[S2,S1,J2]
Subject To
 suppier1[S1]: x_sfj[S1,F1,J1] + x_sfj[S1,F1,J2] + x_sfj[S1,F2,J1]
   + x_sfj[S1,F2,J2] + zp1_ssj[S1,S2,J1] + zp1_ssj[S1,S2,J2]
   - zp1_ssj[S2,S1,J1] - zp1_ssj[S2,S1,J2] <= 300
 suppier2[S1]: x_sfj[S1,F1,J1] + x_sfj[S1,F1,J2] + x_sfj[S1,F2,J1]
   + x_sfj[S1,F2,J2] + zp2_ssj[S1,S2,J1] + zp2_ssj[S1,S2,J2]
   - zp2_ssj[S2,S1,J1] - zp2_ssj[S2,S1,J2] <= 1900
 suppier3[S1]: zp1_ssj[S1,S2,J1] + zp1_ssj[S1,S2,J2] <= 0
 suppier4[S1]: 1.5 zp2_ssj[S1,S2,J1] + 0.5 zp2_ssj[S1,S2,J2] <= 1600
 suppier5[J1,S1]: x_sfj[S1,F1,J1] + x_sfj[S1,F2,J1] - zp1_ssj[S2,S1,J1]
   >= 0
 suppier5[J2,S1]: x_sfj[S1,F1,J2] + x_sfj[S1,F2,J2] - zp1_ssj[S2,S1,J2]
   >= 0
 suppier6[J1,S1]: x_sfj[S1,F1,J1] + x_sfj[S1,F2,J1] - 1.5 zp2_ssj[S2,S1,J1]
   >= 0
 suppier6[J2,S1]: x_sfj[S1,F1,J2] + x_sfj[S1,F2,J2] - 0.5 zp2_ssj[S2,S1,J2]
   >= 0
Bounds
End
