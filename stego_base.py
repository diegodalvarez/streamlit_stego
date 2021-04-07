import numpy as np
import streamlit as st
from PIL import Image

class Stego:
    
    def __init__(self, image, *message):
        
        self.image_name = image.name
        self.image = image
        self.message = message[0]
        

        #split the file name and ending
        file_name_split = self.image_name.split(".")
        
        #then we want to rename the file for the output
        output_name = file_name_split[0] + "_encoded"
        
        #then we want to save the file ending
        output_ending = file_name_split[1]
        
        #then we want to re add the file ending to the name
        output_file = output_name + "." + output_ending
        
        self.output_file = output_file

    def Encode(self):
        
        #open file
        img = Image.open(self.image, 'r')
        
        #get image size which is necessay for finding pixels
        width, height = img.size
        
        #put those pixels into an array
        array = np.array(list(img.getdata()))
        
        #this gets the amount of pixels
        total_pixels = int(array.size / 3)
        
        #add a delimiter
        self.message += "CyB3r"
        
        #now we want to turn that into binary this 
        hidden_message = ''.join([format(ord(i), "08b") for i in self.message])
        
        #now we want the size
        message_pixels = len(hidden_message)
    
        #make sure it can fit
        if message_pixels > total_pixels:
            st.write("message to big")
    
        #if they can fit
        else:
            
            #this will keep track of which pixel we are on
            index = 0
            
            #go through the pixels
            for i in range(total_pixels):
                
                #go through the RGB
                for j in range(0, 3):
                    
                    #check if they can fit
                    if index < message_pixels:
                        
                        #changing the pixel
                        array[i][j] = int(bin(array[i][j])[2:9] + hidden_message[index], 2)
                        
                        #update to keep on track
                        index += 1
                        
            #now rearrange the array so that we can create it into a photo
            array=array.reshape(height, width, 3)
            
            #encode the image
            enc_img = Image.fromarray(array.astype('uint8'), img.mode)
            
            #save the image
            enc_img.save(self.output_file)
            
            st.write("message encoded, file output is called", self.output_file)
    
    def Decode(self):
        
        #read image
        img = Image.open(self.output_file, 'r')
        
        #put that into the array
        array = np.array(list(img.getdata()))
    
        #get the total pixels
        total_pixels = int(array.size / 3)
    
        #start with an empty string so that for the message that we are looking for
        bits = ""
        
        #go through the pixels
        for i in range(total_pixels):
            
            #go through RGB
            for j in range(0, 3):
                
                #put all those binary into the one string
                bits += (bin(array[i][j])[2:][-1])
        
        #put all those bits together
        bits = [bits[i:i+8] for i in range(0, len(bits), 8)]
        
        #now we want to go through the binary and try to find the delimeter
        
        #start with an empty string
        message = ""
        
        #now go through and try to find the delimeter
        for i in range(len(bits)):
            
            #try and find delimeter
            if message[-5:] == "CyB3r":
                break
            
            else:
                message += chr(int(bits[i], 2))
                
        #the case that the message has the delimeter         
        if "CyB3r" in message:
            st.write("Hidden Message:", message[:-5])
        else:
            st.write("No Hidden Message Found")
