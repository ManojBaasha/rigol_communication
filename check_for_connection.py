import pyvisa

rm = pyvisa.ResourceManager()
# pyvisa.log_to_screen() # Use this line to debug to find errors in the code
print(rm.list_resources())

# If successfully detected, your output should be 
# ('USB0::0x1AB1::0x0588::DS1ET180300771::INSTR', ) based on your device configs