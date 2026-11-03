module {
  func.func @forward(%arg0: tensor<1x512x9x9xf32>, %arg1: tensor<560x512x3x3xf32>, %arg2: tensor<1x560x7x7xf32>) -> tensor<1x560x7x7xf32> {
    %0 = linalg.conv_2d_nchw_fchw {dilations = dense<1> : vector<2xi64>, global_layer_idx = 0 : i32, layer_group = 0 : i32, num_banks = 32 : i32, type_layer_idx = 0 : i32, strides = dense<1> : vector<2xi64>} ins(%arg0, %arg1 : tensor<1x512x9x9xf32>, tensor<560x512x3x3xf32>) outs(%arg2 : tensor<1x560x7x7xf32>) -> tensor<1x560x7x7xf32>
    return %0 : tensor<1x560x7x7xf32>
  }
}
