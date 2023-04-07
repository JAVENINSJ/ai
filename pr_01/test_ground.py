import tkinter as tk

# Create a window
window = tk.Tk()
a = 10
# Create a canvas widget and place it behind the grid of buttons
canvas = tk.Canvas(window, background="blue")
canvas.grid(row=0, column=0, rowspan=a, columnspan=a)
  # Move the canvas to the back of the display order

# Create a 5x5 grid of buttons
for i in range(a):
    for j in range(a):
        button = tk.Button(window, text="o")
        button.grid(row=i, column=j)

# Run the main event loop
window.mainloop()
