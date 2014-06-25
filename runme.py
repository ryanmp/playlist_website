
import os, Image, jinja2, PIL.ImageOps, ImageEnhance, ImageFilter, commands

def Main():
	# looks for audio files in current dir
	song_list, song_extensions, song_list_san = GetSongList()

	song_lengths = GetSongLengths(song_list_san, song_extensions)

	# makes 3 new directories, populates them with generated
	# aac, ogg, and mp3 (for maximum compatibility)
	#TranscodeToMultipleFormats(song_list)

	# uses sox to generate a spectrogram image for each audiofile
	# stored in /img
	GenerateSpectrograms(song_list_san,song_extensions,song_list)

	# makes our index.html file from index.jinja
	RenderTemplate(song_list,song_lengths, song_list_san)

	GenerateBlurredBg()

def GetSongList():
	path = os.getcwd()
	music_files = []
	music_files_sanitized = []
	music_file_extensions = []
	all_files = os.listdir(path+'/songs_input')
	for f in all_files:
		if f.endswith(('.mp3', '.aac','.ogg','.wav')):
			tmp = f.split('.')
			music_files.append(tmp[0])
			tmp[0] = tmp[0].replace(" ","\ ")
			music_files_sanitized.append(tmp[0])
			music_file_extensions.append(tmp[1])

	return music_files, music_file_extensions, music_files_sanitized

def TranscodeToMultipleFormats(s):
	return 0

def RenderTemplate(s,s_len, s_san):
	templateEnv = jinja2.Environment( loader= jinja2.FileSystemLoader( os.getcwd() ) )
	template = templateEnv.get_template( "index.jinja" )

	templateVars = { "title" : "dead-simple html5 audio playlist",
	                 "songs" : s,
	                 "song_lengths" : s_len,
	                 "songs_san" : s_san
	               }

	index = open('index.html', 'w+')
	index.write( template.render( templateVars ) ) 

def GenerateBlurredBg():
	tmp_img = Image.open("bg.png")
	for i in range(4):
		tmp_img = tmp_img.filter(ImageFilter.BLUR)

	w, h = tmp_img.size

	whiten = Image.new("RGBA", tmp_img.size, (255,255,255))
	tmp_img = Image.blend(tmp_img, whiten, .9)

	tmp_img = tmp_img.crop((5,0,w-5,h))
	tmp_img.save("bg_blurred.png")


def GetSongLengths(s,e):
	l = []
	for i in s:

		in_secs = int(float(commands.getoutput("soxi -D songs_input/" + i + "." + e[0]) ) )

		ft_sec = in_secs % 60
		ft_mins = in_secs / 60

		if (ft_sec < 10):
			ft_sec = '0'+str(ft_sec)

		formatted_time = str(ft_mins)+":"+str(ft_sec)

		l.append( formatted_time )

	return l

def GenerateSpectrograms(s,e,s2):

	os.system("mkdir spectrograms")

	for i in xrange(len(s)):
		print ("generating spectrogram for:",s[i])
		temp_cmd = "sox songs_input/" + s[i] + "." + e[0] + " -n remix 1 spectrogram -r -x 800 -y 64 -l -h -o top.png"
		os.system(temp_cmd)

		temp_cmd = "sox songs_input/" + s[i] + "." + e[0] + " -n remix 2 spectrogram -r -x 800 -y 64 -l -h -o bottom.png"
		os.system(temp_cmd)

		new_img = Image.new('RGB', (800,128))
		img = Image.open("top.png")
		img2 = Image.open("bottom.png")
		new_img.paste(img, (0,0))
		new_img.paste(img2.transpose(Image.FLIP_TOP_BOTTOM), (0,64))
		#new_img = PIL.ImageOps.invert(new_img)

		enhancer = ImageEnhance.Contrast(new_img)
		new_img = enhancer.enhance(.35)

		enhancer = ImageEnhance.Brightness(new_img)
		new_img = enhancer.enhance(1.4)


		new_img.save("spectrograms/" + s2[i] + ".jpg", "JPEG", quality=35, optimize=True)
		os.system("rm top.png bottom.png")

	return 0

print Main()