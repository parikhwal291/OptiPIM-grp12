\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0x1452d6d3badb255a
Minimize
  15 num_Mul_Col_Var + Out_Cost_Sys_Var + In_Cost_Sys_Var
   + num_Fil_Loading_Var
Subject To
 Integer_Loop_Bound_Var_Cons_L_0_0_O_0: - b_0_0_0_O_0 + L_0_0_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_0_1_O_0: - b_0_1_0_O_0 + L_0_1_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_0_2_O_0: - b_0_2_0_O_0 + L_0_2_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_1_0_O_0: - b_1_0_0_O_0 - 2 b_1_0_1_O_0
   - 4 b_1_0_2_O_0 - 5 b_1_0_3_O_0 - 8 b_1_0_4_O_0 - 10 b_1_0_5_O_0
   - 20 b_1_0_6_O_0 - 25 b_1_0_7_O_0 - 40 b_1_0_8_O_0 - 50 b_1_0_9_O_0
   - 100 b_1_0_10_O_0 - 200 b_1_0_11_O_0 + L_1_0_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_1_1_O_0: - b_1_1_0_O_0 - 2 b_1_1_1_O_0
   - 4 b_1_1_2_O_0 - 5 b_1_1_3_O_0 - 8 b_1_1_4_O_0 - 10 b_1_1_5_O_0
   - 20 b_1_1_6_O_0 - 25 b_1_1_7_O_0 - 40 b_1_1_8_O_0 - 50 b_1_1_9_O_0
   - 100 b_1_1_10_O_0 - 200 b_1_1_11_O_0 + L_1_1_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_1_2_O_0: - b_1_2_0_O_0 - 2 b_1_2_1_O_0
   - 4 b_1_2_2_O_0 - 5 b_1_2_3_O_0 - 8 b_1_2_4_O_0 - 10 b_1_2_5_O_0
   - 20 b_1_2_6_O_0 - 25 b_1_2_7_O_0 - 40 b_1_2_8_O_0 - 50 b_1_2_9_O_0
   - 100 b_1_2_10_O_0 - 200 b_1_2_11_O_0 + L_1_2_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_2_0_O_0: - b_2_0_0_O_0 - 3 b_2_0_1_O_0
   - 9 b_2_0_2_O_0 - 27 b_2_0_3_O_0 + L_2_0_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_2_1_O_0: - b_2_1_0_O_0 - 3 b_2_1_1_O_0
   - 9 b_2_1_2_O_0 - 27 b_2_1_3_O_0 + L_2_1_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_2_2_O_0: - b_2_2_0_O_0 - 3 b_2_2_1_O_0
   - 9 b_2_2_2_O_0 - 27 b_2_2_3_O_0 + L_2_2_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_3_0_O_0: - b_3_0_0_O_0 - 3 b_3_0_1_O_0
   - 9 b_3_0_2_O_0 - 27 b_3_0_3_O_0 + L_3_0_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_3_1_O_0: - b_3_1_0_O_0 - 3 b_3_1_1_O_0
   - 9 b_3_1_2_O_0 - 27 b_3_1_3_O_0 + L_3_1_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_3_2_O_0: - b_3_2_0_O_0 - 3 b_3_2_1_O_0
   - 9 b_3_2_2_O_0 - 27 b_3_2_3_O_0 + L_3_2_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_4_0_O_0: - b_4_0_0_O_0 - 2 b_4_0_1_O_0
   - 4 b_4_0_2_O_0 - 8 b_4_0_3_O_0 - 16 b_4_0_4_O_0 - 32 b_4_0_5_O_0
   - 64 b_4_0_6_O_0 + L_4_0_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_4_1_O_0: - b_4_1_0_O_0 - 2 b_4_1_1_O_0
   - 4 b_4_1_2_O_0 - 8 b_4_1_3_O_0 - 16 b_4_1_4_O_0 - 32 b_4_1_5_O_0
   - 64 b_4_1_6_O_0 + L_4_1_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_4_2_O_0: - b_4_2_0_O_0 - 2 b_4_2_1_O_0
   - 4 b_4_2_2_O_0 - 8 b_4_2_3_O_0 - 16 b_4_2_4_O_0 - 32 b_4_2_5_O_0
   - 64 b_4_2_6_O_0 + L_4_2_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_5_0_O_0: - b_5_0_0_O_0 - 5 b_5_0_1_O_0
   + L_5_0_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_5_1_O_0: - b_5_1_0_O_0 - 5 b_5_1_1_O_0
   + L_5_1_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_5_2_O_0: - b_5_2_0_O_0 - 5 b_5_2_1_O_0
   + L_5_2_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_6_0_O_0: - b_6_0_0_O_0 - 5 b_6_0_1_O_0
   + L_6_0_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_6_1_O_0: - b_6_1_0_O_0 - 5 b_6_1_1_O_0
   + L_6_1_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_6_2_O_0: - b_6_2_0_O_0 - 5 b_6_2_1_O_0
   + L_6_2_O_0 = 0
 C_0_0_O_0_Constraint: - delta_0_2_O_0 - delta_0_3_O_0 - Coeff_0_Comb_0_O_0
   - Coeff_0_Comb_1_O_0 - Coeff_0_Comb_4_O_0 - Coeff_0_Comb_5_O_0
   + C_0_0_O_0 = 0
 C_1_0_O_0_Constraint: - delta_1_2_O_0 - delta_1_3_O_0 - Coeff_1_Comb_0_O_0
   - Coeff_1_Comb_1_O_0 - Coeff_1_Comb_4_O_0 - Coeff_1_Comb_5_O_0
   + C_1_0_O_0 = 0
 C_2_0_O_0_Constraint: - delta_2_2_O_0 - delta_2_3_O_0 - Coeff_2_Comb_0_O_0
   - Coeff_2_Comb_1_O_0 - Coeff_2_Comb_4_O_0 - Coeff_2_Comb_5_O_0
   + C_2_0_O_0 = 0
 C_3_0_O_0_Constraint: - delta_3_2_O_0 - delta_3_3_O_0 - Coeff_3_Comb_0_O_0
   - Coeff_3_Comb_1_O_0 - Coeff_3_Comb_4_O_0 - Coeff_3_Comb_5_O_0
   + C_3_0_O_0 = 0
 [Op]_numChan_lower: num_PE_Sys_Var - 16 num_Channels_Sys_Var >= -15
 [Op]_numChan_upper: num_PE_Sys_Var - 16 num_Channels_Sys_Var <= 0
 [Op_0]_channel_Bandwidth_Var_constraint: - 256 num_Channels_Sys_Var
   + channel_Bandwidth_Var = 0
 P_R_LUT_single_sel_constraint: P_R_LUT_Sel_0_O_0 + P_R_LUT_Sel_1_O_0
   + P_R_LUT_Sel_2_O_0 + P_R_LUT_Sel_3_O_0 + P_R_LUT_Sel_4_O_0
   + P_R_LUT_Sel_5_O_0 + P_R_LUT_Sel_6_O_0 + P_R_LUT_Sel_7_O_0 = 1
 P_R_LUT_Coeff_One_constraint: - C_0_0_O_0 + P_R_LUT_Sel_0_O_0
   + P_R_LUT_Sel_1_O_0 + 3 P_R_LUT_Sel_2_O_0 + 3 P_R_LUT_Sel_3_O_0
   + 9 P_R_LUT_Sel_4_O_0 + 9 P_R_LUT_Sel_5_O_0 + 27 P_R_LUT_Sel_6_O_0
   + 27 P_R_LUT_Sel_7_O_0 = 0
 P_R_LUT_Coeff_Two_constraint: - C_1_0_O_0 + P_R_LUT_Sel_0_O_0
   + 5 P_R_LUT_Sel_1_O_0 + P_R_LUT_Sel_2_O_0 + 5 P_R_LUT_Sel_3_O_0
   + P_R_LUT_Sel_4_O_0 + 5 P_R_LUT_Sel_5_O_0 + P_R_LUT_Sel_6_O_0
   + 5 P_R_LUT_Sel_7_O_0 = 0
 R31: - P_R_LUT_Sel_0_O_0 - P_R_LUT_Sel_1_O_0 - P_R_LUT_Sel_2_O_0
   - P_R_LUT_Sel_3_O_0 - P_R_LUT_Sel_4_O_0 - P_R_LUT_Sel_5_O_0
   - P_R_LUT_Sel_6_O_0 - P_R_LUT_Sel_7_O_0 + PR_Sel_GCD_Value = 0
 Q_S_LUT_single_sel_constraint: Q_S_LUT_Sel_0_O_0 + Q_S_LUT_Sel_1_O_0
   + Q_S_LUT_Sel_2_O_0 + Q_S_LUT_Sel_3_O_0 + Q_S_LUT_Sel_4_O_0
   + Q_S_LUT_Sel_5_O_0 + Q_S_LUT_Sel_6_O_0 + Q_S_LUT_Sel_7_O_0 = 1
 Q_S_LUT_Coeff_One_constraint: - C_2_0_O_0 + Q_S_LUT_Sel_0_O_0
   + Q_S_LUT_Sel_1_O_0 + 3 Q_S_LUT_Sel_2_O_0 + 3 Q_S_LUT_Sel_3_O_0
   + 9 Q_S_LUT_Sel_4_O_0 + 9 Q_S_LUT_Sel_5_O_0 + 27 Q_S_LUT_Sel_6_O_0
   + 27 Q_S_LUT_Sel_7_O_0 = 0
 Q_S_LUT_Coeff_Two_constraint: - C_3_0_O_0 + Q_S_LUT_Sel_0_O_0
   + 5 Q_S_LUT_Sel_1_O_0 + Q_S_LUT_Sel_2_O_0 + 5 Q_S_LUT_Sel_3_O_0
   + Q_S_LUT_Sel_4_O_0 + 5 Q_S_LUT_Sel_5_O_0 + Q_S_LUT_Sel_6_O_0
   + 5 Q_S_LUT_Sel_7_O_0 = 0
 R35: - Q_S_LUT_Sel_0_O_0 - Q_S_LUT_Sel_1_O_0 - Q_S_LUT_Sel_2_O_0
   - Q_S_LUT_Sel_3_O_0 - Q_S_LUT_Sel_4_O_0 - Q_S_LUT_Sel_5_O_0
   - Q_S_LUT_Sel_6_O_0 - Q_S_LUT_Sel_7_O_0 + QS_Sel_GCD_Value = 0
 R36: - tmp_maxP_C_value_var - tmp_maxR_C_value_var
   + [Op_0]_num_input_Col_Term2_Term1_partial = 0
 R37: - tmp_maxQ_C_value_var - tmp_maxS_C_value_var
   + [Op_0]_num_input_Col_Term3_Term1_partial = 0
 In_Cost_Sys_Var_final_constraint: - 15 num_in_col_Var
   - tmp_In_Cost_Sys_Var + In_Cost_Sys_Var = 0
 [Op0]_LoopBoundBinaryConstraint_0_0: b_0_0_0_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_0_1: b_0_1_0_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_0_2: b_0_2_0_O_0 = 1
 [Op0]_LoopBoundMul_0_constraint: = 0
 [Op0]_LoopBoundBinaryConstraint_1_0: b_1_0_0_O_0 + b_1_0_1_O_0
   + b_1_0_2_O_0 + b_1_0_3_O_0 + b_1_0_4_O_0 + b_1_0_5_O_0 + b_1_0_6_O_0
   + b_1_0_7_O_0 + b_1_0_8_O_0 + b_1_0_9_O_0 + b_1_0_10_O_0 + b_1_0_11_O_0
   = 1
 [Op0]_LoopBoundBinaryConstraint_1_1: b_1_1_0_O_0 + b_1_1_1_O_0
   + b_1_1_2_O_0 + b_1_1_3_O_0 + b_1_1_4_O_0 + b_1_1_5_O_0 + b_1_1_6_O_0
   + b_1_1_7_O_0 + b_1_1_8_O_0 + b_1_1_9_O_0 + b_1_1_10_O_0 + b_1_1_11_O_0
   = 1
 [Op0]_LoopBoundBinaryConstraint_1_2: b_1_2_0_O_0 + b_1_2_1_O_0
   + b_1_2_2_O_0 + b_1_2_3_O_0 + b_1_2_4_O_0 + b_1_2_5_O_0 + b_1_2_6_O_0
   + b_1_2_7_O_0 + b_1_2_8_O_0 + b_1_2_9_O_0 + b_1_2_10_O_0 + b_1_2_11_O_0
   = 1
 [Op0]_LoopBoundMul_1_constraint: b_1_0_1_O_0 + 2 b_1_0_2_O_0
   + 2.321928094887362 b_1_0_3_O_0 + 3 b_1_0_4_O_0
   + 3.321928094887362 b_1_0_5_O_0 + 4.321928094887363 b_1_0_6_O_0
   + 4.643856189774724 b_1_0_7_O_0 + 5.321928094887363 b_1_0_8_O_0
   + 5.643856189774724 b_1_0_9_O_0 + 6.643856189774724 b_1_0_10_O_0
   + 7.643856189774724 b_1_0_11_O_0 + b_1_1_1_O_0 + 2 b_1_1_2_O_0
   + 2.321928094887362 b_1_1_3_O_0 + 3 b_1_1_4_O_0
   + 3.321928094887362 b_1_1_5_O_0 + 4.321928094887363 b_1_1_6_O_0
   + 4.643856189774724 b_1_1_7_O_0 + 5.321928094887363 b_1_1_8_O_0
   + 5.643856189774724 b_1_1_9_O_0 + 6.643856189774724 b_1_1_10_O_0
   + 7.643856189774724 b_1_1_11_O_0 + b_1_2_1_O_0 + 2 b_1_2_2_O_0
   + 2.321928094887362 b_1_2_3_O_0 + 3 b_1_2_4_O_0
   + 3.321928094887362 b_1_2_5_O_0 + 4.321928094887363 b_1_2_6_O_0
   + 4.643856189774724 b_1_2_7_O_0 + 5.321928094887363 b_1_2_8_O_0
   + 5.643856189774724 b_1_2_9_O_0 + 6.643856189774724 b_1_2_10_O_0
   + 7.643856189774724 b_1_2_11_O_0 = 7.643856189774724
 [Op0]_LoopBoundBinaryConstraint_2_0: b_2_0_0_O_0 + b_2_0_1_O_0
   + b_2_0_2_O_0 + b_2_0_3_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_2_1: b_2_1_0_O_0 + b_2_1_1_O_0
   + b_2_1_2_O_0 + b_2_1_3_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_2_2: b_2_2_0_O_0 + b_2_2_1_O_0
   + b_2_2_2_O_0 + b_2_2_3_O_0 = 1
 [Op0]_LoopBoundMul_2_constraint: 1.584962500721156 b_2_0_1_O_0
   + 3.169925001442312 b_2_0_2_O_0 + 4.754887502163468 b_2_0_3_O_0
   + 1.584962500721156 b_2_1_1_O_0 + 3.169925001442312 b_2_1_2_O_0
   + 4.754887502163468 b_2_1_3_O_0 + 1.584962500721156 b_2_2_1_O_0
   + 3.169925001442312 b_2_2_2_O_0 + 4.754887502163468 b_2_2_3_O_0
   = 4.754887502163468
 [Op0]_LoopBoundBinaryConstraint_3_0: b_3_0_0_O_0 + b_3_0_1_O_0
   + b_3_0_2_O_0 + b_3_0_3_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_3_1: b_3_1_0_O_0 + b_3_1_1_O_0
   + b_3_1_2_O_0 + b_3_1_3_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_3_2: b_3_2_0_O_0 + b_3_2_1_O_0
   + b_3_2_2_O_0 + b_3_2_3_O_0 = 1
 [Op0]_LoopBoundMul_3_constraint: 1.584962500721156 b_3_0_1_O_0
   + 3.169925001442312 b_3_0_2_O_0 + 4.754887502163468 b_3_0_3_O_0
   + 1.584962500721156 b_3_1_1_O_0 + 3.169925001442312 b_3_1_2_O_0
   + 4.754887502163468 b_3_1_3_O_0 + 1.584962500721156 b_3_2_1_O_0
   + 3.169925001442312 b_3_2_2_O_0 + 4.754887502163468 b_3_2_3_O_0
   = 4.754887502163468
 [Op0]_LoopBoundBinaryConstraint_4_0: b_4_0_0_O_0 + b_4_0_1_O_0
   + b_4_0_2_O_0 + b_4_0_3_O_0 + b_4_0_4_O_0 + b_4_0_5_O_0 + b_4_0_6_O_0
   = 1
 [Op0]_LoopBoundBinaryConstraint_4_1: b_4_1_0_O_0 + b_4_1_1_O_0
   + b_4_1_2_O_0 + b_4_1_3_O_0 + b_4_1_4_O_0 + b_4_1_5_O_0 + b_4_1_6_O_0
   = 1
 [Op0]_LoopBoundBinaryConstraint_4_2: b_4_2_0_O_0 + b_4_2_1_O_0
   + b_4_2_2_O_0 + b_4_2_3_O_0 + b_4_2_4_O_0 + b_4_2_5_O_0 + b_4_2_6_O_0
   = 1
 [Op0]_LoopBoundMul_4_constraint: b_4_0_1_O_0 + 2 b_4_0_2_O_0
   + 3 b_4_0_3_O_0 + 4 b_4_0_4_O_0 + 5 b_4_0_5_O_0 + 6 b_4_0_6_O_0
   + b_4_1_1_O_0 + 2 b_4_1_2_O_0 + 3 b_4_1_3_O_0 + 4 b_4_1_4_O_0
   + 5 b_4_1_5_O_0 + 6 b_4_1_6_O_0 + b_4_2_1_O_0 + 2 b_4_2_2_O_0
   + 3 b_4_2_3_O_0 + 4 b_4_2_4_O_0 + 5 b_4_2_5_O_0 + 6 b_4_2_6_O_0 = 6
 [Op0]_LoopBoundBinaryConstraint_5_0: b_5_0_0_O_0 + b_5_0_1_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_5_1: b_5_1_0_O_0 + b_5_1_1_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_5_2: b_5_2_0_O_0 + b_5_2_1_O_0 = 1
 [Op0]_LoopBoundMul_5_constraint: 2.321928094887362 b_5_0_1_O_0
   + 2.321928094887362 b_5_1_1_O_0 + 2.321928094887362 b_5_2_1_O_0
   = 2.321928094887362
 [Op0]_LoopBoundBinaryConstraint_6_0: b_6_0_0_O_0 + b_6_0_1_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_6_1: b_6_1_0_O_0 + b_6_1_1_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_6_2: b_6_2_0_O_0 + b_6_2_1_O_0 = 1
 [Op0]_LoopBoundMul_6_constraint: 2.321928094887362 b_6_0_1_O_0
   + 2.321928094887362 b_6_1_1_O_0 + 2.321928094887362 b_6_2_1_O_0
   = 2.321928094887362
 [Op0]_TransCoeff_0_constraint: delta_0_0_O_0 + delta_0_1_O_0
   + delta_0_2_O_0 + delta_0_3_O_0 + delta_0_4_O_0 + delta_0_5_O_0 = 1
 [Op0]_TransCoeff_1_constraint: delta_1_0_O_0 + delta_1_1_O_0
   + delta_1_2_O_0 + delta_1_3_O_0 + delta_1_4_O_0 + delta_1_5_O_0 = 1
 [Op0]_TransCoeff_2_constraint: delta_2_0_O_0 + delta_2_1_O_0
   + delta_2_2_O_0 + delta_2_3_O_0 + delta_2_4_O_0 + delta_2_5_O_0 = 1
 [Op0]_TransCoeff_3_constraint: delta_3_0_O_0 + delta_3_1_O_0
   + delta_3_2_O_0 + delta_3_3_O_0 + delta_3_4_O_0 + delta_3_5_O_0 = 1
 num_PE_Constraint: num_PE_Sys_Var <= 32
 num_Col_Constraint: 16 num_Col_PE_Var <= 8192
 Col_Size_Constraint: num_Fil_Col_Var + num_in_col_Var <= 8192
 Coeff_Comb_0_Var_0_O_0_product_constraint: Coeff_0_0_0_O_0 + [
   - L_2_1_O_0 * L_2_2_O_0 ] = 0
 Coeff_0_Comb_0_O_0_Constraint: Coeff_0_Comb_0_O_0 + [
   - Coeff_0_0_0_O_0 * delta_0_0_O_0 ] = 0
 Coeff_0_Comb_1_O_0_Constraint: Coeff_0_Comb_1_O_0 + [
   - L_2_2_O_0 * delta_0_1_O_0 ] = 0
 Coeff_0_Comb_4_O_0_Constraint: Coeff_0_Comb_4_O_0 + [
   - Coeff_0_0_0_O_0 * delta_0_4_O_0 ] = 0
 Coeff_0_Comb_5_O_0_Constraint: Coeff_0_Comb_5_O_0 + [
   - L_2_1_O_0 * delta_0_5_O_0 ] = 0
 Coeff_Comb_0_Var_1_O_0_product_constraint: Coeff_1_0_0_O_0 + [
   - L_5_1_O_0 * L_5_2_O_0 ] = 0
 Coeff_1_Comb_0_O_0_Constraint: Coeff_1_Comb_0_O_0 + [
   - Coeff_1_0_0_O_0 * delta_1_0_O_0 ] = 0
 Coeff_1_Comb_1_O_0_Constraint: Coeff_1_Comb_1_O_0 + [
   - L_5_2_O_0 * delta_1_1_O_0 ] = 0
 Coeff_1_Comb_4_O_0_Constraint: Coeff_1_Comb_4_O_0 + [
   - Coeff_1_0_0_O_0 * delta_1_4_O_0 ] = 0
 Coeff_1_Comb_5_O_0_Constraint: Coeff_1_Comb_5_O_0 + [
   - L_5_1_O_0 * delta_1_5_O_0 ] = 0
 Coeff_Comb_0_Var_2_O_0_product_constraint: Coeff_2_0_0_O_0 + [
   - L_3_1_O_0 * L_3_2_O_0 ] = 0
 Coeff_2_Comb_0_O_0_Constraint: Coeff_2_Comb_0_O_0 + [
   - Coeff_2_0_0_O_0 * delta_2_0_O_0 ] = 0
 Coeff_2_Comb_1_O_0_Constraint: Coeff_2_Comb_1_O_0 + [
   - L_3_2_O_0 * delta_2_1_O_0 ] = 0
 Coeff_2_Comb_4_O_0_Constraint: Coeff_2_Comb_4_O_0 + [
   - Coeff_2_0_0_O_0 * delta_2_4_O_0 ] = 0
 Coeff_2_Comb_5_O_0_Constraint: Coeff_2_Comb_5_O_0 + [
   - L_3_1_O_0 * delta_2_5_O_0 ] = 0
 Coeff_Comb_0_Var_3_O_0_product_constraint: Coeff_3_0_0_O_0 + [
   - L_6_1_O_0 * L_6_2_O_0 ] = 0
 Coeff_3_Comb_0_O_0_Constraint: Coeff_3_Comb_0_O_0 + [
   - Coeff_3_0_0_O_0 * delta_3_0_O_0 ] = 0
 Coeff_3_Comb_1_O_0_Constraint: Coeff_3_Comb_1_O_0 + [
   - L_6_2_O_0 * delta_3_1_O_0 ] = 0
 Coeff_3_Comb_4_O_0_Constraint: Coeff_3_Comb_4_O_0 + [
   - Coeff_3_0_0_O_0 * delta_3_4_O_0 ] = 0
 Coeff_3_Comb_5_O_0_Constraint: Coeff_3_Comb_5_O_0 + [
   - L_6_1_O_0 * delta_3_5_O_0 ] = 0
 [Op_0]_tmpNum_Mul_Col_Var_0_constraint: [Op_0]_tmpNum_Mul_Col_Var_0 + [
   - L_0_0_O_0 * L_1_0_O_0 ] = 0
 [Op_0]_tmpNum_Mul_Col_Var_1_constraint: [Op_0]_tmpNum_Mul_Col_Var_1 + [
   - L_2_0_O_0 * [Op_0]_tmpNum_Mul_Col_Var_0 ] = 0
 [Op_0]_tmpNum_Mul_Col_Var_2_constraint: [Op_0]_tmpNum_Mul_Col_Var_2 + [
   - L_3_0_O_0 * [Op_0]_tmpNum_Mul_Col_Var_1 ] = 0
 [Op_0]_tmpNum_Mul_Col_Var_3_constraint: [Op_0]_tmpNum_Mul_Col_Var_3 + [
   - L_4_0_O_0 * [Op_0]_tmpNum_Mul_Col_Var_2 ] = 0
 [Op_0]_tmpNum_Mul_Col_Var_4_constraint: [Op_0]_tmpNum_Mul_Col_Var_4 + [
   - L_5_0_O_0 * [Op_0]_tmpNum_Mul_Col_Var_3 ] = 0
 [Op_0]_num_Mul_Col_Var_cons: num_Mul_Col_Var + [
   - L_6_0_O_0 * [Op_0]_tmpNum_Mul_Col_Var_4 ] = 0
 [Op_0]_num_Col_PE_Var_0_constraint: [Op_0]_num_Col_PE_Var_0 + [
   - L_0_1_O_0 * L_1_1_O_0 ] = 0
 [Op_0]_num_Col_PE_Var_1_constraint: [Op_0]_num_Col_PE_Var_1 + [
   - L_2_1_O_0 * [Op_0]_num_Col_PE_Var_0 ] = 0
 [Op_0]_num_Col_PE_Var_2_constraint: [Op_0]_num_Col_PE_Var_2 + [
   - L_3_1_O_0 * [Op_0]_num_Col_PE_Var_1 ] = 0
 [Op_0]_num_Col_PE_Var_3_constraint: [Op_0]_num_Col_PE_Var_3 + [
   - L_4_1_O_0 * [Op_0]_num_Col_PE_Var_2 ] = 0
 [Op_0]_num_Col_PE_Var_4_constraint: [Op_0]_num_Col_PE_Var_4 + [
   - L_5_1_O_0 * [Op_0]_num_Col_PE_Var_3 ] = 0
 [Op_0]_num_Col_PE_Var_cons: num_Col_PE_Var + [
   - L_6_1_O_0 * [Op_0]_num_Col_PE_Var_4 ] = 0
 [Op_0]_num_PE_Sys_Var_0_constraint: [Op_0]_num_PE_Sys_Var_0 + [
   - L_0_2_O_0 * L_1_2_O_0 ] = 0
 [Op_0]_num_PE_Sys_Var_1_constraint: [Op_0]_num_PE_Sys_Var_1 + [
   - L_2_2_O_0 * [Op_0]_num_PE_Sys_Var_0 ] = 0
 [Op_0]_num_PE_Sys_Var_2_constraint: [Op_0]_num_PE_Sys_Var_2 + [
   - L_3_2_O_0 * [Op_0]_num_PE_Sys_Var_1 ] = 0
 [Op_0]_num_PE_Sys_Var_3_constraint: [Op_0]_num_PE_Sys_Var_3 + [
   - L_4_2_O_0 * [Op_0]_num_PE_Sys_Var_2 ] = 0
 [Op_0]_num_PE_Sys_Var_4_constraint: [Op_0]_num_PE_Sys_Var_4 + [
   - L_5_2_O_0 * [Op_0]_num_PE_Sys_Var_3 ] = 0
 [Op_0]_num_PE_Sys_Var_cons: num_PE_Sys_Var + [
   - L_6_2_O_0 * [Op_0]_num_PE_Sys_Var_4 ] = 0
 [Op_0]_num_Out_Col_Var_0_constraint: [Op_0]_num_Out_Col_Var_0 + [
   - L_0_0_O_0 * L_2_0_O_0 ] = 0
 [Op_0]_num_Out_Col_Var_1_constraint: [Op_0]_num_Out_Col_Var_1 + [
   - L_3_0_O_0 * [Op_0]_num_Out_Col_Var_0 ] = 0
 [Op_0]_num_Out_Col_Var_constraint: num_Out_Col_Var + [
   - L_1_0_O_0 * [Op_0]_num_Out_Col_Var_1 ] = 0
 [Op_0]_num_Fil_Col_Var_0_constraint: [Op_0]_num_Fil_Col_Var_0 + [
   - L_1_0_O_0 * L_5_0_O_0 ] = 0
 [Op_0]_num_Fil_Col_Var_1_constraint: [Op_0]_num_Fil_Col_Var_1 + [
   - L_6_0_O_0 * [Op_0]_num_Fil_Col_Var_0 ] = 0
 [Op_0]_num_Fil_Col_Var_constraint: num_Fil_Col_Var + [
   - L_4_0_O_0 * [Op_0]_num_Fil_Col_Var_1 ] = 0
 [Op_0]_num_red_out_col_Var_0_constraint: [Op_0]_num_red_out_col_Var_0 + [
   - L_5_0_O_0 * L_6_0_O_0 ] = 0
 [Op_0]_num_red_out_col_Var_constraint: num_red_out_col_Var + [
   - L_4_0_O_0 * [Op_0]_num_red_out_col_Var_0 ] = -1
 [Op_0]_num_input_Col_Term2_Term2_constraint:
   [Op_0]_num_input_Col_Term2_Term2 + [ - L_2_0_O_0 * L_5_0_O_0 ] = 0
 qc47: C_0_0_O_0 + tmp_maxP_C_value_var + [ - L_2_0_O_0 * C_0_0_O_0 ] = 0
 qc48: C_1_0_O_0 + tmp_maxR_C_value_var + [ - L_5_0_O_0 * C_1_0_O_0 ] = 0
 qc49: [Op_0]_num_input_Col_Term2_Term1 + [
   - PR_Sel_GCD_Value * [Op_0]_num_input_Col_Term2_Term1_partial ] = 1
 [Op_0]_num_input_Col_Term3_Term2_constraint:
   [Op_0]_num_input_Col_Term3_Term2 + [ - L_3_0_O_0 * L_6_0_O_0 ] = 0
 qc51: C_2_0_O_0 + tmp_maxQ_C_value_var + [ - L_3_0_O_0 * C_2_0_O_0 ] = 0
 qc52: C_3_0_O_0 + tmp_maxS_C_value_var + [ - L_6_0_O_0 * C_3_0_O_0 ] = 0
 qc53: [Op_0]_num_input_Col_Term3_Term1 + [
   - QS_Sel_GCD_Value * [Op_0]_num_input_Col_Term3_Term1_partial ] = 1
 qc54: [Op_0]_num_inputs_col_tmp_mul0 + [
   - L_0_0_O_0 * [Op_0]_num_inputs_col_term2 ] = 0
 qc55: [Op_0]_num_inputs_col_tmp_mul1 + [
   - [Op_0]_num_inputs_col_term3 * [Op_0]_num_inputs_col_tmp_mul0 ] = 0
 num_inputs_col_constraint: num_in_col_Var + [
   - L_4_0_O_0 * [Op_0]_num_inputs_col_tmp_mul1 ] = 0
 num_Red_Col_Var_constraint: num_Red_Col_Var + [
   - num_Out_Col_Var * num_red_out_col_Var ] = 0
 num_Out_PE_Var_constraint: num_Out_PE_Var + [
   - num_Col_PE_Var * num_Out_Col_Var ] = 0
 num_Out_Sys_Var_constraint: num_Out_Sys_Var + [
   - num_PE_Sys_Var * num_Out_Col_Var ] = 0
 Out_Cost_Sys_Var_constraint: - 16 num_Out_Sys_Var + [
   channel_Bandwidth_Var * Out_Cost_Sys_Var ] = 0
 num_In_PE_Var_constraint: num_In_PE_Var + [
   - num_Col_PE_Var * num_in_col_Var ] = 0
 num_In_Sys_Var_constraint: num_In_Sys_Var + [
   - num_PE_Sys_Var * num_In_PE_Var ] = 0
 tmp_In_Cost_Sys_Var_constraint: - 16 num_In_Sys_Var + [
   channel_Bandwidth_Var * tmp_In_Cost_Sys_Var ] = 0
 num_Fil_Loading_Var_constraint: num_Fil_Loading_Var + [
   - 0.0625 num_Mul_Col_Var * num_Col_PE_Var ] = 0
Bounds
 L_0_0_O_0 = 1
 L_0_1_O_0 = 1
 L_0_2_O_0 = 1
 1 <= L_1_0_O_0 <= 200
 1 <= L_1_1_O_0 <= 200
 1 <= L_1_2_O_0 <= 200
 1 <= L_2_0_O_0 <= 27
 1 <= L_2_1_O_0 <= 27
 1 <= L_2_2_O_0 <= 27
 1 <= L_3_0_O_0 <= 27
 1 <= L_3_1_O_0 <= 27
 1 <= L_3_2_O_0 <= 27
 1 <= L_4_0_O_0 <= 64
 1 <= L_4_1_O_0 <= 64
 1 <= L_4_2_O_0 <= 64
 1 <= L_5_0_O_0 <= 5
 1 <= L_5_1_O_0 <= 5
 1 <= L_5_2_O_0 <= 5
 1 <= L_6_0_O_0 <= 5
 1 <= L_6_1_O_0 <= 5
 1 <= L_6_2_O_0 <= 5
 1 <= Coeff_0_0_0_O_0 <= 27
 Coeff_0_Comb_0_O_0 <= 27
 Coeff_0_Comb_1_O_0 <= 27
 Coeff_0_Comb_4_O_0 <= 27
 Coeff_0_Comb_5_O_0 <= 27
 C_0_0_O_0 <= 27
 1 <= Coeff_1_0_0_O_0 <= 5
 Coeff_1_Comb_0_O_0 <= 5
 Coeff_1_Comb_1_O_0 <= 5
 Coeff_1_Comb_4_O_0 <= 5
 Coeff_1_Comb_5_O_0 <= 5
 C_1_0_O_0 <= 5
 1 <= Coeff_2_0_0_O_0 <= 27
 Coeff_2_Comb_0_O_0 <= 27
 Coeff_2_Comb_1_O_0 <= 27
 Coeff_2_Comb_4_O_0 <= 27
 Coeff_2_Comb_5_O_0 <= 27
 C_2_0_O_0 <= 27
 1 <= Coeff_3_0_0_O_0 <= 5
 Coeff_3_Comb_0_O_0 <= 5
 Coeff_3_Comb_1_O_0 <= 5
 Coeff_3_Comb_4_O_0 <= 5
 Coeff_3_Comb_5_O_0 <= 5
 C_3_0_O_0 <= 5
 1 <= num_Mul_Col_Var <= 2.3328e+08
 1 <= [Op_0]_tmpNum_Mul_Col_Var_0 <= 200
 1 <= [Op_0]_tmpNum_Mul_Col_Var_1 <= 5400
 1 <= [Op_0]_tmpNum_Mul_Col_Var_2 <= 145800
 1 <= [Op_0]_tmpNum_Mul_Col_Var_3 <= 9.3312e+06
 1 <= [Op_0]_tmpNum_Mul_Col_Var_4 <= 4.6656e+07
 1 <= num_Col_PE_Var <= 2.3328e+08
 1 <= [Op_0]_num_Col_PE_Var_0 <= 200
 1 <= [Op_0]_num_Col_PE_Var_1 <= 5400
 1 <= [Op_0]_num_Col_PE_Var_2 <= 145800
 1 <= [Op_0]_num_Col_PE_Var_3 <= 9.3312e+06
 1 <= [Op_0]_num_Col_PE_Var_4 <= 4.6656e+07
 1 <= num_PE_Sys_Var <= 2.3328e+08
 1 <= [Op_0]_num_PE_Sys_Var_0 <= 200
 1 <= [Op_0]_num_PE_Sys_Var_1 <= 5400
 1 <= [Op_0]_num_PE_Sys_Var_2 <= 145800
 1 <= [Op_0]_num_PE_Sys_Var_3 <= 9.3312e+06
 1 <= [Op_0]_num_PE_Sys_Var_4 <= 4.6656e+07
 1 <= num_Channels_Sys_Var <= 2.3328e+08
 1 <= channel_Bandwidth_Var <= 2.3328e+08
 1 <= num_Out_Col_Var <= 145800
 1 <= [Op_0]_num_Out_Col_Var_0 <= 27
 1 <= [Op_0]_num_Out_Col_Var_1 <= 729
 1 <= num_Fil_Col_Var <= 320000
 1 <= [Op_0]_num_Fil_Col_Var_0 <= 1000
 1 <= [Op_0]_num_Fil_Col_Var_1 <= 5000
 num_red_out_col_Var <= 1600
 1 <= [Op_0]_num_red_out_col_Var_0 <= 25
 1 <= num_in_col_Var <= 1.1664e+06
 PR_Sel_GCD_Value <= 1
 QS_Sel_GCD_Value <= 1
 1 <= [Op_0]_num_input_Col_Term2_Term2 <= 135
 tmp_maxP_C_value_var <= 540
 tmp_maxR_C_value_var <= 405
 1 <= [Op_0]_num_input_Col_Term2_Term1_partial <= 270
 1 <= [Op_0]_num_input_Col_Term2_Term1 <= 270
 1 <= [Op_0]_num_inputs_col_term2 <= 136
 1 <= [Op_0]_num_input_Col_Term3_Term2 <= 135
 tmp_maxQ_C_value_var <= 136
 tmp_maxS_C_value_var <= 136
 1 <= [Op_0]_num_input_Col_Term3_Term1_partial <= 270
 1 <= [Op_0]_num_input_Col_Term3_Term1 <= 136
 1 <= [Op_0]_num_inputs_col_term3 <= 136
 1 <= [Op_0]_num_inputs_col_tmp_mul0 <= 1.1664e+06
 1 <= [Op_0]_num_inputs_col_tmp_mul1 <= 1.1664e+06
 num_Red_Col_Var <= 2.3328e+08
 1 <= num_Out_PE_Var <= 5.44195584e+16
 num_Out_Sys_Var <= 5.44195584e+16
 Out_Cost_Sys_Var <= 5.44195584e+16
 1 <= num_In_PE_Var <= 5.44195584e+16
 num_In_Sys_Var <= 5.44195584e+16
 tmp_In_Cost_Sys_Var <= 5.44195584e+16
 In_Cost_Sys_Var <= 5.44195584e+16
 num_Fil_Loading_Var <= 5.44195584e+16
Binaries
 b_0_0_0_O_0 b_0_1_0_O_0 b_0_2_0_O_0 b_1_0_0_O_0 b_1_0_1_O_0 b_1_0_2_O_0
 b_1_0_3_O_0 b_1_0_4_O_0 b_1_0_5_O_0 b_1_0_6_O_0 b_1_0_7_O_0 b_1_0_8_O_0
 b_1_0_9_O_0 b_1_0_10_O_0 b_1_0_11_O_0 b_1_1_0_O_0 b_1_1_1_O_0 b_1_1_2_O_0
 b_1_1_3_O_0 b_1_1_4_O_0 b_1_1_5_O_0 b_1_1_6_O_0 b_1_1_7_O_0 b_1_1_8_O_0
 b_1_1_9_O_0 b_1_1_10_O_0 b_1_1_11_O_0 b_1_2_0_O_0 b_1_2_1_O_0 b_1_2_2_O_0
 b_1_2_3_O_0 b_1_2_4_O_0 b_1_2_5_O_0 b_1_2_6_O_0 b_1_2_7_O_0 b_1_2_8_O_0
 b_1_2_9_O_0 b_1_2_10_O_0 b_1_2_11_O_0 b_2_0_0_O_0 b_2_0_1_O_0 b_2_0_2_O_0
 b_2_0_3_O_0 b_2_1_0_O_0 b_2_1_1_O_0 b_2_1_2_O_0 b_2_1_3_O_0 b_2_2_0_O_0
 b_2_2_1_O_0 b_2_2_2_O_0 b_2_2_3_O_0 b_3_0_0_O_0 b_3_0_1_O_0 b_3_0_2_O_0
 b_3_0_3_O_0 b_3_1_0_O_0 b_3_1_1_O_0 b_3_1_2_O_0 b_3_1_3_O_0 b_3_2_0_O_0
 b_3_2_1_O_0 b_3_2_2_O_0 b_3_2_3_O_0 b_4_0_0_O_0 b_4_0_1_O_0 b_4_0_2_O_0
 b_4_0_3_O_0 b_4_0_4_O_0 b_4_0_5_O_0 b_4_0_6_O_0 b_4_1_0_O_0 b_4_1_1_O_0
 b_4_1_2_O_0 b_4_1_3_O_0 b_4_1_4_O_0 b_4_1_5_O_0 b_4_1_6_O_0 b_4_2_0_O_0
 b_4_2_1_O_0 b_4_2_2_O_0 b_4_2_3_O_0 b_4_2_4_O_0 b_4_2_5_O_0 b_4_2_6_O_0
 b_5_0_0_O_0 b_5_0_1_O_0 b_5_1_0_O_0 b_5_1_1_O_0 b_5_2_0_O_0 b_5_2_1_O_0
 b_6_0_0_O_0 b_6_0_1_O_0 b_6_1_0_O_0 b_6_1_1_O_0 b_6_2_0_O_0 b_6_2_1_O_0
 delta_0_0_O_0 delta_0_1_O_0 delta_0_2_O_0 delta_0_3_O_0 delta_0_4_O_0
 delta_0_5_O_0 delta_1_0_O_0 delta_1_1_O_0 delta_1_2_O_0 delta_1_3_O_0
 delta_1_4_O_0 delta_1_5_O_0 delta_2_0_O_0 delta_2_1_O_0 delta_2_2_O_0
 delta_2_3_O_0 delta_2_4_O_0 delta_2_5_O_0 delta_3_0_O_0 delta_3_1_O_0
 delta_3_2_O_0 delta_3_3_O_0 delta_3_4_O_0 delta_3_5_O_0 P_R_LUT_Sel_0_O_0
 P_R_LUT_Sel_1_O_0 P_R_LUT_Sel_2_O_0 P_R_LUT_Sel_3_O_0 P_R_LUT_Sel_4_O_0
 P_R_LUT_Sel_5_O_0 P_R_LUT_Sel_6_O_0 P_R_LUT_Sel_7_O_0 Q_S_LUT_Sel_0_O_0
 Q_S_LUT_Sel_1_O_0 Q_S_LUT_Sel_2_O_0 Q_S_LUT_Sel_3_O_0 Q_S_LUT_Sel_4_O_0
 Q_S_LUT_Sel_5_O_0 Q_S_LUT_Sel_6_O_0 Q_S_LUT_Sel_7_O_0
Generals
 L_0_0_O_0 L_0_1_O_0 L_0_2_O_0 L_1_0_O_0 L_1_1_O_0 L_1_2_O_0 L_2_0_O_0
 L_2_1_O_0 L_2_2_O_0 L_3_0_O_0 L_3_1_O_0 L_3_2_O_0 L_4_0_O_0 L_4_1_O_0
 L_4_2_O_0 L_5_0_O_0 L_5_1_O_0 L_5_2_O_0 L_6_0_O_0 L_6_1_O_0 L_6_2_O_0
 Coeff_0_0_0_O_0 Coeff_0_Comb_0_O_0 Coeff_0_Comb_1_O_0 Coeff_0_Comb_4_O_0
 Coeff_0_Comb_5_O_0 C_0_0_O_0 Coeff_1_0_0_O_0 Coeff_1_Comb_0_O_0
 Coeff_1_Comb_1_O_0 Coeff_1_Comb_4_O_0 Coeff_1_Comb_5_O_0 C_1_0_O_0
 Coeff_2_0_0_O_0 Coeff_2_Comb_0_O_0 Coeff_2_Comb_1_O_0 Coeff_2_Comb_4_O_0
 Coeff_2_Comb_5_O_0 C_2_0_O_0 Coeff_3_0_0_O_0 Coeff_3_Comb_0_O_0
 Coeff_3_Comb_1_O_0 Coeff_3_Comb_4_O_0 Coeff_3_Comb_5_O_0 C_3_0_O_0
 num_Mul_Col_Var [Op_0]_tmpNum_Mul_Col_Var_0 [Op_0]_tmpNum_Mul_Col_Var_1
 [Op_0]_tmpNum_Mul_Col_Var_2 [Op_0]_tmpNum_Mul_Col_Var_3
 [Op_0]_tmpNum_Mul_Col_Var_4 num_Col_PE_Var [Op_0]_num_Col_PE_Var_0
 [Op_0]_num_Col_PE_Var_1 [Op_0]_num_Col_PE_Var_2 [Op_0]_num_Col_PE_Var_3
 [Op_0]_num_Col_PE_Var_4 num_PE_Sys_Var [Op_0]_num_PE_Sys_Var_0
 [Op_0]_num_PE_Sys_Var_1 [Op_0]_num_PE_Sys_Var_2 [Op_0]_num_PE_Sys_Var_3
 [Op_0]_num_PE_Sys_Var_4 num_Channels_Sys_Var channel_Bandwidth_Var
 num_Out_Col_Var [Op_0]_num_Out_Col_Var_0 [Op_0]_num_Out_Col_Var_1
 num_Fil_Col_Var [Op_0]_num_Fil_Col_Var_0 [Op_0]_num_Fil_Col_Var_1
 num_red_out_col_Var [Op_0]_num_red_out_col_Var_0 num_in_col_Var
 [Op_0]_num_input_Col_Term2_Term2 tmp_maxP_C_value_var tmp_maxR_C_value_var
 [Op_0]_num_input_Col_Term2_Term1_partial [Op_0]_num_input_Col_Term2_Term1
 [Op_0]_num_inputs_col_term2 [Op_0]_num_input_Col_Term3_Term2
 tmp_maxQ_C_value_var tmp_maxS_C_value_var
 [Op_0]_num_input_Col_Term3_Term1_partial [Op_0]_num_input_Col_Term3_Term1
 [Op_0]_num_inputs_col_term3 [Op_0]_num_inputs_col_tmp_mul0
 [Op_0]_num_inputs_col_tmp_mul1 num_Red_Col_Var num_Out_PE_Var
 num_In_PE_Var
General Constraints
 GC0: [Op_0]_num_inputs_col_term2 = MIN (
   [Op_0]_num_input_Col_Term2_Term1 , [Op_0]_num_input_Col_Term2_Term2 )
 GC1: [Op_0]_num_inputs_col_term3 = MIN (
   [Op_0]_num_input_Col_Term3_Term1 , [Op_0]_num_input_Col_Term3_Term2 )
End
