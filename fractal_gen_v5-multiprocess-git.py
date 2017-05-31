import numpy as np

import matplotlib.pyplot as plt

from multiprocessing import Pool

import os #to create temp directory

from PIL import Image #to join the images

import datetime #for timestamp
import time
start_time = time.time();

draw_single = 0;
#draw_single = False;
#draw_single = True;

mass_rows = 11;
mass_cols = 11;

temp_directory_name = "fractalgen_temp"

small_figure_size = 6;
large_figure_size = 10;
figure_dpi = 100; #100 makes for easy calculations when a divisor of img_x, img_y

if (draw_single):
	plt.figure(figsize=(large_figure_size, large_figure_size), dpi=figure_dpi)
else:
	plt.figure(figsize=(small_figure_size, small_figure_size), dpi=figure_dpi)

img_x = int(400 * 1.0)
img_y = int(400 * 1.0)

#img_x = 3000;
#img_y = 3000;

if (draw_single == False):
	img_x = int(400 * 0.25)
	img_y = int(400 * 0.25)

#img_x = 32
#img_y = 18

phi = 1.6180339887498948482;
pi = 3.1415926535897932384626433;
euler = 2.7182818284590452353602874;


#params = (0.285, 0.01, 2, 120, 5, 2.5); #default
#params = (0.6250, -0.5625, 6, 120, 5, 2.5); #dd

#c_r, c_i, exponent, iterations, limit_sq_dist, zoom
params = (0.4, -0.1, 2, 120, 5, 2.5);

c_r_low = -1.0;
c_r_high = 1.0;

c_i_low = -1.0;
c_i_high = 1.0;

if (0):
	c_r_low = -4.0;
	c_r_high = 4.0;

	c_i_low = -4.0;
	c_i_high = 4.0;

if (0):
	c_r_low = -2.0;
	c_r_high = 2.0;

	c_i_low = -2.0;
	c_i_high = 2.0;
	
if (0):
	c_r_low = -1.0;
	c_r_high = 1.0;

	c_i_low = -1.0;
	c_i_high = 1.0;


def draw(c_r, c_i, exponent, iterations, limit_squared_distance, zoom, filename, index, total):

	current_figure_start_time = time.time();
	
	c_constant = np.complex(c_r, c_i);
	
	data = np.zeros((img_y, img_x), np.complex64)
	display_data = np.zeros((img_y, img_x))
	
	# Initialize data array
	for i in range(img_y):
		for j in range(img_x):
			data[i, j] = np.complex( \
				j / img_x * zoom - (zoom/ 2), \
				i / img_y * zoom - (zoom / 2))
	
	# Iteration
	# ============================================
	
	#speed_zeros = np.zeros((img_y, img_x));
	#speed_true = np.ones((img_y, img_x), dtype=bool);

	squared_distances = np.zeros((img_y, img_x))
	iteration_data = np.full((img_y, img_x), np.nan)

	for i in range(iterations):

		#if (i % 25 == 0):
			#print("Iteration " + str(i) + " of " + str(iterations))

		squared_distances = np.add(np.power(np.real(data), 2), \
			np.power(np.imag(data), 2))

		# Will return a warning for comparing with np.nan but that's what we're trying to do
		try:
			fmin_result = np.fmin(np.full((img_y, img_x), i, dtype=int), iteration_data)
		except np.RuntimeWarning:
			pass
			
		iteration_data = np.select( \
			(np.greater(squared_distances, limit_squared_distance), np.ones((img_y, img_x), dtype=bool)), \
			(fmin_result, np.full((img_y, img_x), np.nan)) \
			)
		
#		a_constant = np.complex(-1.0, 1.0);
		a_constant = np.complex(1.0, 0.0);
		
		# The line that performs the iteration. Change the formula to obtain new classes of fractals.
		data = np.select( \
			(np.less_equal(squared_distances, limit_squared_distance), np.ones((img_y, img_x), dtype=bool)), \
			(np.power(data, exponent) + c_constant, data) \
			)
		
		#data = np.select( \
	#		(np.less_equal(squared_distances, limit_squared_distance), np.ones((img_y, img_x), dtype=bool)), \
	#		(np.exp(np.complex(0.0, 1.0) * np.power(data, exponent)) + c_constant, data) \
	#		)
			
	# Sets remaining values for coordinates didn't hit the limit to iteration (one above max of others)
	iteration_data = np.select( \
		(np.isnan(iteration_data), np.ones((img_y, img_x), dtype=bool)),	\
		(np.full((img_y, img_x), iterations, dtype=np.int32), iteration_data) \
		)

	# ============================================

	#print(data[50, 60])

	display_data = np.copy(iteration_data)
	
	plt.title(format(c_r, '') + ", " + format(c_i, ''))
	
	plt.xticks([])
	plt.yticks([])

	plt.pcolor(display_data)
	
	plt.tight_layout()
	
	if (draw_single == False):
		plt.subplots_adjust(left=0.025, right=0.975, top=0.95, bottom=0.0)
	else:
		plt.subplots_adjust(left=0.03, right=0.97, top=0.97, bottom=0.03)
		
	#print("Finished drawing subplots after " + format(time.time() - start_time, '.2f') + " seconds.")

	#plt.colorbar()

	#plt.ylabel('y')
	#plt.show()

	plt.savefig(filename)
	plt.clf();
	
#	draw_rate = float(index + 1.0) / (time.time() - start_time);
#	time_remaining = (total - index - 1) / draw_rate;
	
	# We include the time it took to draw each subplot because of a past incident where there was slowdowns due to memory leakage
	print("Drew " + filename + " in " + format(time.time() - current_figure_start_time, '.2f') + " seconds. Time elapsed: " + format(time.time() - start_time, '.2f') + " seconds.")
	
#	print ("Drawing " + str(index + 1) + " of " + str(total))
#	print("Drew " + filename + " in " + format(time.time() - current_figure_start_time, '.2f') + " seconds. Time remaining: " + format(time_remaining, '.2f') + " seconds.")
	
	
if __name__ == '__main__':

	if (draw_single):
		mass_rows = 1;
		mass_cols = 1;
		
		c_r_low = params[0];
		c_r_high = params[0];
		
		c_i_low = params[1];
		c_i_high = params[1];
		
	print("mass_rows: " + str(mass_rows));
	print("mass_cols: " + str(mass_cols));
	
	call_list = [];
	
	for c_r_counter in range(mass_rows):

		c_constant_real = 0.0;
		if (mass_rows == 1):
			c_constant_real = (c_r_low + c_r_high) / 2;
		else:
			c_constant_real = (float(c_r_counter) / (mass_rows - 1)) * (c_r_high - c_r_low) + c_r_low
		
		for c_i_counter in range(mass_cols):
		
			c_constant_imag = 0.0;
			if (mass_cols == 1):
				c_constant_imag = (c_i_low + c_i_high) / 2;
			else:
				c_constant_imag = (float(c_i_counter) / (mass_cols - 1)) * (c_i_high - c_i_low) + c_i_low
	
			exponent = params[2];
			iterations = params[3];
			limit_squared_distance = params[4];
			zoom = params[5]
			
			filename = temp_directory_name + "/out_" + str(c_r_counter) + "," + str(c_i_counter) + ".png";
			
			call_list.append((c_constant_real, c_constant_imag, exponent, iterations, limit_squared_distance, zoom, filename, \
				c_r_counter * mass_cols + c_i_counter, mass_cols * mass_rows))
	
	if not os.path.exists(temp_directory_name):
		os.makedirs(temp_directory_name)
	
#	print(call_list);
	p = Pool(12);
	p.starmap(draw, call_list)

	# ToDO: Get this from the plt.figure
	each_image_size_x = small_figure_size * figure_dpi;
	each_image_size_y = small_figure_size * figure_dpi;
	
	if (draw_single):
		each_image_size_x = large_figure_size * figure_dpi;
		each_image_size_y = large_figure_size * figure_dpi;
	
	joined_im = Image.new('RGB', (each_image_size_x * mass_cols, each_image_size_y * mass_rows));
	
	# Join the images
	for c_r_counter in range(mass_rows):

		for c_i_counter in range(mass_cols):
			
			current_index = c_r_counter * mass_cols + c_i_counter;
			current_image_filename = call_list[current_index][6];
			current_im = Image.open(current_image_filename);
		
			joined_im.paste(current_im, (c_i_counter * each_image_size_x, c_r_counter * each_image_size_y));
	
	timestamp = format(datetime.datetime.now(), "%Y%m%d-%H%M%S");
	filename = "";
	if (params[2]) < 0:
		filename = "output-expneg" + str(abs(params[2])) + "-" + timestamp + ".png";
	else:
		filename = "output-exp" + str(params[2]) + "-" + timestamp + ".png";
	joined_im.save(filename)
	
	print("Saved to " + filename)
