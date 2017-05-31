# complex_fractal
A multi-threaded Python program using Numpy, MatplotLib to explore different types of fractals.

# Usage

Find this line

```
p = Pool(12);
```

and replace 12 with the number of threads you wish to run. Usually this is the number of threads in your CPU, ie. 8 for i7-7700K or most i7's, 4 for i5-7600K or most i5's. 

## Drawing a 11x11 fractal array

This feature is used to draw an array of fractals for exploring what kinds of parameters for the constant value generate what kinds of fractals.

Set this line to 0 for this drawing mode.

```
draw_single = 0;
```

Set how many rows and columns of fractals. I recommend 11x11 for starting out.

```
mass_rows = 11;
mass_cols = 11;
```

Set the range of the parameter you wish to explore. In this case it is the real and imaginary components of the constant.

```
c_r_low = -0.8;
c_r_high = -1.0;

c_i_low = -0.4;
c_i_high = -0.6;
```

Tweak the exponent and zoom.

```
params = (0.4, -0.1, 2, 120, 5, 5);
```

These values represent (c_real, c_imaginary, exponent, iterations, limit_sq_dist, zoom). The first two parameters do nothing in this case. You don't need to tweak iterations and limit_sq_dist. Leave the exponent at 2 for starting out.

Run the program.

```
./python fractal_gen_v5-multiprocess-git.py
```

An output image will be placed in the current directory.

Tip: Draw a 11x11 fractal array, then when you want to "zoom in" somewhere to see intermediate fractals, note the parameters above the fractal and enter them into c_r_low, c_r_high, c_i_low, and c_i_high.

## Drawing a single large fractal

Set this line to 1 for this drawing mode.

```
draw_single = 1;
```
Tweak the exponent and zoom.

```
params = (0.4, -0.1, 2, 120, 5, 5);
```

These values represent (c_real, c_imaginary, exponent, iterations, limit_sq_dist, zoom). The first two parameters specify the real and imaginary compnents of the fractal. You can use values for fractals you obtained in the above section for a more detailed view of a fractal. You don't need to tweak iterations and limit_sq_dist. Leave the exponent at 2 for starting out.

Run the program.

```
./python fractal_gen_v5-multiprocess-git.py
```

An output image will be placed in the current directory.

# Changing the type of fractal

Look for this line:

```
# The line that performs the iteration. Change the formula to obtain new classes of fractals.
		data = np.select( \
			(np.less_equal(squared_distances, limit_squared_distance), np.ones((img_y, img_x), dtype=bool)), \
			(np.power(data, exponent)) + c_constant, data) \
			)
```      

The 4th line here specifies the function for the iteration. You can change it to 

```
(np.sin(np.power(data, exponent))) + c_constant, data)
```

To add a sine function into the mix and change the type of fractal generated. Play around with different functions such as exp(), log(), cos(), tan(), try negative exponents, different exponents, and any other you can think of. Remember that sine can be expressed in terms of exponential functions.
