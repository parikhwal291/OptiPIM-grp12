module {
  func.func @forward(%arg0: tensor<1x210x15x15xf32>, %arg1: tensor<384x210x3x3xf32>, %arg2: tensor<1x384x13x13xf32>) -> tensor<1x384x13x13xf32> {
    %0 = linalg.conv_2d_nchw_fchw {dilations = dense<1> : vector<2xi64>, global_layer_idx = 0 : i32, layer_group = 0 : i32, num_banks = 32 : i32, strides = dense<1> : vector<2xi64>, type_layer_idx = 0 : i32} ins(%arg0, %arg1 : tensor<1x210x15x15xf32>, tensor<384x210x3x3xf32>) outs(%arg2 : tensor<1x384x13x13xf32>) -> tensor<1x384x13x13xf32>
    return %0 : tensor<1x384x13x13xf32>
  }
}
