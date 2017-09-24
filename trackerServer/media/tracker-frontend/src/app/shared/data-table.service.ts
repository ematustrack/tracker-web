import { Injectable } from '@angular/core';
import { Headers, RequestOptions, RequestMethod, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';
import { DataTable } from './data-table';

@Injectable()
export class DataTableService {
  private Url = 'http://54.175.253.151';  // URL to web api
  private headers = new Headers({ 'Content-Type': 'application/json' });
  constructor(private http: Http) { }

  getPhoto(id: string): string {
    return id;
  }

  getData(start: string, end: string, obra: string, st: string, folio: string, profesional: string): Promise<DataTable[]> {
    const url = `${this.Url}/server/datatable/`;
    const options = new RequestOptions({
      headers: this.headers,
    });

    const body = JSON.stringify({ start, end, obra, st, folio, profesional })
    return this.http
      .post(url, body, options)
      .toPromise()
      .then(response => response.json().data as DataTable[])
      .catch(this.handleError);
  }
  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error); // for demo purposes only
    return Promise.reject(error.message || error);
  }
}
