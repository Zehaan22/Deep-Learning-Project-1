import cv2
import torch
import numpy as np

label = 2
for label in range(0, 10):
    for k in range(1, 2):
        for l in range(16, 26):
            # Load the input image
            image = cv2.imread(
                f'archive/nhcd/nhcd/numerals/{label}/00{k}_{l}.jpg')

            # Use the cvtColor() function to grayscale the image
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Converting to matrix
            gray_mat = [0]*30
            for i in gray_image:
                foo = [0]
                for j in i:
                    if j > 255//2:
                        foo.append(0)
                    else:
                        foo.append(1)
                foo.append(0)
                gray_mat.extend(foo)
            gray_mat.extend([0]*30)

            # Loading the data tensore
            X_data = torch.load("X_data.pt")
            X_data = X_data.numpy()
            # Adding our element to the data
            X_data = np.append(X_data, [gray_mat], axis=0)
            X_data = torch.from_numpy(X_data)
            # Saving the data matrix
            torch.save(X_data, "X_data.pt")
            print("Saved the matrix")

            # Saving the label
            y_data = torch.load("y_data.pt")
            y_data = y_data.numpy()
            # Adding our element to the data
            y_data = np.append(y_data, [label])
            y_data = torch.from_numpy(y_data)
            # Saving the data matrix
            torch.save(y_data, "y_data.pt")
            print(f"Saved as the lable {label}")
