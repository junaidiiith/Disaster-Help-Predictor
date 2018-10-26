import os
import numpy as np
import face_recognition
import pickle

dir_path = os.path.dirname(os.path.realpath(__file__))

def searchImage(img_path, name):

	with open(dir_path+'/face_recognition_encodings.pkl','rb') as f:
		encodings,tags,images = pickle.load(f)

	new_picture = face_recognition.load_image_file("/home/junaid/Downloads/CodeFunDo/BlogPost/media/media/"+img_path)
	new_face_encoding = face_recognition.face_encodings(new_picture)

	if len(new_face_encoding) < 1:
		return ('No face recognised, please input more clear picture')
	else:
		# print(type(new_face_encoding),new_face_encoding,list(encodings.values())[:5])
		results = face_recognition.compare_faces(list(encodings.values()), new_face_encoding[0])
		if any(results):
			return 'This person is already in our database with name :',list(encodings.keys())[results.index(True)]
		else:
			encodings[name] = new_face_encoding[0]
			
			with open('face_recognition_encodings.pkl','wb') as f:
				pickle.dump([encodings,tags,images],f)
