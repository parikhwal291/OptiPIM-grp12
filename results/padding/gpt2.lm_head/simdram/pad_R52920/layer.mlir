module {
  func.func @forward(%arg0: tensor<1x768xf32>, %arg1: tensor<768x52920xf32>, %arg2: tensor<1x52920xf32>) -> tensor<1x52920xf32> {
    %0 = linalg.matmul {global_layer_idx = 0 : i32, layer_group = 0 : i32, num_banks = 32 : i32, type_layer_idx = 0 : i32} ins(%arg0, %arg1 : tensor<1x768xf32>, tensor<768x52920xf32>) outs(%arg2 : tensor<1x52920xf32>) -> tensor<1x52920xf32>
    return %0 : tensor<1x52920xf32>
  }
}
