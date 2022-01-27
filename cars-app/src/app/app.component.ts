import { Component } from '@angular/core';
import { CarServiceService } from './car-service.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass']
})
export class AppComponent {
  title = 'cars-app';

    constructor(
        public carService: CarServiceService
    ) {

    }
}
