Bash command to execute the applescripts (on MacOS):

osascript <script-name>.scpt 'file-name' timeInSeconds

Eg: osascript audio_movie_and_screen_recorder.scpt 'recording1' 10

runMovieRecorder.scpt - records a movie/video using the laptop camera for the mentioned duration and
saves the file as .mov using the specified filename.

runScreenRecorder.scpt - records the laptop screen for the mentioned duration and saves the file as 
.mov using the specified filename.

runAudioRecorder.scpt - records an audio using the in-built laptop microphone for the mentioned 
duration and saves the file as .m4a using the specified filename.

runMovieandScreenRecorder.scpt - records a movie/video and the screen simultaneously for the mentioned
duration by starting to record at a single instant. The two files are saved using the filename 
specified along with an indicator to show which is a screen recording and which is a video recording.

audio_movie_and_screen_recorder.scpt - records a movie/video, screen and audio simultaneously for the 
mentioned duration by starting to record at a single instant. The files are saved in appropriate 
formats using the filename specified along with an indicator to show which is which. In this case, 
audio is extracted from the video and saved separately. So there is no explicit audio recording that
happens along with screen and video recording.

