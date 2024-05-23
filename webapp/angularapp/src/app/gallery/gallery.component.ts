import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { ImageService } from '../services/image.service';
import { PredictionDTO } from '../DTOs/prediction-dto';
import { ClassesDTO } from '../DTOs/classes-dto';


@Component({
  selector: 'app-gallery',
  templateUrl: './gallery.component.html',
  styleUrl: './gallery.component.scss'
})
export class GalleryComponent {

  constructor(private imageService: ImageService) { }

  images: string[] = []
  pagedImages: string[] = []
  page = 0;
  pageSize = 5;
  currentSlideIndex = 0;
  currentScrollPosition = 0;

  scales: number[] = [1, 0.8, 0.73, 0.8, 1]
  rotatesY: number[] = [60, 36, 0, -33, -50]
  translatesX: number[] = [0, 0, 0, 0, 0];
  rotatesYConstants: number[] = [60, 36, 0, -33, -50];

  showImage = false;
  image = ""

  public style = "";
  public artist = "";

  public styles: string[] = [];
  public artists: string[] = [];

  public showMenu = false;
  public icon = "\u2630";

  public showStyles = false;
  public showArtists = false;
  public showAbout = false; 


   ngOnInit(): void {

    this.getAllClasses();
    this.imageService.getAssetFiles().then( (files: string[]) => {
      this.images = files;
      console.log(this.images[0]);
      this.getPagedImages();
    });
  }

  getPagedImages() {
    this.pagedImages = this.images.slice(this.page, this.page + this.pageSize);
  }

  nextPage() {
    if (this.page < Math.ceil(this.images.length - this.pageSize)) {
      this.page++;
      this.getPagedImages();
    } else
      this.page = 0;
  }

  previousPage() {
    if (this.page > 1) {
      this.page--;
      this.getPagedImages();
    } else {
      this.page = this.images.length - this.pageSize + 1;
    }
  }

  showOrHide(variableName: string) {
    const currentValue = Reflect.get(this, variableName);
    Reflect.set(this, variableName, !currentValue);
  }

  showOrHideMenu() {
    if (this.showMenu) {
      this.showMenu = false;
      this.icon = "\u2630";
    }
    else {
      this.showMenu = true;
      this.icon = "\u2716";
    }
  }


  onFileSelected(event: Event) {
    const selectedFiles = (event.target as HTMLInputElement)?.files;

    if (selectedFiles) {
      for (let i = 0; i < selectedFiles.length; i++) {
        const reader = new FileReader();
        reader.onload = (e) => {
          var index = this.images.indexOf(this.pagedImages[2]);

          this.images.splice(index, 0, e.target?.result as string);
          this.pagedImages.splice(2, 0, e.target?.result as string);
          this.pagedImages.pop();

        };
        reader.readAsDataURL(selectedFiles[i]);
      }
    }
}

  getImageClasses(file: any) {
    this.imageService.getImageClasses(file).subscribe((response: PredictionDTO) => {
      this.style = response.class1;
      this.artist = response.class2;
    });
  }

  getAllClasses() {
    this.imageService.getAllClasses().subscribe((response: ClassesDTO) => {
      this.styles = response.class_names1;
      this.artists = response.class_names2;
      console.log(this.styles);
      console.log(this.artists);

    });
  }



  chooseImage(event: Event) {
    const img = (event.target as HTMLImageElement);
    this.showImage = true;
    this.image = img.src;

    fetch(this.image)
      .then(res => res.blob())
      .then(blob => this.getImageClasses(blob))

  }

  removeImage() {
    this.image = "";
    this.showImage = false;
  }


  onScroll(event: WheelEvent) {
    if (event.deltaX < 0) {
      if (this.translatesX[0] < -13) {
        this.nextPage();
        this.translatesX = [0, 0, 0, 0, 0]
      }

      for (let i = 0; i < this.rotatesY.length; i++) {
        let y = this.rotatesY[i];
        this.translatesX[i] -= 6;
      }

    } else {
      if (this.translatesX[4] > 19) {
        this.previousPage();
        this.translatesX = [0, 0, 0, 0, 0]
      }

      for (let i = 0; i < this.rotatesY.length; i++) {
        let y = this.rotatesY[i];
        this.translatesX[i] += 6;
      }

    }

  }

}
