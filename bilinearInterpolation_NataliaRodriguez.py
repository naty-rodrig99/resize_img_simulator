import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

class InterpolationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bilinear Interpolation")
        self.configure(bg="white")
        
        default_original = 4
        default_new = 6
        
        # Group input fields
        input_frame = tk.Frame(self, bg="white")
        input_frame.pack(pady=10)

        self.grid_dims_label = tk.Label(input_frame, text="Input Grid Dimensions:", bg="white", font=("Inter",10))
        self.grid_dims_label.grid(row=0, column=0, padx=(10,5), pady=5, sticky='e')
        self.grid_dims_entry1 = tk.Entry(input_frame, width=5, bg="lightgray", font=("Inter",10))
        self.grid_dims_entry1.grid(row=0, column=1, pady=5)
        self.x_label = tk.Label(input_frame, text="X", bg="white", font=("Inter",10))
        self.x_label.grid(row=0, column=2, padx=(10,5), pady=5, sticky='e')
        self.grid_dims_entry2 = tk.Entry(input_frame, width=5, bg="lightgray", font=("Inter",10))
        self.grid_dims_entry2.grid(row=0, column=3, pady=5)

        self.new_shape_label = tk.Label(input_frame, text="Output Grid Dimensions:", bg="white", font=("Inter",10))
        self.new_shape_label.grid(row=1, column=0, padx=(10,5), pady=5, sticky='e')
        self.new_shape_entry = tk.Entry(input_frame, width=5, bg="lightgray", font=("Inter",10))
        self.new_shape_entry.grid(row=1, column=1, pady=5)
        self.x2_label = tk.Label(input_frame, text="X", bg="white", font=("Inter",10))
        self.x2_label.grid(row=1, column=2, padx=(10,5), pady=5, sticky='e')
        self.new_shape_entry2 = tk.Entry(input_frame, width=5, bg="lightgray", font=("Inter",10))
        self.new_shape_entry2.grid(row=1, column=3, pady=5)

        # Interpolation button
        submit_button = tk.Button(self, text="Interpolate", command=self.interpolate_again, font=("Inter",10), bg="lightblue", fg="black")
        submit_button.pack(pady=5)

        # Frames for original and interpolated grids
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack(side=tk.LEFT, padx=default_original, pady=default_original)

        self.interpolated_frame = tk.Frame(self)
        self.interpolated_frame.pack(side=tk.RIGHT, padx=default_new, pady=default_new)

        # Display initial random grid
        self.grid_data = np.random.randint(0, 255, size=(default_original, default_original, 3), dtype=np.uint8) 
        self.display_grid(self.grid_data, self.grid_frame)
        
        # Initialize interpolation
        self.new_shape = (default_new, default_new)
        self.interpolated_data = np.zeros((self.new_shape[0], self.new_shape[1], self.grid_data.shape[2]), dtype=np.uint8)
        self.current_interpolation_step = 0
        self.bilinear_interpolation_step()

    def display_grid(self, data, frame, interp_pixels=None):
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                # formats the RGB values into a hexadecimal color code
                color = '#%02x%02x%02x' % tuple(data[i, j])
                cell = tk.Label(frame, bg=color, width=4, height=3, padx=2, pady=2, text=f"{i},{j}")
                cell.grid(row=i, column=j, padx=1, pady=1)
    
    def bilinear_interpolation_step(self):
        #Extracts the dimensions of the original grid
        old_shape = self.grid_data.shape[:2]
        i, j = divmod(self.current_interpolation_step, self.new_shape[1])
        
        y_ratio = i / (self.new_shape[0] - 1) * (old_shape[0] - 1)
        x_ratio = j / (self.new_shape[1] - 1) * (old_shape[1] - 1)

        y_index = int(y_ratio)
        x_index = int(x_ratio)
        y_diff = y_ratio - y_index
        x_diff = x_ratio - x_index

        #Boundary conditions for the last row and column
        if i == self.new_shape[0] - 1:
            y_index = min(y_index, old_shape[0] - 2)
        if j == self.new_shape[1] - 1:
            x_index = min(x_index, old_shape[1] - 2)

        #k represents the color channel: red, green, or blue
        for k in range(self.grid_data.shape[2]):
            top_left = self.grid_data[y_index, x_index, k]
            top_right = self.grid_data[y_index, x_index + 1, k]
            bottom_left = self.grid_data[y_index + 1, x_index, k]
            bottom_right = self.grid_data[y_index + 1, x_index + 1, k]

            #check if gets to last column
            if j == self.new_shape[1] - 1:
                top_left = top_right
                bottom_left = bottom_right
                
            #2 interpolations in x
            top = top_left * (1 - x_diff) + top_right * x_diff
            bottom = bottom_left * (1 - x_diff) + bottom_right * x_diff

            #check if gets to last row
            if i == self.new_shape[0] - 1:
                top = bottom
                            
            #1 interpolation in y
            self.interpolated_data[i, j, k] = int(top * (1 - y_diff) + bottom * y_diff)

        self.display_grid(self.interpolated_data, self.interpolated_frame)
        self.current_interpolation_step += 1 #increment counter
        
        if self.current_interpolation_step < self.new_shape[0] * self.new_shape[1]:
            self.after(100, self.bilinear_interpolation_step) #called recursively

    def interpolate_again(self):
        # Get new input values
        input_grid_dims1 = int(self.grid_dims_entry1.get())
        input_grid_dims2 = int(self.grid_dims_entry2.get())
        output_grid_dims = int(self.new_shape_entry.get())
        output_grid_dims2 = int(self.new_shape_entry2.get())

        # Update the original grid and interpolated grid based on new inputs
        self.grid_data = np.random.randint(0, 255, size=(input_grid_dims1, input_grid_dims2, 3), dtype=np.uint8)
        self.new_shape = (output_grid_dims, output_grid_dims2)
        self.interpolated_data = np.zeros((self.new_shape[0], self.new_shape[1], self.grid_data.shape[2]), dtype=np.uint8)
        self.current_interpolation_step = 0

        # Remove previous original grid widgets
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

        # Remove previous interpolated grid widgets
        for widget in self.interpolated_frame.winfo_children():
            widget.destroy()

        # Redo bilinear interpolation
        self.display_grid(self.grid_data, self.grid_frame)
        self.bilinear_interpolation_step()

if __name__ == "__main__":
    app = InterpolationApp()
    app.mainloop()
