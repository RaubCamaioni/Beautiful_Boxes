# Beautiful_Boxes
Python Script Generates Boxs Recursively 

Pulled from a seperate project and turned to "art" efforts.
Splits boxes recursively with some added randomness, colors, and different constrainst on the number of splits. 

Also returns a node list of the splits. My other project uses these nodes as a building block 
for synthetic circuit diagram images. 

Below are a few example outputs. Vary a couple different parameters for different outputs. 

split by the aspect ratio (always split along the long side) random colors :)
the pattern is interesting and unintended. probably caused by some rounding error and recursion depth
![alt text](https://github.com/RaubCamaioni/Beautiful_Boxes/blob/master/images/even_split_random_colors.PNG)

split aspect with added noise to split location, random colors
![alt text](https://github.com/RaubCamaioni/Beautiful_Boxes/blob/master/images/small_aspect_split_random_colors.PNG)

split randomly with added noise to split location, random colors
![alt text](https://github.com/RaubCamaioni/Beautiful_Boxes/blob/master/images/small_random_splits.PNG)

split randomly with added noise to split location, random colors (removed lines)
![alt text](https://github.com/RaubCamaioni/Beautiful_Boxes/blob/master/images/small_random_no_lines.PNG)

messing with the code (shrink boxes leave lines)
![alt text](https://github.com/RaubCamaioni/Beautiful_Boxes/blob/master/images/messing_with_the_code.PNG)

removing even split constraint (had some naive code that needed to be changed)
![alt text](https://github.com/RaubCamaioni/Beautiful_Boxes/blob/master/images/glass_pane.PNG)
