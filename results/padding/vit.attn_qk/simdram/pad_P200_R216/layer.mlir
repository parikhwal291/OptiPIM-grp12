module {
  func.func @forward(%arg0: tensor<12x200x64xf32>, %arg1: tensor<12x64x216xf32>, %arg2: tensor<12x200x216xf32>) -> tensor<12x200x216xf32> {
    %0 = linalg.batch_matmul {global_layer_idx = 0 : i32, layer_group = 0 : i32, num_banks = 32 : i32, type_layer_idx = 0 : i32} ins(%arg0, %arg1 : tensor<12x200x64xf32>, tensor<12x64x216xf32>) outs(%arg2 : tensor<12x200x216xf32>) -> tensor<12x200x216xf32>
    return %0 : tensor<12x200x216xf32>
  }
}
