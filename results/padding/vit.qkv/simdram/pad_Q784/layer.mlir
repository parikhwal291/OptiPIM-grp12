module {
  func.func @forward(%arg0: tensor<197x784xf32>, %arg1: tensor<784x2304xf32>, %arg2: tensor<197x2304xf32>) -> tensor<197x2304xf32> {
    %0 = linalg.matmul {global_layer_idx = 0 : i32, layer_group = 0 : i32, num_banks = 32 : i32, type_layer_idx = 0 : i32} ins(%arg0, %arg1 : tensor<197x784xf32>, tensor<784x2304xf32>) outs(%arg2 : tensor<197x2304xf32>) -> tensor<197x2304xf32>
    return %0 : tensor<197x2304xf32>
  }
}
