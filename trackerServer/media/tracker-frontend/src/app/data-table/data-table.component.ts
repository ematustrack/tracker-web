import { Component, ElementRef, ViewChild, Input } from '@angular/core';
import { DataSource } from '@angular/cdk/table';
import { MdPaginator, MdSort, SelectionModel } from '@angular/material';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/startWith';
import 'rxjs/add/observable/merge';
import 'rxjs/add/observable/fromEvent';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/distinctUntilChanged';
import 'rxjs/add/operator/debounceTime';

import { DataTableService } from '../shared/data-table.service';
import { DataTable } from '../shared/data-table';
import { Router } from '@angular/router';
import { DatePipe } from '@angular/common';
import { DataTableDetailService } from '../shared/data-table-detail.service';
import { DataTableDetailPipe } from '../shared/data-table-detail.pipe';


/**
 * @title Feature-rich data table
 */
@Component({
  selector: 'app-data-table',
  styleUrls: ['data-table.component.css'],
  templateUrl: 'data-table.component.html',
})
export class DataTableComponent {
  displayedColumns = ['foto', 'obra', 'st', 'folio', 'profesional', 'date'];
  exampleDatabase: ExampleDatabase | null;
  selection = new SelectionModel<string>(true, []);
  dataSource: ExampleDataSource | null;
  photos: DataTable[];
  @Input() start: string;
  @Input() end: string;
  @Input() obra: string;
  @Input() st: string;
  @Input() folio: string;
  @Input() profesional: string;
  @ViewChild(MdPaginator) paginator: MdPaginator;
  @ViewChild(MdSort) sort: MdSort;

  constructor(
    private router: Router,
    private datatableService: DataTableService,
    private dataDetailService: DataTableDetailService) {
  }

  ngOnInit() {
    this.exampleDatabase = new ExampleDatabase(this.datatableService, this.start, this.end, this.obra, this.st, this.folio, this.profesional);
    //this.getDataTable(this.start, this.end);
    this.dataSource = new ExampleDataSource(this.exampleDatabase, this.paginator, this.sort);
  }

  ngOnChanges() {
    this.exampleDatabase = new ExampleDatabase(this.datatableService, this.start, this.end, this.obra, this.st, this.folio, this.profesional);
    //this.getDataTable(this.start, this.end);
    this.dataSource = new ExampleDataSource(this.exampleDatabase, this.paginator, this.sort);
  }

  gotoDetail(row: any): void {
    this.dataDetailService.foto = row.foto;
    this.dataDetailService.obra = row.obra;
    this.dataDetailService.st = row.st;
    this.dataDetailService.folio = row.folio;
    this.dataDetailService.profesional = row.profesional;
    this.dataDetailService.note = row.note;
    this.dataDetailService.lat = row.lat;
    this.dataDetailService.lng = row.lng;
    this.dataDetailService.phone = row.phone;
    this.router.navigate(['/detail']);
  }

}


/** An example database that the data source uses to retrieve data for the table. */
export class ExampleDatabase {
  /** Stream that emits whenever the data has been modified. */
  dataChange: BehaviorSubject<DataTable[]> = new BehaviorSubject<DataTable[]>([]);
  get data(): DataTable[] { return this.dataChange.value; }
  photos: DataTable[];

  constructor(private datatableService: DataTableService, start: string, end: string, obra: string, st: string, folio: string, profesional: string) {
    if (!start)
      start = "";
    if (!end)
      end = "";
    if (!obra)
      obra = "";
    if (!st)
      st = "";
    if (!folio)
      folio = "";
    if (!profesional)
      profesional = "";

    this.getDataTable(start, end, obra, st, folio, profesional);
  }

  //getDataTable call dataTableService with two dates
  getDataTable(start: string, end: string, obra: string, st: string, folio: string, profesional: string): void {
    this.datatableService.getData(start, end, obra, st, folio, profesional).then(photos => {
      //this.dataChange = photos;
      for (let i = 0; i < photos.length; i++) {
        const copiedData = this.data.slice();
        copiedData.push(photos[i]);
        this.dataChange.next(copiedData);
      }
    })

  }
}

/**
 * Data source to provide what data should be rendered in the table. Note that the data source
 * can retrieve its data in any way. In this case, the data source is provided a reference
 * to a common data base, ExampleDatabase. It is not the data source's responsibility to manage
 * the underlying data. Instead, it only needs to take the data and send the table exactly what
 * should be rendered.
 */
export class ExampleDataSource extends DataSource<any> {
  _filterChange = new BehaviorSubject('');
  get filter(): string { return this._filterChange.value; }
  set filter(filter: string) { this._filterChange.next(filter); }


  filteredData: DataTable[] = [];
  renderedData: DataTable[] = [];

  constructor(private _exampleDatabase: ExampleDatabase,
    private _paginator: MdPaginator,
    private _sort: MdSort) {
    super();
    // Reset to the first page when the user changes the filter.
    this._filterChange.subscribe(() => this._paginator.pageIndex = 0);
  }

  /** Connect function called by the table to retrieve one stream containing the data to render. */
  connect(): Observable<DataTable[]> {
    // Listen for any changes in the base data, sorting, filtering, or pagination
    const displayDataChanges = [
      this._exampleDatabase.dataChange,
      this._sort.mdSortChange,
      this._filterChange,
      this._paginator.page,
    ];

    return Observable.merge(...displayDataChanges).map(() => {
      // Filter data
      this.filteredData = this._exampleDatabase.data.slice().filter((item: DataTable) => {
        let searchStr = (item.obra).toLowerCase();
        return searchStr.indexOf(this.filter.toLowerCase()) != -1;
      });

      // Sort filtered data
      const sortedData = this.sortData(this.filteredData.slice());

      // Grab the page's slice of the filtered sorted data.
      const startIndex = this._paginator.pageIndex * this._paginator.pageSize;
      this.renderedData = sortedData.splice(startIndex, this._paginator.pageSize);
      return this.renderedData;
    });
  }

  disconnect() { }

  /** Returns a sorted copy of the database data. */
  sortData(data: DataTable[]): DataTable[] {
    if (!this._sort.active || this._sort.direction == '') { return data; }

    return data.sort((a, b) => {
      let propertyA: number | string | Date = '';
      let propertyB: number | string | Date = '';

      switch (this._sort.active) {
        case 'foto': [propertyA, propertyB] = [a.foto, b.foto]; break;
        case 'obra': [propertyA, propertyB] = [a.obra, b.obra]; break;
        case 'st': [propertyA, propertyB] = [a.st, b.st]; break;
        case 'folio': [propertyA, propertyB] = [a.folio, b.folio]; break;
        case 'profesional': [propertyA, propertyB] = [a.profesional, b.profesional]; break;
        case 'date': [propertyA, propertyB] = [a.date, b.date]; break;
      }

      let valueA = isNaN(+propertyA) ? propertyA : +propertyA;
      let valueB = isNaN(+propertyB) ? propertyB : +propertyB;

      return (valueA < valueB ? -1 : 1) * (this._sort.direction == 'asc' ? 1 : -1);
    });
  }
}
