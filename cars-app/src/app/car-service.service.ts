import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root'
})
export class CarServiceService {

    km0Cars: any = [] ;
    secondHandCars: any = [];
    headers: any = [];

    constructor(
        private http: HttpClient
    ) {
        this.http.get('assets/cars-km0.csv', { responseType: 'text' }).subscribe(data => {
            data.split('\n').forEach(el => {
                this.km0Cars.push(el.split(','));
            });
            this.headers = this.km0Cars[0];
            this.km0Cars.shift();
        });

        this.http.get('assets/cars-segunda-mano.csv', { responseType: 'text' }).subscribe(data => {
            data.split('\n').forEach(element => {
                this.secondHandCars.push(element.split(','));
            });
            this.secondHandCars.shift();
        });
    }
}
