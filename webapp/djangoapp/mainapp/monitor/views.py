from django.shortcuts import render
import numpy as np
from .apps import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from keras.applications.efficientnet import preprocess_input
from PIL import Image

class ClassifierView(APIView):
    parser_classes = (
        MultiPartParser,
        JSONParser,
    )

    class_names1 = ['Abstract Expressionism', 'Baroque', 'Constructivism', 'Cubbism', 'Impressionism', 'Neo Classical', 'Popart', 'Post impressionism','Realism', 'Renaissance', 'Romanticism', 'Surrealism', 'Symbolism']
    
    class_names2 = ['ALBRECHT DURER ', 'AMEDEO MODIGLIANI ', 'ANDREA MANTEGNA ', 'ANDY WARHOL ', 'ARSHILLE GORKY ', 'CAMILLE COROT ', 'CARAVAGGIO ', 'CASPAR DAVID FRIEDRICH ', 'CLAUDE LORRAIN ', 'CLAUDE MONET ', 'DANTE GABRIEL ROSSETTI ', 'DAVID HOCKNEY ', 'DIEGO VELAZQUEZ ', 'EDGAR DEGAS ', 'EDOUARD MANET ', 'EDVARD MUNCH ', 'EDWARD HOPPER ', 'EGON SCHIELE ', 'EL LISSITZKY ', 'EUGENE DELACROIX ', 'FERNAND LEGER ', 'FRA ANGELICO ', 'FRANCIS BACON ', 'FRANCISCO DE GOYA ', 'FRANCISCO DE ZURBARAN ', 'FRANS HALS ', 'FRANZ MARC ', 'FREDERIC EDWIN CHURCH ', 'FRIDA KAHLO ', 'GENTILESCHI ARTEMISIA ', 'GEORGES BRAQUE ', 'GEORGES DE LA TOUR ', 'GEORGES SEURAT ', 'GEORGIA OKEEFE ', 'GERHARD RICHTER ', 'GIORGIO DE CHIRICO ', 'GIORGIONE ', 'GIOTTO DI BONDONE ', 'GUSTAVE COURBET ', 'GUSTAVE MOREAU ', 'GUSTAV KLIMT ', 'HANS HOLBEIN THE YOUNGER ', 'HANS MEMLING ', 'HENRI MATISSE ', 'HIERONYMUS BOSCH ', 'JACKSON POLLOCK ', 'JACQUES-LOUIS DAVID ', 'JAMES ENSOR ', 'JAMES MCNEILL WHISTLER ', 'JAN VAN EYCK ', 'JAN VERMEER ', 'JASPER JOHNS ', 'JEAN-ANTOINE WATTEAU ', 'JEAN-AUGUSTE-DOMINIQUE INGRES ', 'JEAN FRANCOIS MILLET ', 'JEAN-MICHEL BASQUIAT ', 'JOACHIM PATINIR ', 'JOAN MIRO ', 'JOHN CONSTABLE ', 'JOSEPH MALLORD WILLIAM TURNER ', 'KAZIMIR MALEVICH ', 'LUCIO FONTANA ', 'MARC CHAGALL ', 'MARK ROTHKO ', 'MAX ERNST ', 'NICOLAS POUSSIN ', 'PAUL CEZANNE ', 'PAUL GAUGUIN ', 'PAUL KLEE ', 'PETER PAUL RUBENS ', 'PICASSO ', 'PIERRE-AUGUSTE RENOIR ', 'PIETER BRUEGEL THE ELDER ', 'PIET MONDRIAN ', 'RAPHAEL ', 'REMBRANDT VAN RIJN ', 'RENE MAGRITTE ', 'ROGER VAN DER WEYDEN ', 'ROY LICHTENSTEIN ', 'SALVADOR DALI ', 'SANDRO BOTTICELLI ', 'THEODORE GERICAULT ', 'TINTORETTO ', 'TITIAN ', 'UMBERTO BOCCIONI ', 'VINCENT VAN GOGH ', 'WASSILY KANDINSKY ', 'WILLEM DE KOONING ', 'WILLIAM BLAKE ', 'WILLIAM HOGARTH ', 'WINSLOW HOMER ']

    def post(self,request):

        if 'image' not in request.FILES:
            return Response({'error': 'Image file is required.'}, status=400)
        try:
            image_file = request.FILES['image']
            img = Image.open(image_file)
            img = img.convert('RGB')
            img = img.resize((224, 224))
            img_array = np.array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array.astype(np.float32))
    
            model1 = Model1Config.model
            model2 = Model2Config.model

            prediction1 = model1(img_array)
            class_index1 = np.argmax(prediction1)
            class_name1 = self.class_names1[class_index1]

            prediction2 = model2(img_array)
            class_index2 = np.argmax(prediction2)
            class_name2 = self.class_names2[class_index2]

            return Response({
            'status': 'success',
            'class1':class_name1,
            'class2':class_name2,
        }, status=201)
         
        except IOError:
            return Response({'error': 'The uploaded file is not recognized as an image.'}, status=400)
        except ValueError:
            return Response({'error': 'Mismatch error in provided input and expected model input.'}, status=500)
        except Exception:
            return Response({'error': 'An unexpected error occurred.'}, status=500)


    def get(self, request):
        return Response( {
        'status': 'success',
        'class_names1': self.class_names1,
        'class_names2': self.class_names2
        }, status=201)
