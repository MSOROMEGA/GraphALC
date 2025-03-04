\ Model MLV-S2
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  4.7 x_sfj[S2,F1,J1] + 4.7 x_sfj[S2,F1,J2] + 4 x_sfj[S2,F2,J1]
   + 4.4 x_sfj[S2,F2,J2] + 0 x_fdj[] + 0 x_dcj[] - 2 zp1_ssj[S1,S2,J1]
   - 1.5 zp1_ssj[S1,S2,J2] + 2.5 zp1_ssj[S2,S1,J1] + 1.8 zp1_ssj[S2,S1,J2]
   - 1.8 zp2_ssj[S1,S2,J1] - 0.75 zp2_ssj[S1,S2,J2]
   + 2.55 zp2_ssj[S2,S1,J1] + 0.9 zp2_ssj[S2,S1,J2]
Subject To
 suppier1[S2]: x_sfj[S2,F1,J1] + x_sfj[S2,F1,J2] + x_sfj[S2,F2,J1]
   + x_sfj[S2,F2,J2] - zp1_ssj[S1,S2,J1] - zp1_ssj[S1,S2,J2]
   + zp1_ssj[S2,S1,J1] + zp1_ssj[S2,S1,J2] <= 1900
 suppier2[S2]: x_sfj[S2,F1,J1] + x_sfj[S2,F1,J2] + x_sfj[S2,F2,J1]
   + x_sfj[S2,F2,J2] - zp2_ssj[S1,S2,J1] - zp2_ssj[S1,S2,J2]
   + zp2_ssj[S2,S1,J1] + zp2_ssj[S2,S1,J2] <= 850
 suppier3[S2]: zp1_ssj[S2,S1,J1] + zp1_ssj[S2,S1,J2] <= 1050
 suppier4[S2]: 1.5 zp2_ssj[S2,S1,J1] + 0.5 zp2_ssj[S2,S1,J2] <= 0
 suppier5[J1,S2]: x_sfj[S2,F1,J1] + x_sfj[S2,F2,J1] - zp1_ssj[S1,S2,J1]
   >= 0
 suppier5[J2,S2]: x_sfj[S2,F1,J2] + x_sfj[S2,F2,J2] - zp1_ssj[S1,S2,J2]
   >= 0
 suppier6[J1,S2]: x_sfj[S2,F1,J1] + x_sfj[S2,F2,J1] - 1.5 zp2_ssj[S1,S2,J1]
   >= 0
 suppier6[J2,S2]: x_sfj[S2,F1,J2] + x_sfj[S2,F2,J2] - 0.5 zp2_ssj[S1,S2,J2]
   >= 0
Bounds
End
