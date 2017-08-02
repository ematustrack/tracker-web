import { BrowserModule } from '@angular/platform-browser';
import { NgModule, ViewChild, ApplicationRef } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { CdkTableModule } from '@angular/cdk/table';
import { HttpModule } from '@angular/http';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FlexLayoutModule } from '@angular/flex-layout';

import 'hammerjs';
import { AppRoutingModule } from './app-routing.module';

import { MdToolbarModule, MdCardModule, MdDatepickerModule } from '@angular/material';
import { MdInputModule, MdNativeDateModule, MdCheckboxModule} from '@angular/material';
import { MdButtonModule, MdTableModule, MdSortModule, MdPaginatorModule } from '@angular/material';
import {MdSelectModule, MdProgressSpinnerModule, MdListModule} from '@angular/material';
import {MdIconModule} from '@angular/material';





import { DashboardComponent } from './dashboard/dashboard.component';
import { DataTableComponent } from './data-table/data-table.component';

import {DataTableService} from './shared/data-table.service';
import {SelectionService} from './shared/selection.service';
import { DataTableDetailComponent } from './data-table-detail/data-table-detail.component';
import {DataTableDetailService} from './shared/data-table-detail.service';


import { AgmCoreModule } from '@agm/core';
import { MapComponent } from './map/map.component';
import { DataTableDetailPipe } from './shared/data-table-detail.pipe';


@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    DataTableComponent,
    DataTableDetailComponent,
    MapComponent,
    DataTableDetailPipe,
  ],
  imports: [
    AppRoutingModule,
    BrowserModule,
    MdToolbarModule,
    MdCardModule,
    MdSelectModule,
    FormsModule,
    MdListModule,
    CommonModule,
    HttpModule,
    MdInputModule,
    MdProgressSpinnerModule,
    MdButtonModule,
    MdIconModule,
    MdSortModule,
    MdTableModule,
    MdCheckboxModule,
    MdPaginatorModule,
    ReactiveFormsModule,
    MdDatepickerModule,
    MdNativeDateModule,
    BrowserAnimationsModule,
    FlexLayoutModule,
    AppRoutingModule,
    CdkTableModule,
    AgmCoreModule.forRoot({
      apiKey: 'AIzaSyDSxR8qyaTgNvzpEg4997fm_WC7ji1kwHY'
    })
  ],
  providers: [DataTableService, SelectionService, DataTableDetailService],
  bootstrap: [AppComponent]
})
export class AppModule { }
