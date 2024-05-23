# Classifying paintings by artist and style

## Introduction
How to correctly classify a painting? Art experts and curators are well acquainted with guidelines and rules that enable them to accurately identify a painting's category,
on the other hand laypeople lack this ability. However, advancements in computer vision and machine learning have automated and simplified this process, making it accessible even
to non-experts. <br>
But how does it work?

<div align="center">
  <img src="https://github.com/sanjarakanovic/PaintingClassification/blob/main/imgs/sc1.png"/>
</div>

Image classification involves assigning classes to input images and training a model on labeled data to predict the class of unseen images. 
Convolutional Neural Networks (CNNs) are commonly used for this task due to their ability to learn hierarchical representations of features from raw pixel values. 
CNN functions by processing images through numerous layers, with each layer progressively extracting more complex and abstract features. During training, 
the CNN adjusts its internal parameters based on the provided labeled data, optimizing its ability to accurately classify images. 
This iterative process involves comparing the network's predictions with the actual labels and updating the parameters accordingly through techniques like backpropagation.

<div align="center">
  <img src="https://github.com/sanjarakanovic/PaintingClassification/blob/main/imgs/cnn-features.png" style="width:80%;height:auto;"/>
</div>

Instead of starting the training process from scratch, which can be computationally demanding, time-consuming and prone to slow convergence, 
transfer learning is frequently employed. This approach involves using a pre-trained neural network that has already been trained on large and diverse dataset, 
and leveraging knowledge gained from solving one problem and applying it to different, but related, problem. But how the model trained to classify natural images 
can be used for painting classification? The key lies in the shared visual features across different domains, such as edges, textures, colors, and shapes. 
These low-level features are fundamental to both tasks and are encoded in the lower layers of the network. Higher layers combine these low-level features to 
detect more complex patterns and structures, such as specific object parts, object configurations, or entire objects themselves. These layers have learned to extract 
general features from natural images. By updating the parameters of these higher layers, the model can learn to extract and represent higher-level artistic features and 
concepts present in paintings. This form a transfer learning is called fine tuning, in contrast to feature extraction, where the model's weights remain unchanged. 
Transfer learning is particularly beneficial for small dataset domain-specific tasks, as is the case here.


## Dataset

Dataset used is Painting91, which is detailly explained here: http://www.cat.uab.cat/~joost/papers/2014MVApainting91.pdf

<div align="center">
  <img src="https://github.com/sanjarakanovic/PaintingClassification/blob/main/imgs/dataset.jpg"/>
</div>

## Data preparation

As usual, data must be prepared before being fed into the neural network, so the images are resized to an input size of a pre-trained model and the preprocessing function
used in the pre-trained model is applied. In an effort to minimize overfitting, enhance the diversity and robustness of the training data and enhance performance on the test
set, various augmentation techniques were explored, such as horizontal flipping, random zooming, translation, rotation, contrast adjustment, random cropping and random augment. 
Despite trying different combinations of these techniques, there was little observable progress in mitigating overfitting or enhancing overall performance. 
The model mostly achieved near-perfect training accuracy and despite this, it's performance on the test set did not show significant improvement and either remained stagnant
or even decreased slightly. Some techniques like random rotation and random augmentation (particularly when applying three augmentations per image), led to a decrease in both
training and test accuracy.


## Model building

The model comprises three main components: a base pre-trained model, a GlobalAveragePooling2D layer, and a Dense layer with softmax activation, serving as the classifier,
producing a probability distribution over the different classes present in the dataset. The number of neurons in this layer corresponds to the number of classes in the dataset. 
Various pre-trained models are explored such as: EfficientNetB0, EfficientNetV2S, ResNet50, VGG19, MobileNetV2 and InceptionV3. EfficientNetB0 was selected because it delivered
the best performance on the test set. 

<div align="center">
  <img src="https://github.com/sanjarakanovic/PaintingClassification/blob/main/imgs/model.png"/>
</div> 

## Feature extraction versus fine tuning

Feature extraction is naturally faster and reduces risk of overfitting since there is less trainable parameters. On the other hand, fine-tuning has higher performance potential, 
better adaptation and greater flexibility, albeit adding more complexity to the training process. <br>

<div align="center" >
  <img src="https://github.com/sanjarakanovic/PaintingClassification/blob/main/imgs/transferlearning.png" style="width:80%;height:auto;"/>
</div>

Both of these approaches were tested: fine-tuning by unfreezing all layers, unfreezing the top 10%, 15%, and 30% of layers. For a model trained on 13 classes, the difference
in accuracy between these fine-tuning methods was insignificant on the test set. However, for a model trained on 91 classes, unfreezing more layers resulted in slightly better 
performance. Unfreezing 30% or all layers gave similar results, which were better than unfreezing only 10% or 15%.
Fine-tuning resulted in slightly higher accuracy compared to feature extraction, making it preferable when maximizing accuracy is the primary objective. 
While feature extraction allowed for higher initial learning rates, such as 1e-2, fine-tuning suffered from instability at such rates, hence starting with 1e-3 is recommended. 


## Regularization techniques

Overfitting is a common challenge in machine learning where a model learns to memorize the training data rather than generalize patterns, resulting in poor performance on 
unseen data. Regularization techniques are used to mitigate overfitting and improve model generalization.  <br>

<div align="center">
  <img src="https://github.com/sanjarakanovic/PaintingClassification/blob/main/imgs/augmentation.png"/>
</div>

Data augmentation, as previously explained, was one of the methods employed. However, in this case, data augmentation did not help in preventing overfitting or improving performance. 
This could be due to the nature of the dataset or the model already being robust to these simple transformations, indicating that the variations introduced were not 
significant enough to enhance generalization. In some instances, both training and test accuracy decreased, suggesting that the augmented data might not have been 
representative of real-world variations or that the model struggled with the complexity of the augmented data.  <br>

<div align="center">
  <img src="https://github.com/sanjarakanovic/PaintingClassification/blob/main/imgs/dropout.png"/>
</div>

Dropout, a technique where random neurons are turned off during training to prevent over-reliance on specific features, was also tested but did not help in preventing 
overfitting or improving performance. This might be due to the model's architecture or the complexity of the task, where dropout may not have provided the necessary 
regularization.  <br>

<div align="center">
  <img src="https://github.com/sanjarakanovic/PaintingClassification/blob/main/imgs/l1l2.png"/>
</div>

L1 and L2 regularization add penalties to the loss function for large weights, encouraging the model to keep weights small and thereby reducing overfitting. 
L2 regularization, also known as Ridge regularization, penalizes large weights smoothly, aiming to keep all weights small, while L1 regularization, known as Lasso 
regularization, encourages the model to have fewer nonzero weights, inducing sparsity in the weights, making the model more robust to outliers. These techniques were 
tested with different strategies and were found to enhance the model's performance during fine-tuning, though they didn't improve performance during feature extraction. 
L2 regularization can be used effectively with values of 0.1 or higher. However, using such high values for L1 regularization can lead to underfitting, so a lower value like
0.01 is more suitable. L2 regularization performed better than L1 regularization in case with 91 classes, while they performed similarly in case with 13 classes.  <br>

<div align="center">
  <img src="https://github.com/sanjarakanovic/PaintingClassification/blob/main/imgs/ls.png"/>
</div>

Label smoothing, another technique that was helpful, works by softening the labels during training. Instead of assigning full probability to the correct class, it distributes 
some probability to incorrect classes, which helps in preventing the model from becoming overly confident in its predictions. This technique was effective with a smoothing 
rate of 0.1, which helped boost performance. Higher rates, however, did not provide additional benefits and could potentially harm the model's accuracy, particularly in case 
with 13 classes.


## Confusion matrices

Two models with the highest accuracy on the test set were chosen to display their confusion matrices:

 **13 classes:**

- **Loss: 1.2701**

- **Accuracy: 0.7546**

<div align="center">
  <img src="https://github.com/sanjarakanovic/PaintingClassification/blob/main/imgs/confusion_matrix_1.png" style="width:70%;height:auto;"/>
</div> <br>


**91 classes:**

- **Loss: 2.2890**

- **Accuracy: 0.6474**

<div align="center">
  <img src="https://github.com/sanjarakanovic/PaintingClassification/blob/main/imgs/confusion_matrix_2.png" style="width:80%;height:auto;"/>
</div>



# Jupyter Notebook 

The Jupyter Notebook provided in the repository is designed as fundamental code for conducting independent experiments and it can be seamlessly run on Google Colab.



# Web application

The web application is designed for users to upload their own images or use pre-existing images for the purpose of classification.

<div align="center">
  <img src="https://github.com/sanjarakanovic/PaintingClassification/blob/main/imgs/sc2.png"/>
</div>  <br>

<div align="center">
  <img src="https://github.com/sanjarakanovic/PaintingClassification/blob/main/imgs/sc3.png"/>
</div>  <br>

<div align="center">
  <img src="https://github.com/sanjarakanovic/PaintingClassification/blob/main/imgs/sc4.png"/>
</div>


## Technologies Used:
 - **Django**
 - **Angular**

## Requirements:
 - Python 3.x
 - PIP (included in Python from version 3.4)
 - Django
 - Angular CLI
 - Node.js
 - npm (Node Package Manager)


## Installation and setup instructions:

## Backend:
1. Install Python 3.x if not already installed.
2. Open a command prompt inside the `djangoapp` directory.
3. Create a virtual environment:
    ```
    python -m venv venv
    ```
4. Activate the environment:
    - **Windows:**
        ```
        venv\Scripts\activate.bat
        ```
    - **Unix/MacOS:**
        ```
        source venv/bin/activate
        ```
5. Install project dependencies:
    ```
    pip install -r requirements.txt
    ```
6. Navigate to the `mainapp` directory:
    ```
    cd mainapp
    ```
7. Run the Django development server:
    ```
    python manage.py runserver
    ```

## Frontend:
1. Install Node.js and npm if not already installed.
2. Install Angular CLI globally:
    ```
    npm install -g @angular/cli
    ```
3. Open a command prompt inside the `angularapp` directory.
   
4. Install dependencies:
    ```
    npm install
    ```
5. Start the Angular development server:
    ```
    ng serve
    ```
