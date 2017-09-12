import {Component, ViewChild, OnChanges, Input, OnInit, ElementRef, ChangeDetectorRef, AfterViewInit} from '@angular/core';
import {DataSource} from '@angular/cdk/table';
import {MdPaginator, MdSort} from '@angular/material';
import {Observable} from 'rxjs/Observable';
import {Http, Response} from '@angular/http';
import {BehaviorSubject} from 'rxjs/BehaviorSubject';
import { DatePipe } from '@angular/common';
import {DataTableDetailService} from '../shared/data-table-detail.service';
import {DataTableDetailPipe} from '../shared/data-table-detail.pipe';

import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/merge';
import 'rxjs/add/observable/of';
import 'rxjs/add/observable/fromEvent';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/startWith';
import 'rxjs/add/operator/switchMap';
import 'rxjs/add/operator/distinctUntilChanged';
import 'rxjs/add/operator/debounceTime';

import { DataTableService } from '../shared/data-table.service';
import { DataTable, DataInTable } from '../shared/data-table';
import { Router }   from '@angular/router';


/**
 * @title Feature-rich data table
 */
@Component({
  selector: 'app-data-table',
  styleUrls: ['data-table.component.css'],
  templateUrl: 'data-table.component.html',
})
export class DataTableComponent implements OnChanges, AfterViewInit {
  displayedColumns = ['foto', 'obra', 'st', 'folio', 'profesional', 'date'];
  exampleDatabase: ExampleDatabase | null;
  dataSource: ExampleDataSource | null;

  @Input() start: string;
  @Input() end: string;
  @Input() obra: string;
  @Input() st: string;
  @Input() folio: string;
  @Input() profesional: string;

  @ViewChild(MdPaginator) paginator: MdPaginator;

  constructor(
    private router: Router,
    private datatableService: DataTableService,
    private changeDetector: ChangeDetectorRef,
    private dataDetailService: DataTableDetailService) {
  }

  ngOnChanges() {
    this.exampleDatabase = new ExampleDatabase(this.datatableService);
    //this.getDataTable(this.start, this.end);
    this.dataSource = new ExampleDataSource(this.exampleDatabase!, this.paginator, this.start, this.end, this.obra, this.st, this.folio, this.profesional);

  }

  ngAfterViewInit() {

    //
    // TODO: Remove this as it is a workaround to make the table visible when the page got reloaded
    //var eventObservable = Observable.fromEvent(
    //  this.f.nativeElement, 'keyup');
    //
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
  //getDataTable call dataTableService with two dates
  dataChange: BehaviorSubject<DataTable[]> = new BehaviorSubject<DataTable[]>([]);
  get data(): DataTable[] { return this.dataChange.value; }

  getDataTable(start: string, end: string, obra: string, st: string, folio: string, profesional: string): Observable<DataInTable> {
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
    return this.datatableService.getData(start, end, obra, st, folio, profesional)
      .map(response => {
        this.dataChange.next(response.json());
        return response.json() as DataInTable;
      });
  }

  constructor(private datatableService: DataTableService) { }
}

/**
 * Data source to provide what data should be rendered in the table. Note that the data source
 * can retrieve its data in any way. In this case, the data source is provided a reference
 * to a common data base, ExampleDatabase. It is not the data source's responsibility to manage
 * the underlying data. Instead, it only needs to take the data and send the table exactly what
 * should be rendered.
 */
export class ExampleDataSource extends DataSource<DataTable> {
  resultsLength = 0;
  isLoadingResults: boolean = false;
  isRateLimitReached: boolean = false;

  constructor(private _exampleDatabase: ExampleDatabase,
    private _paginator: MdPaginator,
    private start: string,
    private end: string,
    private obra: string,
    private st: string,
    private folio: string,
    private profesional: string) {
    super();
  }

  /** Connect function called by the table to retrieve one stream containing the data to render. */
  connect(): Observable<DataTable[]> {

    // Listen for any changes in the base data, sorting, filtering, or pagination
    const displayDataChanges = [
    ];

    //this._sort.mdSortChange.subscribe(() => this._paginator.pageIndex = 0);
    return Observable.merge(...displayDataChanges)
      .startWith(null)
      .switchMap(() => {
        this.isLoadingResults = true;
        return this._exampleDatabase.getDataTable(
          this.start, this.end, this.obra, this.st, this.folio, this.profesional);
      })
      .map(data => {

        // Flip flag to show that loading has finished.
        this.isLoadingResults = false;
        this.isRateLimitReached = false;
        //
        this.resultsLength = data["data"].length;
        //
        return data["data"];//.getSortedData();
      })
      .catch(() => {
        this.isLoadingResults = false;
        // Catch if the GitHub API has reached its rate limit. Return empty data.
        this.isRateLimitReached = true;
        return Observable.of(null);
      });
  }

  disconnect() { }


}
