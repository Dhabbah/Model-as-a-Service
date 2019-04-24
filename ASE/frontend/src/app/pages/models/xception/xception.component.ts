import { Component, OnInit } from '@angular/core';
import {HttpClient} from '@angular/common/http';

@Component({
  selector: 'app-xception',
  templateUrl: './xception.component.html',
  styleUrls: ['./xception.component.css']
})
export class XceptionComponent implements OnInit {

  constructor(private Http: HttpClient) { }
  fileToDisplay;
  fileToUpload;
  fileToPredict
  ReceivedData;

  ngOnInit() {
  }
  postMethod(files: FileList) {
    this.fileToUpload = files.item(0);
    const reader = new FileReader();
    reader.readAsDataURL((this.fileToUpload));
    reader.onload = (event) => {
      this.fileToDisplay = reader.result;
    }
    const formData = new FormData();
    formData.append('file', this.fileToUpload, this.fileToUpload.name);
    console.log(this.fileToUpload);
    this.fileToPredict = formData;
    this.ReceivedData = '';
  }

  predict(event) {
    this.Http.post('http://localhost:64006/predict', this.fileToPredict, {responseType: 'text'}).subscribe((data) => {
        this.ReceivedData = data;
        console.log(data);
      },
      error => {
        console.log(error);
      });
  }
}
