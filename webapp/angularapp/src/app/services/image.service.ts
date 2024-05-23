import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { PredictionDTO } from '../DTOs/prediction-dto';
import { ClassesDTO } from '../DTOs/classes-dto';

@Injectable({
  providedIn: 'root'
})
export class ImageService {

  constructor(private httpClient: HttpClient) { }

   url = 'http://127.0.0.1:8000/classifier';

  getAssetFiles(): Promise<string[]> {
    return this.httpClient.get('assets/filenames.json').toPromise().then((response: any) => {
        return response.filenames;
      });
    }
  

  getImageClasses(file: any): Observable<PredictionDTO> {
    const formData = new FormData();
    formData.append('image', file);
    return this.httpClient.post<PredictionDTO>(this.url, formData);
  }

  getAllClasses(): Observable<ClassesDTO> {
    return this.httpClient.get<ClassesDTO>(this.url);

  }
}
