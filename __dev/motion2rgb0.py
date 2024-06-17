l=load_img_folder_to_dict("/Volumes/CalvaryLG Mexico 2022/motion0-frames-10Hz/IMG_1971")

gs=list(l.values())

for i in range(2,len(gs)):
	g=1*gs[i]
	g[:,:,2]=np.abs(g[:,:,2]-g[:,:,1])
	g[:,:,0]=0#1*gs[i-2][:,:,1]
	g[:,:,1]=0#1*gs[i-1][:,:,1]
	sh(g)
	spause()
	time.sleep(0.1)
