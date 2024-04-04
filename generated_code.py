python
# Function to calculate the area of a rectangle
def rectangle_area(length, width):
    # Calculate and return the area
    return length * width

# Take input from user for length and width
length = float(input("Enter the length of the rectangle: "))
width = float(input("Enter the width of the rectangle: "))

# Call the function to calculate the area and display it
area = rectangle_area(length, width)
print("The area of the rectangle is", area)
