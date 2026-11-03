\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0x887abba6d39cac70
Minimize
  15 num_Fil_Col_Var + Out_Cost_Sys_Var + In_Cost_Sys_Var
   + num_Fil_Loading_Var
Subject To
 Integer_Loop_Bound_Var_Cons_L_0_0_O_0: - b_0_0_0_O_0 + L_0_0_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_0_1_O_0: - b_0_1_0_O_0 + L_0_1_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_0_2_O_0: - b_0_2_0_O_0 + L_0_2_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_1_0_O_0: - b_1_0_0_O_0 + L_1_0_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_1_1_O_0: - b_1_1_0_O_0 + L_1_1_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_1_2_O_0: - b_1_2_0_O_0 + L_1_2_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_2_0_O_0: - b_2_0_0_O_0 + L_2_0_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_2_1_O_0: - b_2_1_0_O_0 + L_2_1_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_2_2_O_0: - b_2_2_0_O_0 + L_2_2_O_0 = 0
 Integer_Loop_Bound_Var_Cons_L_3_0_O_0: - b_3_0_0_O_0 - 3 b_3_0_1_O_0
   - 7 b_3_0_2_O_0 - 9 b_3_0_3_O_0 - 21 b_3_0_4_O_0 - 27 b_3_0_5_O_0
   - 49 b_3_0_6_O_0 - 63 b_3_0_7_O_0 - 147 b_3_0_8_O_0 - 189 b_3_0_9_O_0
   - 343 b_3_0_10_O_0 - 441 b_3_0_11_O_0 - 1029 b_3_0_12_O_0
   - 1323 b_3_0_13_O_0 - 3087 b_3_0_14_O_0 - 9261 b_3_0_15_O_0 + L_3_0_O_0
   = 0
 Integer_Loop_Bound_Var_Cons_L_3_1_O_0: - b_3_1_0_O_0 - 3 b_3_1_1_O_0
   - 7 b_3_1_2_O_0 - 9 b_3_1_3_O_0 - 21 b_3_1_4_O_0 - 27 b_3_1_5_O_0
   - 49 b_3_1_6_O_0 - 63 b_3_1_7_O_0 - 147 b_3_1_8_O_0 - 189 b_3_1_9_O_0
   - 343 b_3_1_10_O_0 - 441 b_3_1_11_O_0 - 1029 b_3_1_12_O_0
   - 1323 b_3_1_13_O_0 - 3087 b_3_1_14_O_0 - 9261 b_3_1_15_O_0 + L_3_1_O_0
   = 0
 Integer_Loop_Bound_Var_Cons_L_3_2_O_0: - b_3_2_0_O_0 - 3 b_3_2_1_O_0
   - 7 b_3_2_2_O_0 - 9 b_3_2_3_O_0 - 21 b_3_2_4_O_0 - 27 b_3_2_5_O_0
   - 49 b_3_2_6_O_0 - 63 b_3_2_7_O_0 - 147 b_3_2_8_O_0 - 189 b_3_2_9_O_0
   - 343 b_3_2_10_O_0 - 441 b_3_2_11_O_0 - 1029 b_3_2_12_O_0
   - 1323 b_3_2_13_O_0 - 3087 b_3_2_14_O_0 - 9261 b_3_2_15_O_0 + L_3_2_O_0
   = 0
 Integer_Loop_Bound_Var_Cons_L_4_0_O_0: - b_4_0_0_O_0 - 2 b_4_0_1_O_0
   - 4 b_4_0_2_O_0 - 8 b_4_0_3_O_0 - 16 b_4_0_4_O_0 - 32 b_4_0_5_O_0
   - 64 b_4_0_6_O_0 - 128 b_4_0_7_O_0 - 256 b_4_0_8_O_0 - 512 b_4_0_9_O_0
   - 1024 b_4_0_10_O_0 - 2048 b_4_0_11_O_0 - 4096 b_4_0_12_O_0 + L_4_0_O_0
   = 0
 Integer_Loop_Bound_Var_Cons_L_4_1_O_0: - b_4_1_0_O_0 - 2 b_4_1_1_O_0
   - 4 b_4_1_2_O_0 - 8 b_4_1_3_O_0 - 16 b_4_1_4_O_0 - 32 b_4_1_5_O_0
   - 64 b_4_1_6_O_0 - 128 b_4_1_7_O_0 - 256 b_4_1_8_O_0 - 512 b_4_1_9_O_0
   - 1024 b_4_1_10_O_0 - 2048 b_4_1_11_O_0 - 4096 b_4_1_12_O_0 + L_4_1_O_0
   = 0
 Integer_Loop_Bound_Var_Cons_L_4_2_O_0: - b_4_2_0_O_0 - 2 b_4_2_1_O_0
   - 4 b_4_2_2_O_0 - 8 b_4_2_3_O_0 - 16 b_4_2_4_O_0 - 32 b_4_2_5_O_0
   - 64 b_4_2_6_O_0 - 128 b_4_2_7_O_0 - 256 b_4_2_8_O_0 - 512 b_4_2_9_O_0
   - 1024 b_4_2_10_O_0 - 2048 b_4_2_11_O_0 - 4096 b_4_2_12_O_0 + L_4_2_O_0
   = 0
 [Op]_numChan_lower: num_PE_Sys_Var - 16 num_Channels_Sys_Var >= -15
 [Op]_numChan_upper: num_PE_Sys_Var - 16 num_Channels_Sys_Var <= 0
 [Op_0]_channel_Bandwidth_Var_constraint: - 256 num_Channels_Sys_Var
   + channel_Bandwidth_Var = 0
 [Op_0]_num_red_out_col_Var_constraint: - L_3_0_O_0 + num_red_out_col_Var
   = -1
 [Op0]_LoopBoundBinaryConstraint_0_0: b_0_0_0_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_0_1: b_0_1_0_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_0_2: b_0_2_0_O_0 = 1
 [Op0]_LoopBoundMul_0_constraint: = 0
 [Op0]_LoopBoundBinaryConstraint_1_0: b_1_0_0_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_1_1: b_1_1_0_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_1_2: b_1_2_0_O_0 = 1
 [Op0]_LoopBoundMul_1_constraint: = 0
 [Op0]_LoopBoundBinaryConstraint_2_0: b_2_0_0_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_2_1: b_2_1_0_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_2_2: b_2_2_0_O_0 = 1
 [Op0]_LoopBoundMul_2_constraint: = 0
 [Op0]_LoopBoundBinaryConstraint_3_0: b_3_0_0_O_0 + b_3_0_1_O_0
   + b_3_0_2_O_0 + b_3_0_3_O_0 + b_3_0_4_O_0 + b_3_0_5_O_0 + b_3_0_6_O_0
   + b_3_0_7_O_0 + b_3_0_8_O_0 + b_3_0_9_O_0 + b_3_0_10_O_0 + b_3_0_11_O_0
   + b_3_0_12_O_0 + b_3_0_13_O_0 + b_3_0_14_O_0 + b_3_0_15_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_3_1: b_3_1_0_O_0 + b_3_1_1_O_0
   + b_3_1_2_O_0 + b_3_1_3_O_0 + b_3_1_4_O_0 + b_3_1_5_O_0 + b_3_1_6_O_0
   + b_3_1_7_O_0 + b_3_1_8_O_0 + b_3_1_9_O_0 + b_3_1_10_O_0 + b_3_1_11_O_0
   + b_3_1_12_O_0 + b_3_1_13_O_0 + b_3_1_14_O_0 + b_3_1_15_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_3_2: b_3_2_0_O_0 + b_3_2_1_O_0
   + b_3_2_2_O_0 + b_3_2_3_O_0 + b_3_2_4_O_0 + b_3_2_5_O_0 + b_3_2_6_O_0
   + b_3_2_7_O_0 + b_3_2_8_O_0 + b_3_2_9_O_0 + b_3_2_10_O_0 + b_3_2_11_O_0
   + b_3_2_12_O_0 + b_3_2_13_O_0 + b_3_2_14_O_0 + b_3_2_15_O_0 = 1
 [Op0]_LoopBoundMul_3_constraint: 1.584962500721156 b_3_0_1_O_0
   + 2.807354922057604 b_3_0_2_O_0 + 3.169925001442312 b_3_0_3_O_0
   + 4.392317422778761 b_3_0_4_O_0 + 4.754887502163468 b_3_0_5_O_0
   + 5.614709844115208 b_3_0_6_O_0 + 5.977279923499917 b_3_0_7_O_0
   + 7.199672344836364 b_3_0_8_O_0 + 7.562242424221073 b_3_0_9_O_0
   + 8.422064766172813 b_3_0_10_O_0 + 8.784634845557521 b_3_0_11_O_0
   + 10.00702726689397 b_3_0_12_O_0 + 10.36959734627868 b_3_0_13_O_0
   + 11.59198976761513 b_3_0_14_O_0 + 13.17695226833628 b_3_0_15_O_0
   + 1.584962500721156 b_3_1_1_O_0 + 2.807354922057604 b_3_1_2_O_0
   + 3.169925001442312 b_3_1_3_O_0 + 4.392317422778761 b_3_1_4_O_0
   + 4.754887502163468 b_3_1_5_O_0 + 5.614709844115208 b_3_1_6_O_0
   + 5.977279923499917 b_3_1_7_O_0 + 7.199672344836364 b_3_1_8_O_0
   + 7.562242424221073 b_3_1_9_O_0 + 8.422064766172813 b_3_1_10_O_0
   + 8.784634845557521 b_3_1_11_O_0 + 10.00702726689397 b_3_1_12_O_0
   + 10.36959734627868 b_3_1_13_O_0 + 11.59198976761513 b_3_1_14_O_0
   + 13.17695226833628 b_3_1_15_O_0 + 1.584962500721156 b_3_2_1_O_0
   + 2.807354922057604 b_3_2_2_O_0 + 3.169925001442312 b_3_2_3_O_0
   + 4.392317422778761 b_3_2_4_O_0 + 4.754887502163468 b_3_2_5_O_0
   + 5.614709844115208 b_3_2_6_O_0 + 5.977279923499917 b_3_2_7_O_0
   + 7.199672344836364 b_3_2_8_O_0 + 7.562242424221073 b_3_2_9_O_0
   + 8.422064766172813 b_3_2_10_O_0 + 8.784634845557521 b_3_2_11_O_0
   + 10.00702726689397 b_3_2_12_O_0 + 10.36959734627868 b_3_2_13_O_0
   + 11.59198976761513 b_3_2_14_O_0 + 13.17695226833628 b_3_2_15_O_0
   = 13.17695226833628
 [Op0]_LoopBoundBinaryConstraint_4_0: b_4_0_0_O_0 + b_4_0_1_O_0
   + b_4_0_2_O_0 + b_4_0_3_O_0 + b_4_0_4_O_0 + b_4_0_5_O_0 + b_4_0_6_O_0
   + b_4_0_7_O_0 + b_4_0_8_O_0 + b_4_0_9_O_0 + b_4_0_10_O_0 + b_4_0_11_O_0
   + b_4_0_12_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_4_1: b_4_1_0_O_0 + b_4_1_1_O_0
   + b_4_1_2_O_0 + b_4_1_3_O_0 + b_4_1_4_O_0 + b_4_1_5_O_0 + b_4_1_6_O_0
   + b_4_1_7_O_0 + b_4_1_8_O_0 + b_4_1_9_O_0 + b_4_1_10_O_0 + b_4_1_11_O_0
   + b_4_1_12_O_0 = 1
 [Op0]_LoopBoundBinaryConstraint_4_2: b_4_2_0_O_0 + b_4_2_1_O_0
   + b_4_2_2_O_0 + b_4_2_3_O_0 + b_4_2_4_O_0 + b_4_2_5_O_0 + b_4_2_6_O_0
   + b_4_2_7_O_0 + b_4_2_8_O_0 + b_4_2_9_O_0 + b_4_2_10_O_0 + b_4_2_11_O_0
   + b_4_2_12_O_0 = 1
 [Op0]_LoopBoundMul_4_constraint: b_4_0_1_O_0 + 2 b_4_0_2_O_0
   + 3 b_4_0_3_O_0 + 4 b_4_0_4_O_0 + 5 b_4_0_5_O_0 + 6 b_4_0_6_O_0
   + 7 b_4_0_7_O_0 + 8 b_4_0_8_O_0 + 9 b_4_0_9_O_0 + 10 b_4_0_10_O_0
   + 11 b_4_0_11_O_0 + 12 b_4_0_12_O_0 + b_4_1_1_O_0 + 2 b_4_1_2_O_0
   + 3 b_4_1_3_O_0 + 4 b_4_1_4_O_0 + 5 b_4_1_5_O_0 + 6 b_4_1_6_O_0
   + 7 b_4_1_7_O_0 + 8 b_4_1_8_O_0 + 9 b_4_1_9_O_0 + 10 b_4_1_10_O_0
   + 11 b_4_1_11_O_0 + 12 b_4_1_12_O_0 + b_4_2_1_O_0 + 2 b_4_2_2_O_0
   + 3 b_4_2_3_O_0 + 4 b_4_2_4_O_0 + 5 b_4_2_5_O_0 + 6 b_4_2_6_O_0
   + 7 b_4_2_7_O_0 + 8 b_4_2_8_O_0 + 9 b_4_2_9_O_0 + 10 b_4_2_10_O_0
   + 11 b_4_2_11_O_0 + 12 b_4_2_12_O_0 = 12
 num_PE_Constraint: num_PE_Sys_Var <= 32
 num_Col_Constraint: 16 num_Col_PE_Var <= 8192
 Col_Size_Constraint: num_Fil_Col_Var + num_In_Col_Var <= 8192
 [Op_0]_tmpNum_Mul_Col_Var_0_constraint: [Op_0]_tmpNum_Mul_Col_Var_0 + [
   - L_0_0_O_0 * L_1_0_O_0 ] = 0
 [Op_0]_tmpNum_Mul_Col_Var_1_constraint: [Op_0]_tmpNum_Mul_Col_Var_1 + [
   - L_2_0_O_0 * [Op_0]_tmpNum_Mul_Col_Var_0 ] = 0
 [Op_0]_tmpNum_Mul_Col_Var_2_constraint: [Op_0]_tmpNum_Mul_Col_Var_2 + [
   - L_3_0_O_0 * [Op_0]_tmpNum_Mul_Col_Var_1 ] = 0
 [Op_0]_num_Mul_Col_Var_cons: num_Mul_Col_Var + [
   - L_4_0_O_0 * [Op_0]_tmpNum_Mul_Col_Var_2 ] = 0
 [Op_0]_num_Col_PE_Var_0_constraint: [Op_0]_num_Col_PE_Var_0 + [
   - L_0_1_O_0 * L_1_1_O_0 ] = 0
 [Op_0]_num_Col_PE_Var_1_constraint: [Op_0]_num_Col_PE_Var_1 + [
   - L_2_1_O_0 * [Op_0]_num_Col_PE_Var_0 ] = 0
 [Op_0]_num_Col_PE_Var_2_constraint: [Op_0]_num_Col_PE_Var_2 + [
   - L_3_1_O_0 * [Op_0]_num_Col_PE_Var_1 ] = 0
 [Op_0]_num_Col_PE_Var_cons: num_Col_PE_Var + [
   - L_4_1_O_0 * [Op_0]_num_Col_PE_Var_2 ] = 0
 [Op_0]_num_PE_Sys_Var_0_constraint: [Op_0]_num_PE_Sys_Var_0 + [
   - L_0_2_O_0 * L_1_2_O_0 ] = 0
 [Op_0]_num_PE_Sys_Var_1_constraint: [Op_0]_num_PE_Sys_Var_1 + [
   - L_2_2_O_0 * [Op_0]_num_PE_Sys_Var_0 ] = 0
 [Op_0]_num_PE_Sys_Var_2_constraint: [Op_0]_num_PE_Sys_Var_2 + [
   - L_3_2_O_0 * [Op_0]_num_PE_Sys_Var_1 ] = 0
 [Op_0]_num_PE_Sys_Var_cons: num_PE_Sys_Var + [
   - L_4_2_O_0 * [Op_0]_num_PE_Sys_Var_2 ] = 0
 [Op_0]_num_Out_Col_Var_0_constraint: [Op_0]_num_Out_Col_Var_0 + [
   - L_2_0_O_0 * L_4_0_O_0 ] = 0
 [Op_0]_num_Out_Col_Var_constraint: num_Out_Col_Var + [
   - L_0_0_O_0 * [Op_0]_num_Out_Col_Var_0 ] = 0
 [Op_0]_num_Fil_Col_Var_0_constraint: [Op_0]_num_Fil_Col_Var_0 + [
   - L_3_0_O_0 * L_4_0_O_0 ] = 0
 [Op_0]_num_Fil_Col_Var_constraint: num_Fil_Col_Var + [
   - L_0_0_O_0 * [Op_0]_num_Fil_Col_Var_0 ] = 0
 [Op_0]_num_In_Col_Var_0_constraint: [Op_0]_num_In_Col_Var_0 + [
   - L_2_0_O_0 * L_3_0_O_0 ] = 0
 [Op_0]_num_In_Col_Var_constraint: num_In_Col_Var + [
   - L_0_0_O_0 * [Op_0]_num_In_Col_Var_0 ] = 0
 num_Red_Col_Var_constraint: num_Red_Col_Var + [
   - num_Out_Col_Var * num_red_out_col_Var ] = 0
 num_Out_PE_Var_constraint: num_Out_PE_Var + [
   - num_Col_PE_Var * num_Out_Col_Var ] = 0
 num_Out_Sys_Var_constraint: num_Out_Sys_Var + [
   - num_PE_Sys_Var * num_Out_Col_Var ] = 0
 Out_Cost_Sys_Var_constraint: - 16 num_Out_Sys_Var + [
   channel_Bandwidth_Var * Out_Cost_Sys_Var ] = 0
 num_In_PE_Var_constraint: num_In_PE_Var + [
   - num_Col_PE_Var * num_In_Col_Var ] = 0
 num_In_Sys_Var_constraint: num_In_Sys_Var + [
   - 0.0625 num_PE_Sys_Var * num_In_PE_Var ] = 0
 tmp_In_Cost_Sys_Var_constraint: - 16 num_In_Sys_Var + [
   channel_Bandwidth_Var * In_Cost_Sys_Var ] = 0
 num_Fil_Loading_Var_constraint: num_Fil_Loading_Var + [
   - 0.0625 num_Col_PE_Var * num_Fil_Col_Var ] = 0
Bounds
 L_0_0_O_0 = 1
 L_0_1_O_0 = 1
 L_0_2_O_0 = 1
 L_1_0_O_0 = 1
 L_1_1_O_0 = 1
 L_1_2_O_0 = 1
 L_2_0_O_0 = 1
 L_2_1_O_0 = 1
 L_2_2_O_0 = 1
 1 <= L_3_0_O_0 <= 9261
 1 <= L_3_1_O_0 <= 9261
 1 <= L_3_2_O_0 <= 9261
 1 <= L_4_0_O_0 <= 4096
 1 <= L_4_1_O_0 <= 4096
 1 <= L_4_2_O_0 <= 4096
 1 <= num_Mul_Col_Var <= 3.7933056e+07
 [Op_0]_tmpNum_Mul_Col_Var_0 = 1
 [Op_0]_tmpNum_Mul_Col_Var_1 = 1
 1 <= [Op_0]_tmpNum_Mul_Col_Var_2 <= 9261
 1 <= num_Col_PE_Var <= 3.7933056e+07
 [Op_0]_num_Col_PE_Var_0 = 1
 [Op_0]_num_Col_PE_Var_1 = 1
 1 <= [Op_0]_num_Col_PE_Var_2 <= 9261
 1 <= num_PE_Sys_Var <= 3.7933056e+07
 [Op_0]_num_PE_Sys_Var_0 = 1
 [Op_0]_num_PE_Sys_Var_1 = 1
 1 <= [Op_0]_num_PE_Sys_Var_2 <= 9261
 1 <= num_Channels_Sys_Var <= 3.7933056e+07
 1 <= channel_Bandwidth_Var <= 3.7933056e+07
 1 <= num_Out_Col_Var <= 4096
 1 <= [Op_0]_num_Out_Col_Var_0 <= 4096
 1 <= num_Fil_Col_Var <= 3.7933056e+07
 1 <= [Op_0]_num_Fil_Col_Var_0 <= 3.7933056e+07
 num_red_out_col_Var <= 9261
 1 <= num_In_Col_Var <= 9261
 1 <= [Op_0]_num_In_Col_Var_0 <= 9261
 num_Red_Col_Var <= 3.7933056e+07
 num_Out_PE_Var <= 3.10747594752e+11
 num_Out_Sys_Var <= 3.10747594752e+11
 Out_Cost_Sys_Var <= 1.438916737499136e+15
 1 <= num_In_PE_Var <= 3.10747594752e+11
 num_In_Sys_Var <= 3.10747594752e+11
 In_Cost_Sys_Var <= 1.438916737499136e+15
 num_Fil_Loading_Var <= 3.10747594752e+11
Binaries
 b_0_0_0_O_0 b_0_1_0_O_0 b_0_2_0_O_0 b_1_0_0_O_0 b_1_1_0_O_0 b_1_2_0_O_0
 b_2_0_0_O_0 b_2_1_0_O_0 b_2_2_0_O_0 b_3_0_0_O_0 b_3_0_1_O_0 b_3_0_2_O_0
 b_3_0_3_O_0 b_3_0_4_O_0 b_3_0_5_O_0 b_3_0_6_O_0 b_3_0_7_O_0 b_3_0_8_O_0
 b_3_0_9_O_0 b_3_0_10_O_0 b_3_0_11_O_0 b_3_0_12_O_0 b_3_0_13_O_0
 b_3_0_14_O_0 b_3_0_15_O_0 b_3_1_0_O_0 b_3_1_1_O_0 b_3_1_2_O_0 b_3_1_3_O_0
 b_3_1_4_O_0 b_3_1_5_O_0 b_3_1_6_O_0 b_3_1_7_O_0 b_3_1_8_O_0 b_3_1_9_O_0
 b_3_1_10_O_0 b_3_1_11_O_0 b_3_1_12_O_0 b_3_1_13_O_0 b_3_1_14_O_0
 b_3_1_15_O_0 b_3_2_0_O_0 b_3_2_1_O_0 b_3_2_2_O_0 b_3_2_3_O_0 b_3_2_4_O_0
 b_3_2_5_O_0 b_3_2_6_O_0 b_3_2_7_O_0 b_3_2_8_O_0 b_3_2_9_O_0 b_3_2_10_O_0
 b_3_2_11_O_0 b_3_2_12_O_0 b_3_2_13_O_0 b_3_2_14_O_0 b_3_2_15_O_0
 b_4_0_0_O_0 b_4_0_1_O_0 b_4_0_2_O_0 b_4_0_3_O_0 b_4_0_4_O_0 b_4_0_5_O_0
 b_4_0_6_O_0 b_4_0_7_O_0 b_4_0_8_O_0 b_4_0_9_O_0 b_4_0_10_O_0 b_4_0_11_O_0
 b_4_0_12_O_0 b_4_1_0_O_0 b_4_1_1_O_0 b_4_1_2_O_0 b_4_1_3_O_0 b_4_1_4_O_0
 b_4_1_5_O_0 b_4_1_6_O_0 b_4_1_7_O_0 b_4_1_8_O_0 b_4_1_9_O_0 b_4_1_10_O_0
 b_4_1_11_O_0 b_4_1_12_O_0 b_4_2_0_O_0 b_4_2_1_O_0 b_4_2_2_O_0 b_4_2_3_O_0
 b_4_2_4_O_0 b_4_2_5_O_0 b_4_2_6_O_0 b_4_2_7_O_0 b_4_2_8_O_0 b_4_2_9_O_0
 b_4_2_10_O_0 b_4_2_11_O_0 b_4_2_12_O_0
Generals
 L_0_0_O_0 L_0_1_O_0 L_0_2_O_0 L_1_0_O_0 L_1_1_O_0 L_1_2_O_0 L_2_0_O_0
 L_2_1_O_0 L_2_2_O_0 L_3_0_O_0 L_3_1_O_0 L_3_2_O_0 L_4_0_O_0 L_4_1_O_0
 L_4_2_O_0 num_Mul_Col_Var [Op_0]_tmpNum_Mul_Col_Var_0
 [Op_0]_tmpNum_Mul_Col_Var_1 [Op_0]_tmpNum_Mul_Col_Var_2 num_Col_PE_Var
 [Op_0]_num_Col_PE_Var_0 [Op_0]_num_Col_PE_Var_1 [Op_0]_num_Col_PE_Var_2
 num_PE_Sys_Var [Op_0]_num_PE_Sys_Var_0 [Op_0]_num_PE_Sys_Var_1
 [Op_0]_num_PE_Sys_Var_2 num_Channels_Sys_Var channel_Bandwidth_Var
 num_Out_Col_Var [Op_0]_num_Out_Col_Var_0 num_Fil_Col_Var
 [Op_0]_num_Fil_Col_Var_0 num_red_out_col_Var num_In_Col_Var
 [Op_0]_num_In_Col_Var_0 num_Red_Col_Var num_Out_PE_Var num_In_PE_Var
End
