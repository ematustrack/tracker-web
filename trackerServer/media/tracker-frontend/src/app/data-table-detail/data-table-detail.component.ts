import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Params, Router }   from '@angular/router';
import { AgmCoreModule, MapsAPILoader } from '@agm/core';
import {HashLocationStrategy, Location, LocationStrategy} from '@angular/common';

import { DataTable } from './../shared/data-table';
import 'rxjs/add/operator/switchMap';
import { DataTableService } from './../shared/data-table.service';
import { DataTableDetailService } from './../shared/data-table-detail.service';
@Component({
  selector: 'app-data-table-detail',
  templateUrl: './data-table-detail.component.html',
  styleUrls: ['./data-table-detail.component.css']
})
export class DataTableDetailComponent implements OnInit {
  providers: [Location, { provide: LocationStrategy, useClass: HashLocationStrategy }]
  foto: string;
  lat: number;
  lng: number;
  note: string;
  obra: string;
  st: string;
  folio: string;
  phone: string;
  profesional: string;

  constructor(
    private route: ActivatedRoute,
    private location: Location,
    private datatableService: DataTableService,
    private dataDetailService: DataTableDetailService,
    private router: Router,
  ) { }

  ngOnInit(): void {
    if (typeof this.dataDetailService.foto == 'undefined') {
      alert("No hay una imagen, redirigiendo al home");
      this.router.navigate(['/home']);
      return;
    }
    this.foto = this.dataDetailService.foto;
    this.obra = this.dataDetailService.obra;
    this.st = this.dataDetailService.st;
    this.folio = this.dataDetailService.folio;
    this.profesional = this.dataDetailService.profesional;
    this.note = this.dataDetailService.note;
    this.lat = this.dataDetailService.lat;
    this.phone = this.dataDetailService.phone;
    this.lng = this.dataDetailService.lng;
  }
  goBack(): void {
    this.location.back();
  }

}
