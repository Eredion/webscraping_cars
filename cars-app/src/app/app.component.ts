import { Component } from '@angular/core';
import { CarServiceService } from './car-service.service';
import { HttpClient } from '@angular/common/http';
import { ModalDismissReasons, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { FormControl } from '@angular/forms';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent {
    title = 'cars-app';

    page: number = 1;
    pageSize: number = 15;
    carSize: number = 0;
    maxSize: number = 10;
    cars: any = [];
    allCars: any = [];
    headers: any = [];
    selectedCar: any = [];

    constructor(
        private http: HttpClient,
        private modalService: NgbModal,
    ) {
        this.http.get('assets/cars.csv', { responseType: 'text' }).subscribe(data => {
            data.split('\n').forEach(el => {
                this.allCars.push(el.split(','));
            });
            this.headers = this.allCars[0];
            this.allCars.shift();
            this.carSize = this.allCars.length;
            this.refreshCars();
        });

    }

    refreshCars() {
        this.cars = this.allCars.slice(this.page * this.pageSize - this.pageSize, this.page * this.pageSize);
    }

    selectRow(row: any) {
        this.selectedCar = row;
    }

    open(content: any) {
        this.modalService.open(content, { ariaLabelledBy: 'modal-basic-title' })
    }
}
