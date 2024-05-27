import matplotlib.pyplot as plt
import numpy as np

# Grid values
grid_x = np.array([2, 4, 6, 8, 10])
grid_y = np.array([2, 4, 6, 8, 10])

# Camera values
camera_x = np.array([2.89, 4.89, 6.89, 8.89, 10.89])
camera_y = np.array([4.36, 6.36, 8.36, 10.36, 12.36])

# Fit a polynomial curve for Grid values
grid_coeffs = np.polyfit(grid_x, grid_y, 2)
grid_poly = np.poly1d(grid_coeffs)
grid_curve_x = np.linspace(min(grid_x), max(grid_x), 100)
grid_curve_y = grid_poly(grid_curve_x)

# Fit a polynomial curve for Camera values
camera_coeffs = np.polyfit(camera_x, camera_y, 2)
camera_poly = np.poly1d(camera_coeffs)
camera_curve_x = np.linspace(min(camera_x), max(camera_x), 100)
camera_curve_y = camera_poly(camera_curve_x)

# Plotting both sets on the same graph
plt.figure(figsize=(10, 5))
plt.scatter(grid_x, grid_y, color='red', label='Grid Values')
plt.plot(grid_curve_x, grid_curve_y, 'r-', label='Grid Curve Fit')
plt.scatter(camera_x, camera_y, color='blue', label='Camera Values')
plt.plot(camera_curve_x, camera_curve_y, 'b-', label='Camera Curve Fit')

# Adding titles and labels
plt.title('Curve Fit Comparison of Grid Values vs. Camera Values')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()

# Display the graph
plt.show()
