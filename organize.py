import os
import shutil

folder = "test_folder"

for file in os.listdir(folder):
    if os.path.isfile(os.path.join(folder, file)):
        ext = file.split('.')[-1]
        dest = os.path.join(folder, ext)

        if not os.path.exists(dest):
            os.makedirs(dest)

        shutil.move(
            os.path.join(folder, file),
            os.path.join(dest, file)
        )

print("Files organized successfully.")

