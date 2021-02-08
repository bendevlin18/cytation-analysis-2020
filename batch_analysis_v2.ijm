// ask user to select a folder
dir = getDirectory("Select A folder");
// get the list of files (& folders) in it
fileList = getFileList(dir);
// prepare a folder to output the images
output_dir = dir + File.separator + "batch_output_files" + File.separator ;
File.makeDirectory(output_dir);


//activate batch mode
setBatchMode(true);


// LOOP to process the list of files
for (i = 0; i < lengthOf(fileList); i++) {
	// define the "path" 
	// by concatenation of dir and the i element of the array fileList
	current_imagePath = dir+fileList[i];
	
	// basic if statement to make sure we are not including any directory folders in this loop
	// otherwise it will error out :(
	if (!File.isDirectory(current_imagePath)){

		// open the image
		open(current_imagePath);
		// run("Bio-Formats Importer", "open=" + current_imagePath + " autoscale color_mode=Grayscale rois_import=[ROI manager] view=Hyperstack stack_order=XYCZT");
		// get some info about the image
		getDimensions(width, height, channels, slices, frames);
		currentImage_name = getTitle();
		
		///// THESE ARE OLD PROCESSING STEPS, CAN ADD OR SUBTRACT OTHERS FROM HERE AS NEEDED /////
		//setOption("ScaleConversions", true);
		//run("Enhance Contrast", "saturated=0.35");
		//run("Scale...", "x=.25 y=.25 z=1.0 width=688 height=552 depth=19 interpolation=Bilinear average process create");
		//run("Auto Threshold", "method=Mean white");
		
		run("Set Measurements...", "area mean standard min display invert redirect=None decimal=3");
		run("Measure");
		selectWindow("Results");
		close();

}
}

saveAs("Measurements", output_dir +"full_output_fiji.csv");
print("All Done! You can find the output here: " + output_dir +"full_output_fiji.csv");